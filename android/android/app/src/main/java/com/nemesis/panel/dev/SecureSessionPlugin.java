package com.nemesis.panel.dev;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import org.json.JSONObject;

@CapacitorPlugin(name = "SecureSession")
public class SecureSessionPlugin extends Plugin {
    private KeystoreSessionStore store;
    @Override public void load() { store = new KeystoreSessionStore(getContext()); }
    @PluginMethod public void read(PluginCall call) {
        try {
            JSONObject saved = store.read();
            JSObject result = new JSObject();
            result.put("session", saved == null ? JSONObject.NULL : new JSObject(saved.toString()));
            call.resolve(result);
        } catch (Exception ignored) { call.reject("Saved session unavailable. Sign in again.", "SECURE_STORAGE"); }
    }
    @PluginMethod public void write(PluginCall call) {
        try {
            Long expiry = call.getLong("expiresAt");
            if (expiry == null) throw new IllegalArgumentException();
            store.write(call.getString("token"), expiry);
            call.resolve();
        } catch (Exception ignored) { call.reject("Unable to save the secure session.", "SECURE_STORAGE"); }
    }
    @PluginMethod public void clear(PluginCall call) {
        try { store.clear(); call.resolve(); }
        catch (Exception ignored) { call.reject("Unable to remove the saved session.", "SECURE_STORAGE"); }
    }
}
