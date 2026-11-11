"""Editorial animation system v2: thin strokes, uniform stations, narrated beats."""
import os
import numpy as np
from manim import *

# Register the bundled fonts for this render process, so no system install is needed.
# Fonts already installed system-wide keep working if registration is unavailable.
try:
    import manimpango
    _fonts = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
    for _f in sorted(os.listdir(_fonts)):
        if _f.endswith(".ttf"):
            manimpango.register_font(os.path.join(_fonts, _f))
except Exception:
    pass

THEME = os.environ.get("THEME", "light")
PALETTES = {
    "light": dict(plate="#E9ECE6", ink="#121A21", muted="#5D6871", rule="#BCC3BA",
                  accent="#B3262E", amber="#B87806", soft="#F7F8F5", faint="#DCE0D9", wash="#EBDDBD", redact="#121A21"),
    "dark": dict(plate="#151B20", ink="#E6EAE5", muted="#93A0A8", rule="#3A454C",
                 accent="#EE5A5F", amber="#E3A63B", soft="#1C242A", faint="#26313A", wash="#4A3D22", redact="#06090B"),
}
P = PALETTES[THEME]

config.background_color = P["plate"]
_scale = 0.5 if os.environ.get("PREVIEW") else 1.0
config.pixel_width = int(1920 * _scale)
config.pixel_height = int((820 if os.environ.get("HERO") else 1080) * _scale)
config.frame_rate = 10 if os.environ.get("PREVIEW") else 24
config.frame_height = config.frame_width * config.pixel_height / config.pixel_width

SANS, SERIF, MONO = "IBM Plex Sans", "SdM Manim", "IBM Plex Sans"  # labels use the sans; no monospace
SERIF_FALLBACK = "Newsreader 16pt 16pt"
_MISSING = set()
LW = 2.0          # line weight
EASE = rate_functions.ease_in_out_cubic


def T(s, size=24, color=None, font=SANS, weight=NORMAL, slant=NORMAL):
    t2f = {ch: SERIF_FALLBACK for ch in set(s) & _MISSING} if font == SERIF else None
    if font == SERIF:
        slant = NORMAL  # the supplied face has no italic; never synthesize one
    return Text(s, font=font, font_size=size, color=color or P["ink"], weight=weight,
                slant=slant, disable_ligatures=True, t2f=t2f)


def serif(s, size=36, color=None, slant=NORMAL):
    return T(s, size, color, SERIF, NORMAL, slant)


def mono(s, size=17, color=None, weight=MEDIUM):
    return T(s, size, color or P["muted"], MONO, weight)


def kicker(s):
    t = mono(s.upper(), 17)
    dash = Line(ORIGIN, RIGHT * 0.42, stroke_width=1.4, color=P["muted"])
    g = VGroup(dash, t).arrange(RIGHT, buff=0.18)
    g.to_corner(UL, buff=0.5)
    return g


def baseline_y(t):
    """Baseline y of a Text: bottom of its first glyph that has no descender."""
    chars = [c for c in getattr(t, "text", "") if not c.isspace()]
    for i, c in enumerate(chars[:len(t)]):
        if c not in "gjpqy,;()/":
            return t[i].get_bottom()[1]
    return t[0].get_bottom()[1]


def label(title, sub=None, tsize=23, ssize=18, align=ORIGIN):
    """Title + optional one-line sub, positioned by baselines so every label in a row lines up."""
    t = T(title, tsize, weight=MEDIUM)
    if not sub:
        return VGroup(t)
    s = T(sub, ssize, P["muted"])
    s.shift([0, (baseline_y(t) - 0.34) - baseline_y(s), 0])
    if align is LEFT:
        s.shift([t.get_left()[0] - s.get_left()[0], 0, 0])
    else:
        s.set_x(t.get_x())
    return VGroup(t, s)


def under(mob, lab, gap=0.2):
    """Place a label below mob: title cap-height top sits `gap` below mob."""
    lab.set_x(mob.get_x())
    lab.shift([0, (mob.get_bottom()[1] - gap) - lab[0][0].get_top()[1], 0])
    return lab


def over(mob, lab, gap=0.2):
    """Place a label above mob: its last line's baseline sits `gap` + descender room above mob."""
    lab.set_x(mob.get_x())
    lab.shift([0, (mob.get_top()[1] + gap + 0.09) - baseline_y(lab[-1]), 0])
    return lab


# ---------------- narration ----------------
class Narrator:
    def __init__(self, scene, total, pos=None):
        self.scene, self.total, self.cur, self.n = scene, total, None, 0
        self.pos = pos if pos is not None else np.array([-6.62, -3.42, 0])

    def make(self, text):
        self.n += 1
        num = mono(f"{self.n:02d} / {self.total:02d}", 15)
        txt = serif(text, 30, P["ink"], ITALIC)
        g = VGroup(num, txt).arrange(RIGHT, buff=0.32, aligned_edge=DOWN)
        num.shift(UP * 0.04)
        g.move_to(self.pos, aligned_edge=LEFT)
        return g

    def say(self, text, rt=0.4):
        new = self.make(text)
        if self.cur is not None:
            self.scene.play(FadeOut(self.cur, shift=UP * 0.06), run_time=0.22)
        self.scene.play(FadeIn(new, shift=UP * 0.06), run_time=rt)
        self.cur = new

    def clear(self, rt=0.35):
        if self.cur is not None:
            self.scene.play(FadeOut(self.cur), run_time=rt)
            self.cur = None


# ---------------- line icons (fit in ~0.5 unit box) ----------------
def i_doc(s=0.5, c=None):
    c = c or P["ink"]
    w, h, f = s * 0.72, s * 0.92, s * 0.2
    body = Polygon((-w/2, h/2, 0), (w/2 - f, h/2, 0), (w/2, h/2 - f, 0), (w/2, -h/2, 0), (-w/2, -h/2, 0),
                   stroke_color=c, stroke_width=LW, fill_opacity=0)
    fold = VMobject(stroke_color=c, stroke_width=LW).set_points_as_corners(
        [(w/2 - f, h/2, 0), (w/2 - f, h/2 - f, 0), (w/2, h/2 - f, 0)])
    lines = VGroup(*[Line((-w/2 + 0.07, h/2 - 0.17 - k * 0.1, 0), (w/2 - 0.08 - (0.08 if k == 2 else 0), h/2 - 0.17 - k * 0.1, 0),
                          stroke_width=LW * 0.8, color=c) for k in range(4)])
    return VGroup(body, fold, lines)


def i_person(s=0.5, c=None, fill=False):
    c = c or P["ink"]
    head = Circle(radius=s * 0.17, stroke_color=c, stroke_width=LW, fill_color=c, fill_opacity=1 if fill else 0)
    head.shift(UP * s * 0.17)
    sh = Arc(radius=s * 0.3, start_angle=0, angle=PI, stroke_color=c, stroke_width=LW)
    sh.shift(DOWN * s * 0.3)
    base = Line(sh.get_start(), sh.get_end(), stroke_color=c, stroke_width=LW)
    return VGroup(head, sh, base)


def i_globe(s=0.5, c=None):
    c = c or P["ink"]
    r = s * 0.42
    g = VGroup(Circle(radius=r, stroke_color=c, stroke_width=LW),
               Ellipse(width=r, height=2 * r, stroke_color=c, stroke_width=LW * 0.8),
               Line(LEFT * r, RIGHT * r, stroke_color=c, stroke_width=LW * 0.8))
    return g


def i_db(s=0.5, c=None):
    c = c or P["ink"]
    w, h, eh = s * 0.7, s * 0.7, s * 0.2
    top = Ellipse(width=w, height=eh, stroke_color=c, stroke_width=LW).shift(UP * h / 2)
    l = Line((-w/2, h/2, 0), (-w/2, -h/2, 0), stroke_color=c, stroke_width=LW)
    r = Line((w/2, h/2, 0), (w/2, -h/2, 0), stroke_color=c, stroke_width=LW)
    b = Arc(radius=w/2, start_angle=PI, angle=PI, stroke_color=c, stroke_width=LW).stretch(eh / w, 1).shift(DOWN * h / 2)
    m = Arc(radius=w/2, start_angle=PI, angle=PI, stroke_color=c, stroke_width=LW * 0.8).stretch(eh / w, 1)
    return VGroup(top, l, r, b, m)


def i_table(s=0.5, c=None, chair=None):
    c = c or P["ink"]
    t = Circle(radius=s * 0.2, stroke_color=c, stroke_width=LW)
    seats = VGroup()
    for k in range(6):
        a = PI / 2 + k * TAU / 6
        d = Dot(np.array([np.cos(a), np.sin(a), 0]) * s * 0.36, radius=s * 0.055, color=c)
        seats.add(d)
    seats[0].set_color(chair or P["accent"])
    return VGroup(t, seats)


def i_quote(s=0.5, c=None):
    c = c or P["ink"]
    q = T("“”", int(46 * s / 0.5), c, SERIF)
    return q.move_to(ORIGIN).shift(DOWN * s * 0.1)


def i_layers(s=0.5, c=None):
    c = c or P["ink"]
    g = VGroup(*[RoundedRectangle(corner_radius=0.03, width=s * 0.72, height=s * 0.16, stroke_color=c,
                                  stroke_width=LW).shift(UP * (k - 1) * s * 0.26) for k in range(3)])
    return g


def station(icon, r=0.46, color=None, ring=None):
    c = Circle(radius=r, stroke_color=ring or color or P["ink"], stroke_width=LW * (1.25 if ring else 1),
               fill_color=P["soft"], fill_opacity=1)
    icon.move_to(c.get_center())
    return VGroup(c, icon)


def tag(text, kind="yes", size=16):
    t = T(text.upper(), size, None, MONO, MEDIUM)
    if kind == "yes":
        fill, tc, sc = P["ink"], P["plate"], P["ink"]
    elif kind == "no":
        fill, tc, sc = P["soft"], P["ink"], P["ink"]
    elif kind == "unc":
        fill, tc, sc = P["amber"], P["plate"], P["amber"]
    else:
        fill, tc, sc = P["accent"], P["plate"], P["accent"]
    t.set_color(tc)
    box = RoundedRectangle(corner_radius=0.05, width=t.width + 0.26, height=0.36, stroke_color=sc,
                           stroke_width=1.4, fill_color=fill, fill_opacity=1)
    t.move_to(box)
    return VGroup(box, t)


def connector(a, b, color=None, buff=0.08, tip=True):
    color = color or P["muted"]
    if tip:
        return Arrow(a, b, buff=buff, stroke_width=LW, color=color, tip_length=0.12,
                     max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=50)
    return Line(a, b, buff=buff, stroke_width=LW, color=color)


def diamond(s=0.5, color=None):
    return Square(side_length=s, stroke_color=color or P["ink"], stroke_width=LW,
                  fill_color=P["soft"], fill_opacity=1).rotate(PI / 4)


def tick(size=0.26, color=None, w=None):
    return VMobject(stroke_color=color or P["ink"], stroke_width=w or LW * 1.2).set_points_as_corners(
        [np.array([-0.5, 0.0, 0]) * size, np.array([-0.15, -0.38, 0]) * size, np.array([0.55, 0.45, 0]) * size])


def pulse(scene, mob, scale=1.08, rt=0.4):
    scene.play(mob.animate.scale(scale), rate_func=there_and_back, run_time=rt)


def travel(scene, path_points, color=None, rt=0.6, r=0.075):
    d = Dot(path_points[0], radius=r, color=color or P["ink"])
    path = VMobject().set_points_as_corners(path_points)
    scene.add(d)
    scene.play(MoveAlongPath(d, path), run_time=rt, rate_func=EASE)
    scene.remove(d)
