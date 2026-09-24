from pathlib import Path
import sys

root = Path(sys.argv[1])
view = root / "android/app/src/main/kotlin/com/example/lyricstream/LyricOverlayView.kt"
settings = root / "android/app/src/main/kotlin/com/example/lyricstream/OverlaySettings.kt"

s = view.read_text()

s = s.replace(
    "drawLyricsState(c, theme, accent, left, right, contentW)",
    "drawLyricsState(c, theme, accent, accentB, left, right, contentW)",
)
s = s.replace(
    "private fun drawLyricsState(c: Canvas, theme: OverlayTheme, accent: Int, left: Float, right: Float, contentW: Float) {",
    "private fun drawLyricsState(c: Canvas, theme: OverlayTheme, accent: Int, accentB: Int, left: Float, right: Float, contentW: Float) {",
)

start = s.index("    private fun drawAuroraSurface(")
end = s.index("    private fun drawLyricsState(", start)

new_aurora = r'''    private fun drawAuroraSurface(c: Canvas, outer: RectF, accent: Int, accentB: Int, alphaScale: Float) {
        val intensity = settings.auroraIntensity.coerceIn(.15f, 1f)
        val moving = !settings.reduceMotion && settings.performanceMode != PerformanceMode.ECO
        val time = if (moving) SystemClock.uptimeMillis() / 1000f else 0f
        val accentC = auroraThirdAccent(accent, accentB)
        val longRadius = max(width, height) * .82f
        val shortRadius = max(width, height) * .42f

        // Aurora v7: no hard card. A subtle ink veil protects readability while the
        // colored light itself stays visibly separated from the game underneath.
        bg.shader = RadialGradient(
            width * .50f, height * .52f, max(width, height) * .66f,
            intArrayOf(
                withAlpha(Color.BLACK, (118 * alphaScale).toInt()),
                withAlpha(Color.BLACK, (58 * alphaScale).toInt()),
                Color.TRANSPARENT
            ),
            floatArrayOf(0f, .48f, 1f),
            Shader.TileMode.CLAMP
        )
        c.drawRect(outer, bg)

        val x1 = width * (.18f + .12f * sin(time * .73f))
        val y1 = height * (.48f + .20f * cos(time * .61f))
        val x2 = width * (.72f + .13f * cos(time * .57f + 1.1f))
        val y2 = height * (.50f + .21f * sin(time * .67f + .8f))
        val x3 = width * (.50f + .21f * sin(time * .41f + 2.2f))
        val y3 = height * (.30f + .13f * cos(time * .83f + .3f))

        fun orb(x: Float, y: Float, radius: Float, color: Int, power: Int) {
            bg.shader = RadialGradient(
                x, y, radius,
                intArrayOf(
                    withAlpha(Color.WHITE, (power * .24f * intensity * alphaScale).toInt()),
                    withAlpha(color, (power * intensity * alphaScale).toInt()),
                    withAlpha(color, (power * .34f * intensity * alphaScale).toInt()),
                    Color.TRANSPARENT,
                ),
                floatArrayOf(0f, .12f, .42f, 1f),
                Shader.TileMode.CLAMP
            )
            c.drawRect(outer, bg)
        }

        orb(x1, y1, longRadius, accent, 196)
        orb(x2, y2, longRadius * .90f, accentB, 174)
        orb(x3, y3, shortRadius, accentC, 142)

        // Curved aurora ribbon A.
        val pathA = Path().apply {
            moveTo(-dp(24f), height * (.57f + .07f * sin(time * .52f)))
            cubicTo(
                width * .25f, height * (.18f + .08f * cos(time * .64f)),
                width * .62f, height * (.88f + .06f * sin(time * .44f)),
                width + dp(26f), height * (.36f + .08f * cos(time * .58f))
            )
        }
        linePaint.style = Paint.Style.STROKE
        linePaint.strokeCap = Paint.Cap.ROUND
        linePaint.strokeJoin = Paint.Join.ROUND
        linePaint.strokeWidth = dp(if (height < dp(100f)) 17f else 23f)
        linePaint.shader = LinearGradient(
            0f, 0f, width.toFloat(), height.toFloat(),
            intArrayOf(
                Color.TRANSPARENT,
                withAlpha(accent, (96 * intensity * alphaScale).toInt()),
                withAlpha(accentB, (118 * intensity * alphaScale).toInt()),
                Color.TRANSPARENT
            ),
            floatArrayOf(0f, .28f, .72f, 1f),
            Shader.TileMode.CLAMP
        )
        c.drawPath(pathA, linePaint)

        // Curved aurora ribbon B.
        val pathB = Path().apply {
            moveTo(-dp(18f), height * (.22f + .05f * cos(time * .48f)))
            cubicTo(
                width * .30f, height * (.78f + .05f * sin(time * .56f)),
                width * .70f, height * (.04f + .08f * cos(time * .51f)),
                width + dp(20f), height * (.67f + .05f * sin(time * .62f))
            )
        }
        linePaint.strokeWidth = dp(if (height < dp(100f)) 9f else 13f)
        linePaint.shader = LinearGradient(
            0f, height.toFloat(), width.toFloat(), 0f,
            intArrayOf(
                Color.TRANSPARENT,
                withAlpha(accentC, (80 * intensity * alphaScale).toInt()),
                withAlpha(accent, (74 * intensity * alphaScale).toInt()),
                Color.TRANSPARENT
            ),
            floatArrayOf(0f, .25f, .75f, 1f),
            Shader.TileMode.CLAMP
        )
        c.drawPath(pathB, linePaint)

        // Narrow moving glint so the motion is actually perceptible in-game.
        val travel = if (moving) ((time * .20f) % 1f) else .52f
        val sweepX = width * (-.16f + travel * 1.32f)
        bg.shader = LinearGradient(
            sweepX - dp(54f), 0f, sweepX + dp(54f), 0f,
            intArrayOf(
                Color.TRANSPARENT,
                withAlpha(accentC, (26 * intensity).toInt()),
                withAlpha(Color.WHITE, (105 * intensity * alphaScale).toInt()),
                withAlpha(accent, (35 * intensity).toInt()),
                Color.TRANSPARENT
            ),
            floatArrayOf(0f, .31f, .50f, .69f, 1f),
            Shader.TileMode.CLAMP
        )
        c.drawRect(outer, bg)

        linePaint.shader = null
        linePaint.style = Paint.Style.FILL
        bg.shader = null
        if (moving) postInvalidateDelayed(if (settings.performanceMode == PerformanceMode.ULTRA) 32L else 48L)
    }

    private fun drawLyricBloom(
        c: Canvas,
        left: Float,
        top: Float,
        right: Float,
        bottom: Float,
        accent: Int,
        accentB: Int
    ) {
        if (!settings.glowEnabled || settings.hudSkin != HudSkin.AURORA || settings.highContrast) return
        val intensity = settings.auroraIntensity.coerceIn(.15f, 1f)
        val moving = !settings.reduceMotion && settings.performanceMode != PerformanceMode.ECO
        val time = if (moving) SystemClock.uptimeMillis() / 1000f else 0f
        val h = (bottom - top).coerceAtLeast(dp(24f))
        val w = (right - left).coerceAtLeast(dp(80f))
        val x = left + w * (.36f + .10f * sin(time * .91f))
        val y = top + h * (.50f + .08f * cos(time * .77f))
        val radius = max(w * .58f, h * 2.5f)

        bg.shader = RadialGradient(
            x, y, radius,
            intArrayOf(
                withAlpha(Color.WHITE, (34 * intensity * pausedDim).toInt()),
                withAlpha(accent, (128 * intensity * pausedDim).toInt()),
                withAlpha(accentB, (58 * intensity * pausedDim).toInt()),
                Color.TRANSPARENT,
            ),
            floatArrayOf(0f, .18f, .48f, 1f),
            Shader.TileMode.CLAMP
        )
        c.drawRect(left - dp(18f), top - dp(12f), right + dp(18f), bottom + dp(14f), bg)
        bg.shader = null
    }

'''

s = s[:start] + new_aurora + s[end:]

old_shadow = '''        if (settings.glowEnabled && (settings.hudSkin == HudSkin.AURORA || settings.hudSkin == HudSkin.RIBBON)) {
            activePaint.setShadowLayer(dp(8f), 0f, 0f, withAlpha(accent, 128))
        } else {
'''
new_shadow = '''        if (settings.glowEnabled && (settings.hudSkin == HudSkin.AURORA || settings.hudSkin == HudSkin.RIBBON)) {
            val haloRadius = if (settings.hudSkin == HudSkin.AURORA) 11.5f else 8f
            val haloAlpha = if (settings.hudSkin == HudSkin.AURORA) 188 else 128
            activePaint.setShadowLayer(dp(haloRadius), 0f, 0f, withAlpha(accent, haloAlpha))
        } else {
'''
if old_shadow not in s:
    raise SystemExit("shadow block not found")
s = s.replace(old_shadow, new_shadow, 1)

layout_block = '''        val layout = makeFittedLayout(
            line.text,
            activePaint,
            contentW.toInt(),
            maxLines = maxLines,
            maxHeightPx = availableHeight,
            minTextSizePx = sp(10.6f),
            align = Layout.Alignment.ALIGN_NORMAL,
        )

        c.save()
'''
layout_replacement = '''        val layout = makeFittedLayout(
            line.text,
            activePaint,
            contentW.toInt(),
            maxLines = maxLines,
            maxHeightPx = availableHeight,
            minTextSizePx = sp(10.6f),
            align = Layout.Alignment.ALIGN_NORMAL,
        )

        drawLyricBloom(c, left, textY, right, textY + layout.height, accent, accentB)

        c.save()
'''
if layout_block not in s:
    raise SystemExit("layout block not found")
s = s.replace(layout_block, layout_replacement, 1)

blend_marker = '''    private fun blend(a: Int, b: Int, t: Float): Int {
'''
helper = '''    private fun auroraThirdAccent(accent: Int, fallback: Int): Int {
        val hsv = FloatArray(3); Color.colorToHSV(accent, hsv)
        if (hsv[1] < .20f) return fallback
        hsv[0] = (hsv[0] + 132f) % 360f
        hsv[1] = (hsv[1] * .92f).coerceIn(.52f, .94f)
        hsv[2] = .99f
        return Color.HSVToColor(hsv)
    }

'''
if blend_marker not in s:
    raise SystemExit("blend marker not found")
s = s.replace(blend_marker, helper + blend_marker, 1)

view.write_text(s)

q = settings.read_text()
q = q.replace("val auroraIntensity: Float = .88f,", "val auroraIntensity: Float = 1.0f,")
q = q.replace("if (visualVersion < 6) {", "if (visualVersion < 7) {")
q = q.replace('putInt("visualUpgradeVersion", 6)', 'putInt("visualUpgradeVersion", 7)')
q = q.replace('editor.putFloat("auroraIntensity", .88f)', 'editor.putFloat("auroraIntensity", 1.0f)')
q = q.replace(
    'prefs.getFloat("auroraIntensity", .88f).coerceIn(0f, 1f)',
    'prefs.getFloat("auroraIntensity", 1.0f).coerceIn(0f, 1f)'
)

marker = '''            editor.putBoolean("panelEnabled", true)
            editor.putBoolean("showUnlockHandle", true)
'''
replacement = '''            if (currentSkin == HudSkin.AURORA.name) {
                editor.putFloat("auroraIntensity", 1.0f)
                editor.putBoolean("glowEnabled", true)
                editor.putString("adaptiveThemeMode", AdaptiveThemeMode.FULL.name)
            }

            editor.putBoolean("panelEnabled", true)
            editor.putBoolean("showUnlockHandle", true)
'''
if marker not in q:
    raise SystemExit("settings migration marker not found")
q = q.replace(marker, replacement, 1)
settings.write_text(q)
