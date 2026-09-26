from pathlib import Path
import sys

root = Path(sys.argv[1])

# Flutter app: floating minimal glass nav with a moving active capsule.
main = root / 'lib/main.dart'
s = main.read_text()
old = """  Widget _bottomNav() => Padding(
        padding: const EdgeInsets.fromLTRB(14, 4, 14, 12),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(26),
          child: BackdropFilter(
            filter: ImageFilter.blur(sigmaX: 18, sigmaY: 18),
            child: Container(
              padding: const EdgeInsets.all(5),
              decoration: BoxDecoration(color: Theme.of(context).colorScheme.surface.withValues(alpha: .78), border: Border.all(color: Colors.white.withValues(alpha: .08)), borderRadius: BorderRadius.circular(26)),
              child: Row(children: [
                _navItem(Icons.home_rounded, 'Home', 0),
                _navItem(Icons.tune_rounded, 'Studio', 1),
                _navItem(Icons.sync_rounded, 'Sync', 2),
                _navItem(Icons.storefront_rounded, 'Store', 3),
                _navItem(Icons.settings_rounded, 'Settings', 4),
              ]),
            ),
          ),
        ),
      );

  Widget _navItem(IconData icon, String label, int index) => Expanded(child: SpringPress(
        onTap: () => setState(() => tab = index),
        child: Semantics(
          selected: tab == index,
          button: true,
          label: label,
          child: Container(
            height: 52,
            decoration: BoxDecoration(borderRadius: BorderRadius.circular(20), gradient: tab == index ? LinearGradient(colors: [Theme.of(context).colorScheme.primary.withValues(alpha: .2), Theme.of(context).colorScheme.secondary.withValues(alpha: .15)]) : null),
            child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [Icon(icon, size: 20, color: tab == index ? Theme.of(context).colorScheme.primary : null), const SizedBox(height: 2), Text(label, style: TextStyle(fontSize: 9.5, fontWeight: tab == index ? FontWeight.w800 : FontWeight.w500))]),
          ),
        ),
      ));
"""
new = """  Widget _bottomNav() {
    final scheme = Theme.of(context).colorScheme;
    final surface = scheme.surface;
    return Padding(
      padding: const EdgeInsets.fromLTRB(18, 2, 18, 14),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(30),
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 26, sigmaY: 26),
          child: Container(
            height: 64,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(30),
              gradient: LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [
                  surface.withValues(alpha: widget.dark ? .62 : .78),
                  surface.withValues(alpha: widget.dark ? .38 : .58),
                ],
              ),
              border: Border.all(color: Colors.white.withValues(alpha: widget.dark ? .10 : .22), width: .8),
              boxShadow: [
                BoxShadow(color: Colors.black.withValues(alpha: widget.dark ? .28 : .10), blurRadius: 28, offset: const Offset(0, 12)),
                BoxShadow(color: scheme.primary.withValues(alpha: .055), blurRadius: 26, spreadRadius: -6),
              ],
            ),
            child: LayoutBuilder(builder: (context, constraints) {
              final itemWidth = constraints.maxWidth / 5;
              return Stack(
                alignment: Alignment.center,
                children: [
                  AnimatedPositioned(
                    duration: const Duration(milliseconds: 360),
                    curve: Curves.easeOutBack,
                    left: itemWidth * tab + 4,
                    top: 5,
                    bottom: 5,
                    width: itemWidth - 8,
                    child: Container(
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(24),
                        gradient: LinearGradient(
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                          colors: [
                            Colors.white.withValues(alpha: widget.dark ? .095 : .42),
                            scheme.primary.withValues(alpha: widget.dark ? .17 : .13),
                            scheme.secondary.withValues(alpha: widget.dark ? .09 : .08),
                          ],
                        ),
                        border: Border.all(color: Colors.white.withValues(alpha: widget.dark ? .11 : .34), width: .75),
                        boxShadow: [
                          BoxShadow(color: scheme.primary.withValues(alpha: .16), blurRadius: 22, spreadRadius: -7),
                        ],
                      ),
                    ),
                  ),
                  Row(children: [
                    _navItem(Icons.home_rounded, 'Home', 0),
                    _navItem(Icons.tune_rounded, 'Studio', 1),
                    _navItem(Icons.sync_rounded, 'Sync', 2),
                    _navItem(Icons.storefront_rounded, 'Store', 3),
                    _navItem(Icons.settings_rounded, 'Settings', 4),
                  ]),
                ],
              );
            }),
          ),
        ),
      ),
    );
  }

  Widget _navItem(IconData icon, String label, int index) {
    final selected = tab == index;
    final scheme = Theme.of(context).colorScheme;
    return Expanded(
      child: SpringPress(
        onTap: () => setState(() => tab = index),
        child: Semantics(
          selected: selected,
          button: true,
          label: label,
          child: SizedBox.expand(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                AnimatedScale(
                  scale: selected ? 1.06 : .96,
                  duration: const Duration(milliseconds: 280),
                  curve: Curves.easeOutBack,
                  child: Icon(
                    icon,
                    size: selected ? 21 : 20,
                    color: selected ? scheme.onSurface : scheme.onSurface.withValues(alpha: .62),
                  ),
                ),
                AnimatedSize(
                  duration: const Duration(milliseconds: 260),
                  curve: Curves.easeOutCubic,
                  child: selected
                      ? Padding(
                          padding: const EdgeInsets.only(top: 2),
                          child: Text(
                            label,
                            maxLines: 1,
                            overflow: TextOverflow.fade,
                            style: TextStyle(fontSize: 9.2, height: 1, fontWeight: FontWeight.w800, color: scheme.onSurface.withValues(alpha: .96)),
                          ),
                        )
                      : const SizedBox(height: 0),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
"""
if old not in s:
    raise SystemExit('v9 navbar source marker not found')
s = s.replace(old, new, 1)
main.write_text(s)

# Native HUD: organic readability field, lyric entrance motion and premium timeline.
view = root / 'android/app/src/main/kotlin/com/example/lyricstream/LyricOverlayView.kt'
k = view.read_text()
k = k.replace('    private var lyricPulseAtMs = 0L\n', '    private var lyricPulseAtMs = 0L\n    private var lyricChangedAtMs = 0L\n', 1)
marker = '''    private fun drawLyricsState(c: Canvas, theme: OverlayTheme, accent: Int, accentB: Int, left: Float, right: Float, contentW: Float) {\n'''
helper = r'''    private fun drawReadabilityField(c: Canvas, left: Float, top: Float, right: Float, bottom: Float, accent: Int, accentB: Int) {
        if (settings.highContrast) return
        val padX = dp(14f)
        val padY = dp(9f)
        val l = (left - padX).coerceAtLeast(0f)
        val r = (right + padX).coerceAtMost(width.toFloat())
        val t = (top - padY).coerceAtLeast(0f)
        val b = (bottom + padY).coerceAtMost(height.toFloat())
        val darkAlpha = when (settings.hudSkin) {
            HudSkin.PURE_TEXT -> 116
            HudSkin.AURORA -> 88
            HudSkin.RIBBON -> 72
            else -> 52
        }
        val cx = left + (right - left) * .43f
        val cy = top + (bottom - top) * .52f
        val radius = max((r - l) * .72f, (b - t) * 2.2f)
        bg.shader = RadialGradient(
            cx, cy, radius,
            intArrayOf(
                Color.argb((darkAlpha * pausedDim).toInt().coerceIn(0,255), 3, 5, 9),
                Color.argb((darkAlpha * .58f * pausedDim).toInt().coerceIn(0,255), 3, 5, 9),
                Color.TRANSPARENT,
            ),
            floatArrayOf(0f, .44f, 1f),
            Shader.TileMode.CLAMP
        )
        c.drawRect(l, t, r, b, bg)
        bg.shader = null

        linePaint.strokeCap = Paint.Cap.ROUND
        linePaint.strokeWidth = dp(2.2f)
        linePaint.shader = LinearGradient(0f, t, 0f, b, withAlpha(a, 225), withAlpha(b, 70), Shader.TileMode.CLAMP)
        c.drawLine(left - dp(8f), t + dp(7f), left - dp(8f), b - dp(7f), linePaint)
        linePaint.shader = null
    }

    private fun lyricEnterProgress(): Float {
        if (settings.reduceMotion || lyricChangedAtMs <= 0L) return 1f
        val age = (SystemClock.elapsedRealtime() - lyricChangedAtMs).coerceAtLeast(0L)
        if (age >= 420L) return 1f
        val t = (age / 420f).coerceIn(0f, 1f)
        return 1f - (1f - t) * (1f - t)
    }

'''
if marker not in k:
    raise SystemExit('v9 lyric marker not found')
k = k.replace(marker, helper + marker, 1)
old = '''        drawLyricBloom(c, left, textY, right, textY + layout.height, accent, accentB)

        c.save()
        c.translate(left, textY)
        c.scale(activeScale, activeScale, 0f, 0f)
        layout.draw(c)
'''
new = '''        drawReadabilityField(c, left, textY, right, textY + layout.height, accent, accentB)
        drawLyricBloom(c, left, textY, right, textY + layout.height, accent, accentB)

        val enter = lyricEnterProgress()
        c.save()
        c.translate(left + dp((1f - enter) * 7f), textY + dp((1f - enter) * 3f))
        c.scale(activeScale, activeScale, 0f, 0f)
        layout.draw(c)
'''
if old not in k:
    raise SystemExit('v9 lyric draw marker not found')
k = k.replace(old, new, 1)
old = '''        activeIndex = idx
        if (settings.reactiveLight) lyricPulseAtMs = SystemClock.elapsedRealtime()
'''
new = '''        activeIndex = idx
        lyricChangedAtMs = SystemClock.elapsedRealtime()
        if (settings.reactiveLight) lyricPulseAtMs = lyricChangedAtMs
'''
if old not in k:
    raise SystemExit('v9 active-index marker not found')
k = k.replace(old, new, 1)
old = '''        linePaint.strokeCap = Paint.Cap.ROUND
        linePaint.strokeWidth = dp(2.2f)
        linePaint.color = withAlpha(if (settings.darkMode) Color.WHITE else Color.BLACK, 34)
        c.drawLine(left, y, right, y, linePaint)
        linePaint.shader = LinearGradient(left, 0f, right, 0f, accent, accentB, Shader.TileMode.CLAMP)
        c.drawLine(left, y, left + (right - left) * progress, y, linePaint)
        linePaint.shader = null
'''
new = '''        linePaint.strokeCap = Paint.Cap.ROUND
        linePaint.strokeWidth = dp(1.35f)
        linePaint.color = withAlpha(if (settings.darkMode) Color.WHITE else Color.BLACK, 28)
        c.drawLine(left, y, right, y, linePaint)
        linePaint.strokeWidth = dp(1.8f)
        linePaint.shader = LinearGradient(left, 0f, right, 0f, accent, accentB, Shader.TileMode.CLAMP)
        val headX = left + (right - left) * progress
        c.drawLine(left, y, headX, y, linePaint)
        linePaint.shader = null
        bg.color = withAlpha(Color.WHITE, 220)
        c.drawCircle(headX, y, dp(2.3f), bg)
        bg.color = withAlpha(accent, 72)
        c.drawCircle(headX, y, dp(5.2f), bg)
'''
if old not in k:
    raise SystemExit('v9 progress marker not found')
k = k.replace(old, new, 1)
view.write_text(k)

# In-game control center: compact frosted sheet instead of a heavy black card.
panel = root / 'android/app/src/main/kotlin/com/example/lyricstream/InGameControlCenterView.kt'
p = panel.read_text()
old = '''        val outer = RectF(dp(1f), dp(1f), width - dp(1f), height - dp(1f))
        bg.color = Color.argb(238, 6, 8, 13)
        c.drawRoundRect(outer, dp(26f), dp(26f), bg)
        stroke.strokeWidth = dp(1f)
        stroke.shader = LinearGradient(0f, 0f, width.toFloat(), height.toFloat(), withAlpha(a, 190), withAlpha(b, 60), Shader.TileMode.CLAMP)
        c.drawRoundRect(outer, dp(26f), dp(26f), stroke)
        stroke.shader = null

        text.color = Color.WHITE; text.textSize = sp(14.5f)
        c.drawText("GAME CONTROL", dp(18f), dp(27f), text)
        sub.color = withAlpha(Color.WHITE, 112); sub.textSize = sp(8.4f)
        c.drawText("LIVE HUD • PASS-THROUGH SAFE", dp(18f), dp(41f), sub)
'''
new = '''        val outer = RectF(dp(1f), dp(1f), width - dp(1f), height - dp(1f))
        bg.shader = LinearGradient(
            0f, 0f, width.toFloat(), height.toFloat(),
            intArrayOf(Color.argb(222, 7, 9, 14), Color.argb(206, 12, 14, 22), Color.argb(220, 6, 8, 13)),
            null, Shader.TileMode.CLAMP
        )
        c.drawRoundRect(outer, dp(28f), dp(28f), bg)
        bg.shader = RadialGradient(width * .18f, height * .10f, width * .72f, withAlpha(a, 42), Color.TRANSPARENT, Shader.TileMode.CLAMP)
        c.drawRoundRect(outer, dp(28f), dp(28f), bg)
        bg.shader = RadialGradient(width * .82f, height * .18f, width * .68f, withAlpha(b, 30), Color.TRANSPARENT, Shader.TileMode.CLAMP)
        c.drawRoundRect(outer, dp(28f), dp(28f), bg)
        bg.shader = null
        stroke.strokeWidth = dp(.85f)
        stroke.shader = LinearGradient(0f, 0f, width.toFloat(), height.toFloat(), withAlpha(Color.WHITE, 82), withAlpha(a, 62), Shader.TileMode.CLAMP)
        c.drawRoundRect(outer, dp(28f), dp(28f), stroke)
        stroke.shader = null

        text.color = Color.WHITE; text.textSize = sp(13.8f)
        c.drawText("LYRICSTREAM", dp(18f), dp(25f), text)
        sub.color = withAlpha(Color.WHITE, 106); sub.textSize = sp(8.0f)
        c.drawText("GAME HUD CONTROL", dp(18f), dp(39f), sub)
'''
if old not in p:
    raise SystemExit('v9 panel header marker not found')
p = p.replace(old, new, 1)
old = '''        bg.color = if (selected) withAlpha(accent, 52) else Color.argb(178, 18, 22, 31)
        c.drawRoundRect(r, dp(13f), dp(13f), bg)
        stroke.style = Paint.Style.STROKE; stroke.strokeWidth = dp(if (selected) 1.35f else .8f)
        stroke.color = if (selected) withAlpha(accent, 220) else Color.argb(45,255,255,255)
        c.drawRoundRect(r, dp(13f), dp(13f), stroke)
'''
new = '''        bg.color = if (selected) withAlpha(accent, 44) else Color.argb(118, 255, 255, 255)
        c.drawRoundRect(r, dp(15f), dp(15f), bg)
        stroke.style = Paint.Style.STROKE; stroke.strokeWidth = dp(if (selected) 1.15f else .7f)
        stroke.color = if (selected) withAlpha(accent, 190) else Color.argb(38,255,255,255)
        c.drawRoundRect(r, dp(15f), dp(15f), stroke)
'''
if old not in p:
    raise SystemExit('v9 panel button marker not found')
p = p.replace(old, new, 1)
panel.write_text(p)

# Smaller edge dock.
dock = root / 'android/app/src/main/kotlin/com/example/lyricstream/EdgeDockView.kt'
d = dock.read_text()
d = d.replace('''        p.color = Color.argb(190, 7, 9, 14)
        c.drawRoundRect(rect, dp(14f), dp(14f), p)
''', '''        p.color = Color.argb(152, 7, 9, 14)
        c.drawRoundRect(rect, dp(13f), dp(13f), p)
''', 1)
d = d.replace('''        p.color = Color.argb(208, 7, 9, 14)
        c.drawRoundRect(RectF(dp(7f), dp(9f), width - dp(7f), height - dp(9f)), dp(9f), dp(9f), p)

        line.strokeWidth = dp(2.1f)
''', '''        p.color = Color.argb(176, 7, 9, 14)
        c.drawRoundRect(RectF(dp(6f), dp(8f), width - dp(6f), height - dp(8f)), dp(9f), dp(9f), p)

        line.strokeWidth = dp(1.7f)
''', 1)
d = d.replace('c.drawLine(cx, cy - dp(12f), cx, cy + dp(12f), line)', 'c.drawLine(cx, cy - dp(9f), cx, cy + dp(9f), line)', 1)
d = d.replace('c.drawPoint(cx, cy - dp(20f), line)', 'c.drawPoint(cx, cy - dp(16f), line)', 1)
d = d.replace('c.drawPoint(cx, cy + dp(20f), line)', 'c.drawPoint(cx, cy + dp(16f), line)', 1)
dock.write_text(d)

# Service: smaller dock/panel and real window blur for the in-game sheet when supported.
svc = root / 'android/app/src/main/kotlin/com/example/lyricstream/OverlayService.kt'
o = svc.read_text()
o = o.replace('dp(28), dp(82), WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,', 'dp(24), dp(68), WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,', 1)
o = o.replace('dp(336), dp(338), WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,', 'dp(328), dp(330), WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,', 1)
old = '''        panelView = view
        panelParams = p
        updateControlCenterPosition()
        wm.addView(view, p)
'''
new = '''        panelView = view
        panelParams = p
        configureBlur(p)
        updateControlCenterPosition()
        wm.addView(view, p)
'''
if old not in o:
    raise SystemExit('v9 service panel marker not found')
o = o.replace(old, new, 1)
svc.write_text(o)

pub = root / 'pubspec.yaml'
q = pub.read_text()
if 'version: 0.8.0+8' not in q:
    raise SystemExit('v9 version marker not found')
pub.write_text(q.replace('version: 0.8.0+8', 'version: 0.9.0+9', 1))
