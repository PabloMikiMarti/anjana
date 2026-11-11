# Anjana site animations (Manim)

Source for the animated figures on the Anjana site. Every MP4 and JPEG poster in `../media/` is generated from this folder.

| Scene | File | Site file | What it shows |
|---|---|---|---|
| Flow | scenes.py | hero-*.mp4 | Hero loop: dossiers → two AI readers → three lanes (1920×820, seamless 10 s loop) |
| Committee | scenes.py | fig1-*.mp4 | Fig. 1, how events are adjudicated today |
| TwoReaders | scenes.py | fig2-*.mp4 | Fig. 2, the committee's logic with two AI readers |
| Evidence | scenes.py | fig3-*.mp4 | Fig. 3, criterion-level evidence (synthetic record) |
| Triage | scenes.py | fig4-*.mp4 | Fig. 4, DELIVER triage by AI score |
| Forest | scenes.py | fig5-*.mp4 | Fig. 5, hazard ratios, committee vs AI |
| App | scenes.py | fig6-*.mp4 | Fig. 6, sketch of the Anjana adjudicator workflow (synthetic case) |
| AIPipeline | investor_scenes.py | fig7-*.mp4 | Fig. 7, AI-enabled drugs entering trials, Phase I success, and the adjudication they lead to |
| SpecialtyReuse | investor_scenes.py | fig8-*.mp4 | Fig. 8, one engine with swappable endpoint definitions across specialties |

## Setup
- Python 3.10+ and Manim Community (`pip install -r requirements.txt`). Manim needs Cairo, Pango and ffmpeg (on macOS: `brew install cairo pango ffmpeg`).
- Fonts are bundled in `fonts/` and registered by `style.py` at render time, so nothing needs installing. They are IBM Plex Sans (labels and body), Newsreader (fallback glyphs) and `SdMManim-Regular.ttf`.
- `SdMManim-Regular.ttf` is Serif de Muestra plus the glyphs it lacks. Rebuild it with `build_sdm_font.py` if the font changes.

## Render
- Everything, both themes, straight into `../media/`: `./render_all.sh`
- Only some scenes: `./render_all.sh AIPipeline SpecialtyReuse`
- Quick preview of one scene: `PREVIEW=1 THEME=light manim render scenes.py Committee`
- `THEME` = `light` | `dark` (colors in `style.py` match the site's tokens). `HERO=1` switches to the 1920×820 hero frame.

## Editing
- `style.py`: palette, fonts, icons, `label()` / `under()` / `over()` (baseline-aligned labels), and the numbered caption narrator.
- Data in figures 1–6 comes from the published papers (Circ Heart Fail 2025; JACC 2025). Fig. 4 category sizes are rounded to whole percentages.
- Every number in figures 7–8 is sourced in `../docs/investor-evidence.md`. Patient fields, event dots and lanes are illustrative.
