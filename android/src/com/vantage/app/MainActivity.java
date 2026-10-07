package com.vantage.app;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.ConsoleMessage;
import android.webkit.JsPromptResult;
import android.webkit.JsResult;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

public class MainActivity extends Activity {
    private WebView webView;
    private long lastBackPressTime = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Configure Window for edge-to-edge / dark theme
        Window window = getWindow();
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);
            window.setStatusBarColor(Color.parseColor("#14161c"));
            window.setNavigationBarColor(Color.parseColor("#1b1e26"));
        }

        // Create lightweight WebView
        webView = new WebView(this);
        webView.setBackgroundColor(Color.parseColor("#14161c"));

        // Enable hardware acceleration
        webView.setLayerType(View.LAYER_TYPE_HARDWARE, null);

        // WebSettings optimized for speed and low RAM footprint
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setAllowFileAccessFromFileURLs(true);
        settings.setAllowUniversalAccessFromFileURLs(true);
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);
        settings.setDisplayZoomControls(false);
        settings.setBuiltInZoomControls(false);
        settings.setSupportZoom(false);
        settings.setCacheMode(WebSettings.LOAD_DEFAULT);

        // Native Storage & Platform Bridge (survives app death, swipe-away, low RAM)
        webView.addJavascriptInterface(new VantageNativeBridge(this), "VantageNativeStorage");

        // Keep local content in WebView, open external URLs in system browser
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                if (url != null && (url.startsWith("file:") || url.startsWith("http://localhost"))) {
                    return false;
                }
                try {
                    Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                    startActivity(intent);
                    return true;
                } catch (Exception e) {
                    return false;
                }
            }
        });

        // WebChromeClient with safety handlers so JS dialogs never block the WebView thread
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onConsoleMessage(ConsoleMessage consoleMessage) {
                return true;
            }

            @Override
            public boolean onJsAlert(WebView view, String url, String message, JsResult result) {
                result.confirm();
                return true;
            }

            @Override
            public boolean onJsConfirm(WebView view, String url, String message, JsResult result) {
                result.confirm();
                return true;
            }

            @Override
            public boolean onJsPrompt(WebView view, String url, String message, String defaultValue, JsPromptResult result) {
                result.confirm(defaultValue != null ? defaultValue : "");
                return true;
            }
        });

        setContentView(webView);

        // Load Vantage Web Application from assets
        webView.loadUrl("file:///android_asset/www/index.html");
    }

    public static class VantageNativeBridge {
        private final android.content.SharedPreferences prefs;
        private final int statusBarDp;

        public VantageNativeBridge(Activity activity) {
            this.prefs = activity.getSharedPreferences("vantage_native_store", Activity.MODE_PRIVATE);
            int resourceId = activity.getResources().getIdentifier("status_bar_height", "dimen", "android");
            int statusBarPx = (resourceId > 0) ? activity.getResources().getDimensionPixelSize(resourceId) : 0;
            float density = activity.getResources().getDisplayMetrics().density;
            this.statusBarDp = density > 0 ? Math.round(statusBarPx / density) : 24;
        }

        @android.webkit.JavascriptInterface
        public String get(String key) {
            return prefs.getString(key, null);
        }

        @android.webkit.JavascriptInterface
        public boolean set(String key, String value) {
            return prefs.edit().putString(key, value).commit();
        }

        @android.webkit.JavascriptInterface
        public boolean delete(String key) {
            return prefs.edit().remove(key).commit();
        }

        @android.webkit.JavascriptInterface
        public int getStatusBarHeight() {
            return statusBarDp > 0 ? statusBarDp : 26;
        }
    }

    @Override
    public void onBackPressed() {
        if (webView != null) {
            // Query JavaScript handleAndroidBack()
            webView.evaluateJavascript("window.handleAndroidBack ? window.handleAndroidBack() : false;", new ValueCallback<String>() {
                @Override
                public void onReceiveValue(String value) {
                    if ("true".equalsIgnoreCase(value) || "\"true\"".equalsIgnoreCase(value)) {
                        // Handled by JavaScript (e.g. closed modal, drawer, or note editor)
                        return;
                    }
                    // Not handled by JS: check if webView has history
                    if (webView.canGoBack()) {
                        webView.goBack();
                    } else {
                        // Double-tap back within 2 seconds to exit
                        long currentTime = System.currentTimeMillis();
                        if (currentTime - lastBackPressTime < 2000) {
                            finish();
                        } else {
                            lastBackPressTime = currentTime;
                            Toast.makeText(MainActivity.this, "Press back again to exit Vantage", Toast.LENGTH_SHORT).show();
                        }
                    }
                }
            });
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public void onTrimMemory(int level) {
        super.onTrimMemory(level);
        if (webView != null) {
            webView.evaluateJavascript("if (typeof window.flushAllUnsaved === 'function') window.flushAllUnsaved();", null);
            if (level >= TRIM_MEMORY_MODERATE) {
                webView.clearCache(false);
                webView.freeMemory();
            }
        }
        System.gc();
    }

    @Override
    public void onLowMemory() {
        super.onLowMemory();
        if (webView != null) {
            webView.evaluateJavascript("if (typeof window.flushAllUnsaved === 'function') window.flushAllUnsaved();", null);
            webView.freeMemory();
        }
        System.gc();
    }

    @Override
    protected void onPause() {
        if (webView != null) {
            webView.evaluateJavascript("if (typeof window.flushAllUnsaved === 'function') window.flushAllUnsaved();", null);
            webView.onPause();
            webView.pauseTimers();
        }
        super.onPause();
    }

    @Override
    protected void onStop() {
        if (webView != null) {
            webView.evaluateJavascript("if (typeof window.flushAllUnsaved === 'function') window.flushAllUnsaved();", null);
        }
        super.onStop();
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (webView != null) {
            webView.onResume();
            webView.resumeTimers();
        }
    }

    @Override
    protected void onDestroy() {
        if (webView != null) {
            webView.loadUrl("about:blank");
            webView.stopLoading();
            webView.setWebChromeClient(null);
            webView.setWebViewClient(null);
            webView.destroy();
            webView = null;
        }
        super.onDestroy();
    }
}
