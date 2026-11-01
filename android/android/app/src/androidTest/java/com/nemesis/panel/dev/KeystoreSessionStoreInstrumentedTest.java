package com.nemesis.panel.dev;

import static org.junit.Assert.*;
import android.content.Context;
import androidx.test.platform.app.InstrumentationRegistry;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import java.util.UUID;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

/** Requires a real Android runtime; compiling this is not evidence these tests ran. */
@RunWith(AndroidJUnit4.class)
public class KeystoreSessionStoreInstrumentedTest {
    private Context context;
    private KeystoreSessionStore store;
    @Before public void setup() throws Exception {
        context = InstrumentationRegistry.getInstrumentation().getTargetContext();
        store = new KeystoreSessionStore(context);
        store.clear();
    }
    @After public void cleanup() throws Exception { store.clear(); }
    @Test public void encryptedRoundTripAndLogoutErasure() throws Exception {
        String token = UUID.randomUUID().toString() + UUID.randomUUID();
        long expiry = System.currentTimeMillis() + 60000;
        store.write(token, expiry);
        String onDisk = context.getSharedPreferences(KeystoreSessionStore.PREFS, Context.MODE_PRIVATE).getAll().toString();
        assertFalse("Plaintext token must not be persisted", onDisk.contains(token));
        assertEquals(token, store.read().getString("token"));
        assertEquals(expiry, store.read().getLong("expiresAt"));
        store.clear();
        assertNull(store.read());
    }
    @Test public void tamperedCiphertextIsRejectedAndErased() throws Exception {
        store.write(UUID.randomUUID().toString(), System.currentTimeMillis() + 60000);
        context.getSharedPreferences(KeystoreSessionStore.PREFS, Context.MODE_PRIVATE).edit().putString("ciphertext", "tampered").commit();
        assertThrows(Exception.class, () -> store.read());
        assertNull(store.read());
    }
}
