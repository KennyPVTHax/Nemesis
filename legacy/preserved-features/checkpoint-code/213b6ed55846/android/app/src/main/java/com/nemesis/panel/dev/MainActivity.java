package com.nemesis.panel.dev;

import android.os.Bundle;
import android.view.ViewGroup;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import com.getcapacitor.BridgeActivity;

/** Local UI host. No message, contact, accessibility or background collection. */
public class MainActivity extends BridgeActivity {
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        WindowCompat.setDecorFitsSystemWindows(getWindow(), false);
        ViewCompat.setOnApplyWindowInsetsListener(bridge.getWebView(), (view, insets) -> {
            Insets bars = insets.getInsets(WindowInsetsCompat.Type.systemBars()
                    | WindowInsetsCompat.Type.displayCutout());
            Insets keyboard = insets.getInsets(WindowInsetsCompat.Type.ime());
            ViewGroup.LayoutParams raw = view.getLayoutParams();
            if (raw instanceof ViewGroup.MarginLayoutParams) {
                ViewGroup.MarginLayoutParams margins = (ViewGroup.MarginLayoutParams) raw;
                int bottom = Math.max(bars.bottom, keyboard.bottom);
                if (margins.leftMargin != bars.left || margins.topMargin != bars.top
                        || margins.rightMargin != bars.right || margins.bottomMargin != bottom) {
                    margins.setMargins(bars.left, bars.top, bars.right, bottom);
                    view.setLayoutParams(margins);
                }
            }
            return insets;
        });
        ViewCompat.requestApplyInsets(bridge.getWebView());
    }
}
