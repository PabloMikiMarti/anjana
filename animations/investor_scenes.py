"""Figures 7 and 8: the investment case.

Fig. 7  AIPipeline      AI-enabled drugs are filling the clinic; survivors end in adjudicated outcome trials.
Fig. 8  SpecialtyReuse  One Anjana engine; swap the endpoint definition to reach other specialties.

Every number on screen is sourced in docs/investor-evidence.md. Patient fields, event dots and
lanes are illustrative.
"""
from style import *


def fit(m, w):
    """Scale m down (never up) so it is at most w units wide."""
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def anjana_symbol(r=0.36, c=None):
    c = c or P["ink"]
    return VGroup(Circle(radius=r, stroke_color=c, stroke_width=LW).shift(LEFT * r / 2),
                  Circle(radius=r, stroke_color=c, stroke_width=LW).shift(RIGHT * r / 2))


def source_line(text):
    return fit(mono(text, 13), 13.0).move_to([0, -2.73, 0])


def dot_grid(n, cols, sp=0.22, r=0.06, color=None, fill=1.0):
    color = color or P["ink"]
    g = VGroup()
    for i in range(n):
        rr, cc = divmod(i, cols)
        g.add(Dot([cc * sp, -rr * sp, 0], radius=r, color=color, fill_opacity=fill))
    return g


# =====================================================================
# FIG 7 — AI is filling the clinic
# =====================================================================
class AIPipeline(Scene):
    def construct(self):
        kick = kicker("Fig. 7 · AI is filling the clinical pipeline")
        self.add(kick)
        N = Narrator(self, 5)

        # ---- beat 1: two counts of AI-enabled assets in human trials ----
        early = dot_grid(15, 5).move_to([-5.4, 0, 0])
        late = dot_grid(117, 13).move_to([-2.2, 0, 0])
        floor = -0.6
        early.shift([0, floor - early.get_bottom()[1], 0])
        late.shift([0, floor - late.get_bottom()[1], 0])
        n_early = serif("15", 56).set_x(early.get_x())
        n_late = serif("117", 56).set_x(late.get_x())
        for n in (n_early, n_late):
            n.shift([0, 1.5 - baseline_y(n), 0])
        cap_early = VGroup(mono("EARLY 2022", 14, P["ink"]), mono("APPROX. · 20 AI-NATIVE FIRMS", 12))
        cap_late = VGroup(mono("DEC 2025", 14, P["ink"]), mono("63 COMPANIES", 12))
        for cap, grid in ((cap_early, early), (cap_late, late)):
            cap.arrange(DOWN, buff=0.1).set_x(grid.get_x())
            cap.shift([0, (floor - 0.32) - cap.get_top()[1], 0])
        grow = connector([early.get_right()[0] + 0.2, early.get_y(), 0], [late.get_left()[0] - 0.2, early.get_y(), 0])

        N.say("AI-enabled drugs in human trials: from about 15 to 117.")
        self.play(FadeIn(n_early, shift=UP * 0.06), FadeIn(cap_early), run_time=0.45)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in early], lag_ratio=0.05), run_time=0.7)
        self.play(Create(grow), run_time=0.4)
        self.play(FadeIn(n_late, shift=UP * 0.06), FadeIn(cap_late), run_time=0.45)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in late], lag_ratio=0.012), run_time=1.6)
        self.wait(0.9)

        # ---- beat 2: rentosertib, one of those dots, now in Phase III ----
        star = late[13 * 8]  # first dot of the last row: bottom-left of the grid
        tether = Line(star.get_center() + DOWN * 0.1, [star.get_x(), -1.3, 0], color=P["accent"], stroke_width=1.4)
        call = VGroup(mono("RENTOSERTIB · PHASE III, JULY 2026", 14, P["accent"]),
                      T("Target and molecule both found with generative AI", 18, P["muted"]))
        call.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        fit(call, 6.0)
        call.move_to([star.get_x(), 0, 0], aligned_edge=LEFT)
        call.shift([0, -1.42 - call.get_top()[1], 0])

        N.say("One of them, rentosertib, entered Phase III in 2026.")
        self.play(star.animate.set_color(P["accent"]).scale(1.6), run_time=0.4)
        self.play(Create(tether), FadeIn(call, shift=UP * 0.05), run_time=0.6)
        self.wait(1.6)

        # ---- beat 3: Phase I success, AI cohort vs industry ----
        x0, x1 = 0.9, 6.4
        X = lambda f: x0 + f * (x1 - x0)
        head = mono("PHASE I SUCCESS", 14, P["ink"]).move_to([x0, 0, 0], aligned_edge=LEFT)
        head.shift([0, 1.5 - baseline_y(head), 0])

        def row(name, value, y, lo, hi, color):
            nm = T(name, 21, P["ink"], weight=MEDIUM).move_to([x0, 0, 0], aligned_edge=LEFT)
            nm.shift([0, (y + 0.42) - baseline_y(nm), 0])
            val = serif(value, 38).move_to([x1, 0, 0], aligned_edge=RIGHT)
            val.shift([0, (y + 0.42) - baseline_y(val), 0])
            track = Line([x0, y, 0], [x1, y, 0], color=P["rule"], stroke_width=1.4)
            solid = Rectangle(width=X(lo) - x0, height=0.2, stroke_width=0, fill_color=color, fill_opacity=1)
            solid.move_to([x0, y, 0], aligned_edge=LEFT)
            bars = VGroup(solid)
            if hi > lo:
                rng = Rectangle(width=X(hi) - X(lo), height=0.2, stroke_width=0, fill_color=color, fill_opacity=0.35)
                rng.move_to([X(lo), y, 0], aligned_edge=LEFT)
                bars.add(rng)
            return nm, val, track, bars

        ai = row("AI-discovered molecules", "80–90%", 0.62, 0.80, 0.90, P["ink"])
        ind = row("Industry average, 2011–2020", "52%", -0.48, 0.52, 0.52, P["muted"])
        note = mono("EARLY COHORT · PHASE II ABOUT 40%, IN LINE WITH HISTORY", 12)
        note.move_to([x0, -0.98, 0], aligned_edge=LEFT)
        fit(note, x1 - x0)

        N.say("In an early cohort, 80–90% passed Phase I. Industry: 52%.")
        self.play(FadeIn(head), run_time=0.3)
        for nm, val, track, bars in (ai, ind):
            self.play(FadeIn(nm), Create(track), run_time=0.35)
            self.play(GrowFromEdge(bars, LEFT), FadeIn(val, shift=UP * 0.05), run_time=0.7, rate_func=EASE)
        self.play(FadeIn(note), FadeIn(source_line(
            "JAYATUNGA ET AL. NRDD 2022, DDT 2024 · HAQUE ET AL. JCO 2026 · BIO/INFORMA/QLS 2021 · INSILICO 2026")),
            run_time=0.4)
        self.wait(2.0)

        # ---- beat 4: survivors enter outcome trials; events accrue ----
        self.play(*[FadeOut(m) for m in self.mobjects if m is not kick and m is not N.cur], run_time=0.5)

        field = dot_grid(286, 26, sp=0.2, r=0.045, color=P["muted"], fill=0.45).move_to([-3.9, 0.55, 0])
        fhead = mono("OUTCOME TRIAL · EACH DOT A GROUP OF PATIENTS", 13).move_to([field.get_left()[0], 0, 0], aligned_edge=LEFT)
        fhead.shift([0, (field.get_top()[1] + 0.32) - baseline_y(fhead), 0])
        rng = np.random.default_rng(7)
        ev_idx = sorted(rng.choice(len(field), 30, replace=False))
        events = VGroup(*[field[i] for i in ev_idx])

        N.say("Survivors enter outcome trials. Every event needs review.")
        self.play(FadeIn(fhead), LaggedStart(*[FadeIn(d, scale=0.6) for d in field], lag_ratio=0.002), run_time=1.0)
        self.play(LaggedStart(*[d.animate.set_color(P["accent"]).set_opacity(1).scale(1.5) for d in events],
                              lag_ratio=0.06), run_time=1.6)
        self.wait(0.8)

        # ---- beat 5: dossiers flow through Anjana into three lanes ----
        docs = VGroup(*[i_doc(0.5).shift([k * 0.09, -k * 0.09, 0]) for k in range(3)])
        dos = station(docs).move_to([-0.15, 0.55, 0])
        ana = anjana_symbol(r=0.26).move_to([2.3, 0.55, 0])
        ana_ring = Circle(radius=0.46, stroke_color=P["ink"], stroke_width=LW, fill_color=P["soft"],
                          fill_opacity=1).move_to(ana)
        ana_g = VGroup(ana_ring, ana)
        l_dos = under(dos, label("Event dossiers", "one per event"))
        l_ana = under(ana_g, label("Anjana", "two AI readers"))
        a1 = connector(dos.get_right(), ana_g.get_left(), buff=0.14)

        lanes = VGroup(tag("Confirmed", "yes", 14), tag("Rejected", "no", 14), tag("To physician", "unc", 14))
        for t, y in zip(lanes, (1.35, 0.55, -0.25)):
            t.move_to([4.05, y, 0], aligned_edge=LEFT)
        doc_p = station(i_person(0.42), r=0.32, ring=P["amber"]).next_to(lanes[2], RIGHT, buff=0.25)
        arrows = VGroup(*[connector(ana_g.get_right(), t.get_left(), buff=0.12,
                                    color=P["amber"] if k == 2 else P["muted"]) for k, t in enumerate(lanes)])
        stat = T("10 cardiovascular outcome trials: 95,038 patients, more than 9,000 events.", 22, weight=MEDIUM)
        fit(stat, 12.4).move_to([0, -1.55, 0])

        N.say("Anjana reads every dossier and routes only the hard cases.")
        self.play(FadeIn(dos, scale=0.92), FadeIn(l_dos), run_time=0.45)
        self.play(LaggedStart(*[d.animate.move_to(dos.get_center()).scale(0.4).set_opacity(0) for d in events],
                              lag_ratio=0.03), run_time=1.3, rate_func=EASE)
        self.play(Create(a1), FadeIn(ana_g, scale=0.92), FadeIn(l_ana), run_time=0.6)
        travel(self, [dos.get_center(), ana_g.get_center()], P["ink"], rt=0.5)
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(t, shift=RIGHT * 0.06) for t in lanes], lag_ratio=0.15), run_time=0.8)
        self.play(FadeIn(doc_p, scale=0.9), run_time=0.35)
        self.play(FadeIn(stat, shift=UP * 0.06), FadeIn(source_line(
            "PATIENTS, EVENTS AND LANES ILLUSTRATIVE · CVOT TOTALS: DAVIDSON ET AL. JACC BTS 2024")), run_time=0.5)
        self.wait(3.2)


# =====================================================================
# FIG 8 — one engine, swappable endpoint definitions
# =====================================================================
class SpecialtyReuse(Scene):
    CARDS = [
        ("Cardiovascular", "HF hospitalization", "DELIVER · Circ Heart Fail 2025", "validated"),
        ("Cardiovascular", "CV death · MI · stroke", "PARADISE-MI · JACC 2025", "validated"),
        ("Pulmonary", "Cause of death in COPD", "ETHOS · 8,509 patients", "proposed"),
        ("Renal", "AKI and kidney failure", "EMPA-KIDNEY · 6,609 patients", "proposed"),
        ("Metabolic", "MACE in obesity", "SELECT · 17,604 patients", "proposed"),
    ]

    def card_content(self, frame, spec):
        area, title, sub, status = spec
        col = P["ink"] if status == "validated" else P["amber"]
        left, top = frame.get_left()[0] + 0.3, frame.get_top()[1]
        k = mono(area.upper(), 14, col).move_to([left, 0, 0], aligned_edge=LEFT)
        k.shift([0, (top - 0.42) - baseline_y(k), 0])
        t = fit(serif(title, 32), frame.width - 0.6).move_to([left, 0, 0], aligned_edge=LEFT)
        t.shift([0, (top - 0.95) - baseline_y(t), 0])
        s = fit(T(sub, 17, P["muted"]), frame.width - 0.6).move_to([left, 0, 0], aligned_edge=LEFT)
        s.shift([0, (top - 1.35) - baseline_y(s), 0])
        g = tag("Validated" if status == "validated" else "Proposed", "yes" if status == "validated" else "unc", 13)
        g.move_to([left, top - 1.78, 0], aligned_edge=LEFT)
        return VGroup(k, t, s, g), col

    def construct(self):
        self.add(kicker("Fig. 8 · One engine, more specialties"))
        N = Narrator(self, 4)

        # ---- the engine: five modules ----
        names = ["Dossier intake and translation", "Reader 1 · reasoning model", "Reader 2 · trained classifier",
                 "Quoted evidence per criterion", "Physician review and sign-off"]
        ys = [2.0, 1.2, 0.4, -0.4, -1.2]
        bx0, bx1 = -0.1, 6.5
        mods = VGroup()
        for n, y in zip(names, ys):
            box = RoundedRectangle(width=bx1 - bx0, height=0.6, corner_radius=0.05, stroke_color=P["ink"],
                                   stroke_width=1.4, fill_color=P["soft"], fill_opacity=1).move_to([(bx0 + bx1) / 2, y, 0])
            txt = fit(T(n, 21, P["ink"]), 4.3).move_to([bx0 + 0.25, y, 0], aligned_edge=LEFT)
            txt.shift([0, (y - 0.08) - baseline_y(txt), 0])
            mods.add(VGroup(box, txt))
        ehead = mono("ANJANA", 14, P["ink"]).move_to([bx0, 0, 0], aligned_edge=LEFT)
        ehead.shift([0, (ys[0] + 0.52) - baseline_y(ehead), 0])

        # ---- the definition card ----
        frame = RoundedRectangle(width=4.5, height=2.1, corner_radius=0.06, stroke_color=P["ink"], stroke_width=LW,
                                 fill_color=P["soft"], fill_opacity=1).move_to([-4.35, 0.8, 0])
        chead = mono("ENDPOINT DEFINITION", 14).move_to([frame.get_left()[0], 0, 0], aligned_edge=LEFT)
        chead.shift([0, (frame.get_top()[1] + 0.22) - baseline_y(chead), 0])
        content, col = self.card_content(frame, self.CARDS[0])
        feeds = VGroup(connector([frame.get_right()[0], ys[1], 0], [bx0, ys[1], 0], buff=0.1),
                       connector([frame.get_right()[0], ys[2], 0], [bx0, ys[2], 0], buff=0.1))
        flabels = VGroup(fit(mono("DEFINITION", 11), 1.6).next_to(feeds[0], UP, buff=0.08),
                         fit(mono("TRAINING DATA", 11), 1.6).next_to(feeds[1], UP, buff=0.08))

        N.say("Anjana reads each dossier against a written definition.")
        self.play(FadeIn(ehead), LaggedStart(*[FadeIn(m, shift=UP * 0.05) for m in mods], lag_ratio=0.12), run_time=1.0)
        self.play(FadeIn(chead), FadeIn(frame), FadeIn(content), run_time=0.6)
        self.play(LaggedStart(*[Create(f) for f in feeds], lag_ratio=0.2), FadeIn(flabels), run_time=0.6)
        travel(self, [np.array([frame.get_right()[0], ys[1], 0]), np.array([bx0, ys[1], 0])], rt=0.5)
        self.wait(1.2)

        def swap(spec, hold):
            nonlocal content
            new, ncol = self.card_content(frame, spec)
            self.play(FadeOut(content, shift=UP * 0.12), run_time=0.25)
            self.play(frame.animate.set_stroke(ncol), FadeIn(new, shift=UP * 0.12),
                      feeds.animate.set_color(ncol if ncol == P["amber"] else P["muted"]), run_time=0.4)
            content = new
            self.play(*[m[0].animate.set_stroke(ncol) for m in mods[1:3]], run_time=0.25)
            self.play(*[m[0].animate.set_stroke(P["ink"]) for m in mods[1:3]], run_time=0.25)
            self.wait(hold)

        N.say("Change the definition: cardiovascular death, MI, stroke.")
        swap(self.CARDS[1], 1.3)

        N.say("Pulmonary, renal and metabolic trials adjudicate too.")
        for spec in self.CARDS[2:]:
            swap(spec, 1.0)
        self.play(FadeIn(source_line(
            "ETHOS · EMPA-KIDNEY · SELECT USE PUBLISHED COMMITTEE ADJUDICATION · NOT ANJANA RESULTS")), run_time=0.4)
        self.wait(0.6)

        # ---- beat 4: what carries over, what is adapted ----
        kinds = [("Shared", "yes"), ("New definition", "unc"), ("Retrain", "unc"), ("Shared", "yes"), ("Shared", "yes")]
        tags = VGroup()
        for (txt, kind), y in zip(kinds, ys):
            t = tag(txt, kind, 13).move_to([bx1 - 0.18, y, 0], aligned_edge=RIGHT)
            tags.add(t)
        sumline = T("Three of five modules carry over unchanged.", 22, weight=MEDIUM)
        sumline.move_to([frame.get_left()[0], 0, 0], aligned_edge=LEFT)
        sumline.shift([0, -1.25 - baseline_y(sumline), 0])
        fit(sumline, 6.1)

        N.say("Keep the engine. Adapt definitions, retrain, validate.")
        self.play(LaggedStart(*[FadeIn(t, shift=LEFT * 0.06) for t in tags], lag_ratio=0.12), run_time=0.9)
        self.play(*[mods[i][0].animate.set_stroke(P["amber"]) for i in (1, 2)], run_time=0.35)
        self.play(FadeIn(sumline, shift=UP * 0.06), run_time=0.45)
        self.wait(3.2)
