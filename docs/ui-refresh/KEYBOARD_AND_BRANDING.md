Historical development report retained from the prior workspace delivery. Artifact references may point outside this public repository; current migration verification is in ../VALIDATION.md.

# Keyboard and branding — approved UI update

The prior keyboard root fix is retained: Android `adjustResize` owns the viewport, `setDecorFitsSystemWindows(true)` is set, custom IME/WebView margins are absent, Capacitor fullscreen keyboard resizing is disabled, and target-35 forced edge-to-edge is opted out. No second JavaScript/native keyboard-height subtraction has been added.

Approved authentication styling uses natural minimum-height document flow, a centered flexible form, short-height spacing and normal scrolling. OTP is one labeled accessible text input with numeric keyboard/autofill and six visual slots. Leading zeroes remain valid. Browser short-viewport focus/scroll/dismissal checks passed; there is no physical Android keyboard test evidence from this environment. The detailed original investigation remains in `../phase2/KEYBOARD_ROOT_CAUSE.md`.

The owner approved the UI direction and explicitly requested a newly designed logo because the prior helmet crop looked odd. A simpler crimson N monogram was generated for that request. The original generated asset is retained unchanged at `/workspace/generated_images/exec-bfa0fc44-7c7c-467d-8ced-9f33be707292.png`, copied into `android-app/public/nemesis-mark.png` (1254×1254 RGBA). The original owner-supplied JPG remains byte-for-byte unchanged; it is no longer the active brand mark.

The mark is used in login/OTP, utility-page headers and scoped logo overlays on the unchanged original dashboard/APK markup. Native packaging renders square/round 48dp launcher icons and 108dp adaptive foregrounds for mdpi through xxxhdpi with a 66dp safe zone. Existing native splash themes reference the refreshed foreground. The background matches `#0c020d`. No new permissions or remote branding asset is required.

The approved UI changes are a compact wordmark, comfortable form controls, consistent outline tab icons, readable dashboard controls and grouped expandable settings. Original typography, crimson design language, themes, original dashboard structure/animations/controls and exact four-tab purposes remain. Unavailable operations are still explicitly unavailable. New UI code is additive; generated original JSX/CSS/icons/provenance are unchanged.

`NEMESIS-updated-ui.png` is a board made from actual Chromium-rendered screenshots of these components. It is not an Android device capture. Login is the shipped enabled interface; OTP/dashboard/account captures use isolated synthetic responses, never real codes or customer data. Native launcher previews are rendered resources, not OS screenshots.
