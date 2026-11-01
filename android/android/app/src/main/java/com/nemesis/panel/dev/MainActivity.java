package com.nemesis.panel.dev;

import android.os.Bundle;
import androidx.core.view.WindowCompat;
import com.getcapacitor.BridgeActivity;

/** Android owns viewport resizing. Do not subtract IME height a second time. */
public class MainActivity extends BridgeActivity {
    @Override public void onCreate(Bundle state) {
        registerPlugin(SecureSessionPlugin.class);
        super.onCreate(state);
        WindowCompat.setDecorFitsSystemWindows(getWindow(), true);
    }
}
