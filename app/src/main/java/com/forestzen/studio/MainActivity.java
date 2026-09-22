package com.forestzen.studio;

import android.app.Activity;
import android.app.WallpaperManager;
import android.appwidget.AppWidgetManager;
import android.content.ComponentName;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.LinearGradient;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.Shader;
import android.os.Bundle;
import android.provider.Settings;
import android.widget.ImageView;
import android.widget.Toast;
import java.io.IOException;

public class MainActivity extends Activity {
    private Bitmap wallpaper;

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        setContentView(R.layout.activity_main);

        wallpaper = createForestWallpaper(1440, 3200);
        ((ImageView) findViewById(R.id.preview)).setImageBitmap(wallpaper);

        findViewById(R.id.homeWallpaper).setOnClickListener(v -> applyWallpaper(WallpaperManager.FLAG_SYSTEM));
        findViewById(R.id.lockWallpaper).setOnClickListener(v -> applyWallpaper(WallpaperManager.FLAG_LOCK));
        findViewById(R.id.bothWallpaper).setOnClickListener(v -> applyWallpaper(WallpaperManager.FLAG_SYSTEM | WallpaperManager.FLAG_LOCK));
        findViewById(R.id.addClock).setOnClickListener(v -> pinWidget(ZenClockWidget.class));
        findViewById(R.id.addQuote).setOnClickListener(v -> pinWidget(ZenQuoteWidget.class));
        findViewById(R.id.openThemePark).setOnClickListener(v -> openThemePark());
        findViewById(R.id.openFont).setOnClickListener(v -> safeStart(new Intent(Settings.ACTION_DISPLAY_SETTINGS)));
        findViewById(R.id.openLockSettings).setOnClickListener(v -> safeStart(new Intent(Settings.ACTION_SECURITY_SETTINGS)));
    }

    private void applyWallpaper(int flags) {
        try {
            WallpaperManager.getInstance(this).setBitmap(wallpaper, null, true, flags);
            toast("Forest Zen uygulandı");
        } catch (IOException | SecurityException e) {
            toast("Duvar kağıdı uygulanamadı: " + e.getMessage());
        }
    }

    private void pinWidget(Class<?> provider) {
        AppWidgetManager manager = AppWidgetManager.getInstance(this);
        if (!manager.isRequestPinAppWidgetSupported()) {
            toast("Ana ekrana basılı tut → Widget'lar → Forest Zen Studio");
            return;
        }
        manager.requestPinAppWidget(new ComponentName(this, provider), null, null);
    }

    private void openThemePark() {
        Intent intent = getPackageManager().getLaunchIntentForPackage("com.samsung.android.themedesigner");
        if (intent != null) startActivity(intent);
        else toast("Samsung Theme Park yüklü değil.");
    }

    private void safeStart(Intent intent) {
        try { startActivity(intent); }
        catch (Exception e) { toast("Bu ayar ekranı açılamadı."); }
    }

    private void toast(String message) {
        Toast.makeText(this, message, Toast.LENGTH_LONG).show();
    }

    private Bitmap createForestWallpaper(int w, int h) {
        Bitmap bitmap = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888);
        Canvas canvas = new Canvas(bitmap);
        Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);

        LinearGradient gradient = new LinearGradient(
            0, 0, 0, h,
            new int[]{Color.rgb(224,215,195), Color.rgb(163,174,145), Color.rgb(55,77,48)},
            null, Shader.TileMode.CLAMP
        );
        paint.setShader(gradient);
        canvas.drawRect(0, 0, w, h, paint);
        paint.setShader(null);

        paint.setColor(Color.argb(85,238,230,214));
        for (int y = 450; y < 1700; y += 240) canvas.drawOval(-250, y, w + 250, y + 330, paint);

        Path far = new Path();
        far.moveTo(0,2100);
        far.cubicTo(260,1780,520,1850,760,1650);
        far.cubicTo(1030,1420,1220,1780,w,1520);
        far.lineTo(w,h); far.lineTo(0,h); far.close();
        paint.setColor(Color.rgb(71,92,62));
        canvas.drawPath(far, paint);

        Path near = new Path();
        near.moveTo(0,2450);
        near.cubicTo(360,2170,710,2240,w,1900);
        near.lineTo(w,h); near.lineTo(0,h); near.close();
        paint.setColor(Color.rgb(38,57,35));
        canvas.drawPath(near, paint);

        paint.setColor(Color.argb(160,229,222,205));
        canvas.drawCircle(1120,410,160,paint);

        return bitmap;
    }
}
