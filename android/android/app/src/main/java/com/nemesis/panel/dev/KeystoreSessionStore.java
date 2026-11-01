package com.nemesis.panel.dev;

import android.content.Context;
import android.content.SharedPreferences;
import android.security.keystore.KeyGenParameterSpec;
import android.security.keystore.KeyProperties;
import android.util.Base64;
import java.nio.charset.StandardCharsets;
import java.security.GeneralSecurityException;
import java.security.KeyStore;
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import org.json.JSONObject;

/** Only AES-GCM ciphertext is persisted. The non-exportable key lives in Android Keystore. */
final class KeystoreSessionStore {
    static final String PREFS = "nemesis_secure_session";
    static final String ALIAS = "nemesis.session.aes.v1";
    private final Context context;
    KeystoreSessionStore(Context context) { this.context = context.getApplicationContext(); }
    private SharedPreferences preferences() { return context.getSharedPreferences(PREFS, Context.MODE_PRIVATE); }
    private KeyStore keystore() throws Exception {
        KeyStore store = KeyStore.getInstance("AndroidKeyStore");
        store.load(null);
        return store;
    }
    private SecretKey encryptionKey() throws Exception {
        KeyStore store = keystore();
        if (store.containsAlias(ALIAS)) return (SecretKey) store.getKey(ALIAS, null);
        KeyGenerator generator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore");
        generator.init(new KeyGenParameterSpec.Builder(ALIAS, KeyProperties.PURPOSE_ENCRYPT | KeyProperties.PURPOSE_DECRYPT)
            .setBlockModes(KeyProperties.BLOCK_MODE_GCM).setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
            .setRandomizedEncryptionRequired(true).setKeySize(256).build());
        return generator.generateKey();
    }
    private byte[] aad() { return (context.getPackageName() + ":session:v1").getBytes(StandardCharsets.UTF_8); }
    synchronized void write(String token, long expiresAt) throws Exception {
        if (token == null || token.length() < 16 || token.length() > 16384 || token.matches("(?s).*\\s.*") || expiresAt <= System.currentTimeMillis())
            throw new GeneralSecurityException("Invalid session envelope");
        JSONObject envelope = new JSONObject().put("version", 1).put("token", token).put("expiresAt", expiresAt);
        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        cipher.init(Cipher.ENCRYPT_MODE, encryptionKey());
        cipher.updateAAD(aad());
        byte[] ciphertext = cipher.doFinal(envelope.toString().getBytes(StandardCharsets.UTF_8));
        if (!preferences().edit().putString("ciphertext", Base64.encodeToString(ciphertext, Base64.NO_WRAP))
            .putString("iv", Base64.encodeToString(cipher.getIV(), Base64.NO_WRAP)).commit())
            throw new GeneralSecurityException("Session storage unavailable");
    }
    synchronized JSONObject read() throws Exception {
        String ciphertext = preferences().getString("ciphertext", null);
        if (ciphertext == null) return null;
        try {
            KeyStore store = keystore();
            if (!store.containsAlias(ALIAS)) throw new GeneralSecurityException("Session key unavailable");
            String iv = preferences().getString("iv", null);
            if (iv == null) throw new GeneralSecurityException("Session IV unavailable");
            Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
            cipher.init(Cipher.DECRYPT_MODE, (SecretKey) store.getKey(ALIAS, null), new GCMParameterSpec(128, Base64.decode(iv, Base64.NO_WRAP)));
            cipher.updateAAD(aad());
            JSONObject envelope = new JSONObject(new String(cipher.doFinal(Base64.decode(ciphertext, Base64.NO_WRAP)), StandardCharsets.UTF_8));
            if (envelope.getInt("version") != 1 || envelope.getLong("expiresAt") <= System.currentTimeMillis()) { clear(); return null; }
            return envelope;
        } catch (Exception failure) {
            clear();
            throw new GeneralSecurityException("Saved session could not be opened");
        }
    }
    synchronized void clear() throws Exception {
        KeyStore store = keystore();
        if (store.containsAlias(ALIAS)) store.deleteEntry(ALIAS);
        // Even a failed preferences commit cannot recover ciphertext after key deletion.
        preferences().edit().clear().commit();
    }
}
