"""Builds fonts/SdMManim-Regular.ttf: Serif de Muestra plus the glyphs it lacks
(%, en dash, middle dot, ellipsis, arrows, kappa...) borrowed from Newsreader and
scaled to match its cap height. Manim needs this because Pango's per-glyph fallback
puts borrowed glyphs off the baseline. Usage:
  python build_sdm_font.py Serif-de-Muestra-Regular.ttf fonts/newsreader-400-normal.ttf fonts/SdMManim-Regular.ttf
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import DecomposingRecordingPen

src, donor, out = sys.argv[1:4]
a, b = TTFont(src), TTFont(donor)
k = (a["head"].unitsPerEm / b["head"].unitsPerEm) * (a["OS/2"].sCapHeight / (b["OS/2"].sCapHeight * a["head"].unitsPerEm / b["head"].unitsPerEm))
bcm, acm, bgs = b.getBestCmap(), a.getBestCmap(), b.getGlyphSet()
a["glyf"]; a.getGlyphOrder()
for ch in "%–·…≈→←−¢↗‹›κ":
    cp = ord(ch)
    if cp in acm or cp not in bcm:
        continue
    g_src = bcm[cp]; name = "m_" + g_src
    rec = DecomposingRecordingPen(bgs); bgs[g_src].draw(rec)
    pen = TTGlyphPen(None); rec.replay(TransformPen(pen, (k, 0, 0, k, 0, 0)))
    g = pen.glyph(); a["glyf"][name] = g; g.recalcBounds(a["glyf"])
    a["hmtx"][name] = (int(round(b["hmtx"][g_src][0] * k)), getattr(g, "xMin", 0) or 0)
    for t in a["cmap"].tables:
        if t.isUnicode():
            t.cmap[cp] = name
go = list(a["glyf"].glyphOrder); a.setGlyphOrder(go); a["glyf"].glyphOrder = go
for r in a["name"].names:
    if r.nameID in (1, 4, 16): r.string = "SdM Manim"
    if r.nameID == 6: r.string = "SdMManim-Regular"
a.save(out)
