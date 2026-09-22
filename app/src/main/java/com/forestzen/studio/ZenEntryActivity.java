package com.forestzen.studio;

import android.app.Activity;
import android.app.ActivityOptions;
import android.app.KeyguardManager;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;

public class ZenEntryActivity extends Activity {
    private final Handler handler = new Handler(Looper.getMainLooper());
    private boolean animationStarted = false;

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);

        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setShowWhenLocked(true);
        getWindow().setStatusBarColor(android.graphics.Color.TRANSPARENT);
        getWindow().setNavigationBarColor(android.graphics.Color.TRANSPARENT);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);

        setContentView(R.layout.activity_zen_entry);

        KeyguardManager keyguard = (KeyguardManager) getSystemService(KEYGUARD_SERVICE);
        if (keyguard != null && keyguard.isKeyguardLocked()) {
            keyguard.requestDismissKeyguard(this, new KeyguardManager.KeyguardDismissCallback() {
                @Override public void onDismissSucceeded() {
                    playEntryAnimation();
                }

                @Override public void onDismissCancelled() {
                    finish();
                }

                @Override public void onDismissError() {
                    playEntryAnimation();
                }
            });
        } else {
            playEntryAnimation();
        }
    }

    private void playEntryAnimation() {
        if (animationStarted) return;
        animationStarted = true;

        View root = findViewById(R.id.zen_entry_root);
        View background = findViewById(R.id.zen_entry_background);
        View glass = findViewById(R.id.zen_entry_glass);
        View eyebrow = findViewById(R.id.zen_entry_eyebrow);
        View footer = findViewById(R.id.zen_entry_footer);

        root.setAlpha(0f);
        background.setScaleX(1.10f);
        background.setScaleY(1.10f);
        glass.setAlpha(0f);
        glass.setScaleX(0.92f);
        glass.setScaleY(0.92f);
        glass.setTranslationY(54f);
        eyebrow.setAlpha(0f);
        eyebrow.setTranslationY(-18f);
        footer.setAlpha(0f);
        footer.setTranslationY(24f);

        root.animate()
                .alpha(1f)
                .setDuration(320)
                .start();

        background.animate()
                .scaleX(1f)
                .scaleY(1f)
                .setDuration(1050)
                .setInterpolator(new android.view.animation.DecelerateInterpolator())
                .start();

        glass.animate()
                .alpha(1f)
                .scaleX(1f)
                .scaleY(1f)
                .translationY(0f)
                .setStartDelay(120)
                .setDuration(720)
                .setInterpolator(new android.view.animation.DecelerateInterpolator())
                .start();

        eyebrow.animate()
                .alpha(1f)
                .translationY(0f)
                .setStartDelay(270)
                .setDuration(620)
                .start();

        footer.animate()
                .alpha(1f)
                .translationY(0f)
                .setStartDelay(420)
                .setDuration(620)
                .start();

        handler.postDelayed(this::openStudio, 1350);
    }

    private void openStudio() {
        if (isFinishing()) return;

        Intent intent = new Intent(this, MainActivity.class);
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);

        ActivityOptions options = ActivityOptions.makeCustomAnimation(
                this,
                android.R.anim.fade_in,
                android.R.anim.fade_out
        );
        startActivity(intent, options.toBundle());
        finish();
    }

    @Override
    protected void onDestroy() {
        handler.removeCallbacksAndMessages(null);
        super.onDestroy();
    }
}
