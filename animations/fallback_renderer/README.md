# Fallback renderer

A small stand-in for Manim that runs the scenes in this folder unchanged. It covers only the subset of Manim they use, with the same layout rules, bundled fonts, palette, line weights, easing and timing. Use it when Manim, Cairo or Pango cannot be installed. It needs only Pillow, NumPy and ffmpeg.

```bash
cd animations/fallback_renderer
MINI_FONTDIR=../fonts MINI_SS=3 THEME=light python render.py .. investor_scenes AIPipeline out.mp4
```

Checked against a real Manim render of Fig. 4 (`Triage`): the layout matches, and edges are slightly softer. Figures 7 and 8 in `media/` were made with this renderer. Re-running `../render_all.sh AIPipeline SpecialtyReuse` with Manim produces the same figures through the original pipeline.
