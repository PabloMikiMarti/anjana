from style import *


def elbow(points, color=None, tip=True):
    """Polyline connector with an arrow on the last segment."""
    color = color or P["muted"]
    segs = VGroup()
    for a, b in zip(points[:-2], points[1:-1]):
        segs.add(Line(a, b, stroke_width=LW, color=color))
    segs.add(connector(points[-2], points[-1], color, buff=0.0, tip=tip))
    return segs


# =====================================================================
# FIG 1 — How events are adjudicated today
# =====================================================================
class Committee(Scene):
    def construct(self):
        self.add(kicker("Fig. 1 · How events are adjudicated today"))
        N = Narrator(self, 7)

        SITE = station(i_globe()).move_to([-5.95, 0.85, 0])
        DOS = station(i_doc()).move_to([-3.55, 0.85, 0])
        PA = station(i_person()).move_to([-1.65, 2.0, 0])
        PB = station(i_person()).move_to([-1.65, -0.3, 0])
        DIA = diamond(0.5).move_to([1.4, 0.85, 0])
        END = station(i_db()).move_to([5.75, 0.85, 0])
        CM = station(i_table()).move_to([3.6, -1.05, 0])

        lSITE = under(SITE, label("Trial site", "reports an event"), 0.2)
        lDOS = under(DOS, label("Dossier", "redacted, translated"), 0.2)
        lPA = under(PA, label("Physician A"), 0.18)
        lPB = under(PB, label("Physician B"), 0.18)
        lDIA = mono("AGREE?", 15).next_to(DIA, UP, buff=0.16)
        lEND = over(END, label("Endpoint", "recorded"), 0.2)
        lCM = under(CM, label("Committee", "the chair breaks ties"), 0.2)

        # 1 site
        N.say("A trial site reports a possible event.")
        self.play(FadeIn(SITE, scale=0.92), FadeIn(lSITE, shift=UP * 0.06), run_time=0.6)
        self.wait(0.5)
        # 2 dossier
        N.say("Its records become a redacted, translated dossier.")
        c1 = connector(SITE.get_right(), DOS.get_left())
        self.play(Create(c1), run_time=0.45)
        self.play(FadeIn(DOS, scale=0.92), FadeIn(lDOS, shift=UP * 0.06), run_time=0.5)
        doc_lines = DOS[1][2]
        bars = VGroup(*[Rectangle(width=doc_lines[k].get_length() * 0.75, height=0.05, stroke_width=0, fill_color=P["ink"],
                                  fill_opacity=1).move_to(doc_lines[k]).align_to(doc_lines[k], LEFT) for k in (0, 2)])
        en = mono("EN", 13, P["accent"], MEDIUM).next_to(DOS[0], UR, buff=-0.08)
        self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.3), FadeIn(en), run_time=0.6)
        self.wait(0.5)
        # 3 two physicians
        N.say("Two physicians review it independently.")
        c2 = connector(DOS.get_right(), PA.get_left())
        c3 = connector(DOS.get_right(), PB.get_left())
        self.play(Create(c2), Create(c3), run_time=0.5)
        self.play(FadeIn(PA, scale=0.92), FadeIn(PB, scale=0.92), FadeIn(lPA), FadeIn(lPB), run_time=0.5)
        slotA = PA.get_right() + RIGHT * 0.62
        slotB = PB.get_right() + RIGHT * 0.62
        tA = tag("HF", "yes").move_to(slotA)
        tB = tag("HF", "yes").move_to(slotB)
        self.play(FadeIn(tA, shift=RIGHT * 0.08), run_time=0.35)
        self.play(FadeIn(tB, shift=RIGHT * 0.08), run_time=0.35)
        self.wait(0.3)
        # 4 agree
        N.say("If they agree, the endpoint is recorded.")
        c4 = connector(tA.get_right(), DIA.get_left() + UP * 0.02, buff=0.06)
        c5 = connector(tB.get_right(), DIA.get_left() + DOWN * 0.02, buff=0.06)
        self.play(Create(c4), Create(c5), FadeIn(DIA), FadeIn(lDIA), run_time=0.55)
        c6 = connector(DIA.get_right(), END.get_left(), buff=0.06)
        yes = mono("YES", 14).next_to(c6, UP, buff=0.1)
        self.play(Create(c6), FadeIn(yes), FadeIn(END, scale=0.92), FadeIn(lEND), run_time=0.6)
        travel(self, [DIA.get_center(), END.get_center()], P["ink"], 0.6)
        pulse(self, END)
        self.wait(0.3)
        # 5 disagree
        N.say("If not, the committee meets and the chair decides.")
        tB2 = tag("not HF", "no").move_to(slotB)
        self.play(Transform(tB, tB2), run_time=0.4)
        self.play(DIA.animate.set_stroke(P["accent"]).set_fill(P["accent"], 0.16), lDIA.animate.set_color(P["accent"]), run_time=0.35)
        pd = DIA.get_bottom()
        c7 = elbow([pd, np.array([pd[0], CM.get_center()[1], 0]), CM.get_left()], P["accent"])
        no = mono("NO", 14, P["accent"]).next_to(c7[0], LEFT, buff=0.12)
        self.play(Create(c7), FadeIn(no), run_time=0.55)
        self.play(FadeIn(CM, scale=0.92), FadeIn(lCM), run_time=0.45)
        c8 = elbow([CM.get_right(), np.array([END.get_center()[0], CM.get_center()[1], 0]), END.get_bottom()], P["muted"])
        self.play(Create(c8), run_time=0.5)
        travel(self, [CM.get_right(), np.array([END.get_center()[0], CM.get_center()[1], 0]), END.get_center()], P["accent"], 0.7)
        self.wait(1.0)

        # 6 scale
        stage = VGroup(SITE, DOS, PA, PB, DIA, END, CM, lSITE, lDOS, lPA, lPB, lDIA, lEND, lCM,
                       c1, c2, c3, c4, c5, c6, c7, c8, yes, no, tA, tB, bars, en)
        self.play(FadeOut(stage), run_time=0.6)
        N.say("In DELIVER, 1,597 potential events took this path.")
        cols, sp = 80, 0.135
        grid = VGroup()
        for i in range(1597):
            r_, c_ = divmod(i, cols)
            grid.add(Square(0.09, stroke_width=0, fill_color=P["ink"], fill_opacity=1).move_to([c_ * sp, -r_ * sp, 0]))
        grid.move_to([0, 0.15, 0])
        head = VGroup(serif("1,597", 66), T("potential heart-failure hospitalizations", 22, P["muted"])).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        head.next_to(grid, UP, buff=0.42).align_to(grid, LEFT)
        self.play(FadeIn(head, shift=UP * 0.06), run_time=0.45)
        self.play(LaggedStart(*[FadeIn(sq) for sq in grid], lag_ratio=0.0011), run_time=1.8)
        foot = mono("EACH READ BY TWO PHYSICIANS · AT LEAST 3,194 REVIEWS", 15).next_to(grid, DOWN, buff=0.32).align_to(grid, RIGHT)
        self.play(FadeIn(foot), run_time=0.4)
        self.wait(1.6)

        # 7 reproducibility
        self.play(FadeOut(grid), FadeOut(head), FadeOut(foot), run_time=0.5)
        N.say("And different committees can reach different answers.")
        n = 20
        rng = np.random.default_rng(7)
        v1 = (rng.random(n) < 0.72).astype(int)
        v2 = v1.copy()
        flips = [3, 8, 13, 17]
        for f in flips:
            v2[f] = 1 - v2[f]
        size, gap = 0.3, 0.1

        def row(v):
            return VGroup(*[Square(size, stroke_color=P["ink"], stroke_width=1.4, fill_color=P["ink"] if x else P["soft"],
                                   fill_opacity=1).move_to([i * (size + gap), 0, 0]) for i, x in enumerate(v)])
        r1, r2 = row(v1), row(v2)
        rows = VGroup(r1, r2).arrange(DOWN, buff=0.36)
        rows.move_to([0, 0.75, 0]).align_to([-2.4, 0, 0], LEFT)
        l1 = T("Committee 1", 21, weight=MEDIUM).next_to(r1, LEFT, buff=0.35)
        l2 = T("Committee 2", 21, weight=MEDIUM).next_to(r2, LEFT, buff=0.35)
        ttl = T("The same 20 dossiers, adjudicated twice", 21, P["muted"]).next_to(rows, UP, buff=0.45).align_to(l1, LEFT)
        self.play(FadeIn(ttl), FadeIn(l1), LaggedStart(*[FadeIn(s) for s in r1], lag_ratio=0.03), run_time=0.9)
        self.play(FadeIn(l2), LaggedStart(*[FadeIn(s) for s in r2], lag_ratio=0.03), run_time=0.9)
        marks = VGroup(*[SurroundingRectangle(VGroup(r1[f], r2[f]), color=P["accent"], buff=0.07, stroke_width=1.6,
                                              corner_radius=0.04) for f in flips])
        self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.15), run_time=0.8)
        kap = Text("κ 0.60", font=SERIF, font_size=60, color=P["accent"], t2f={"κ": "FreeSerif"}, t2s={"κ": ITALIC})
        kap_l = T("agreement between two committees", 20, P["muted"])
        kap2 = Text("κ 0.72", font=SERIF, font_size=60, color=P["ink"], t2f={"κ": "FreeSerif"}, t2s={"κ": ITALIC})
        kap2_l = T("between two reviewers on one committee", 20, P["muted"])
        k1 = VGroup(kap, kap_l).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        k2 = VGroup(kap2, kap2_l).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        ks = VGroup(k2, k1).arrange(RIGHT, buff=1.0, aligned_edge=UP).next_to(rows, DOWN, buff=0.7).align_to(l1, LEFT)
        self.play(FadeIn(k2, shift=UP * 0.06), run_time=0.45)
        self.play(FadeIn(k1, shift=UP * 0.06), run_time=0.45)
        src = mono("PUBLISHED ESTIMATES · HF HOSPITALIZATION IN GLOBAL TRIALS · SQUARES ILLUSTRATIVE", 13)
        src.next_to(ks, DOWN, buff=0.45).align_to(ks, LEFT)
        self.play(FadeIn(src), run_time=0.3)
        self.wait(2.6)


# =====================================================================
# FIG 2 — Two readers
# =====================================================================
class TwoReaders(Scene):
    def construct(self):
        self.add(kicker("Fig. 2 · The committee's logic, with two AI readers"))
        N = Narrator(self, 6)
        yc, yt, yb = 0.2, 1.5, -1.1
        pD = np.array([-5.6, yc, 0])
        xR, xBus, xMerge, xDia, xOut = -2.6, -4.3, -0.55, 0.95, 4.7
        pA, pB = np.array([xR, yt, 0]), np.array([xR, yb, 0])
        pY, pN = np.array([xOut, yt, 0]), np.array([xOut, yb, 0])
        muted = P["muted"]

        def poly(pts, color=None, tip=True):
            return elbow([np.array(p, dtype=float) for p in pts], color or muted, tip)

        D = station(i_doc()).move_to(pD)
        lD = under(D, label("Dossier", "one reported event"), 0.18)
        A = station(i_person()).move_to(pA)
        B = station(i_person()).move_to(pB)
        lA = over(A, label("Physician A", "independent review"), 0.18)
        lB = under(B, label("Physician B", "independent review"), 0.18)
        DIA = diamond(0.5).move_to([xDia, yc, 0])
        lDIA = mono("AGREE?", 15).next_to(DIA, RIGHT, buff=0.2)
        REC = station(i_db()).move_to(pY)
        lREC = over(REC, label("Recorded", "endpoint confirmed"), 0.18)
        CM = station(i_table()).move_to(pN)
        lCM = under(CM, label("Committee", "the chair breaks ties"), 0.18)

        r = 0.46
        inA = poly([pD + RIGHT * r, [xBus, yc, 0], [xBus, yt, 0], pA + LEFT * (r + 0.04)])
        inB = poly([[xBus, yc, 0], [xBus, yb, 0], pB + LEFT * (r + 0.04)])
        outA = poly([pA + RIGHT * r, [xMerge, yt, 0], [xMerge, yc, 0], DIA.get_left() + LEFT * 0.04])
        outB = Line(pB + RIGHT * r, [xMerge, yb, 0], stroke_width=LW, color=muted).add(Line([xMerge, yb, 0], [xMerge, yc, 0], stroke_width=LW, color=muted))
        yes = poly([DIA.get_top(), [xDia, yt, 0], pY + LEFT * (r + 0.04)])
        no = poly([DIA.get_bottom(), [xDia, yb, 0], pN + LEFT * (r + 0.04)])
        yl = mono("YES", 14).next_to(Line([xDia, yt, 0], [xOut - r, yt, 0]), UP, buff=0.1)
        nl = mono("NO", 14).next_to(Line([xDia, yb, 0], [xOut - r, yb, 0]), DOWN, buff=0.1)
        slotA, slotB = np.array([(xR + r + xMerge) / 2, yt, 0]), np.array([(xR + r + xMerge) / 2, yb, 0])

        N.say("A committee reads every dossier twice.")
        self.play(FadeIn(D), FadeIn(lD), run_time=0.4)
        self.play(Create(inA), Create(inB), run_time=0.6, rate_func=EASE)
        self.play(FadeIn(A, scale=0.94), FadeIn(B, scale=0.94), FadeIn(lA), FadeIn(lB), run_time=0.5)
        self.play(Create(outA), Create(outB), run_time=0.6, rate_func=EASE)
        self.play(FadeIn(DIA), FadeIn(lDIA), run_time=0.35)
        self.play(Create(yes), Create(no), FadeIn(yl), FadeIn(nl), run_time=0.6, rate_func=EASE)
        self.play(FadeIn(REC, scale=0.94), FadeIn(lREC), FadeIn(CM, scale=0.94), FadeIn(lCM), run_time=0.5)
        self.wait(0.8)

        N.say("We keep the structure and change the readers.")
        self.play(VGroup(A, B, lA, lB).animate.set_opacity(0.22), run_time=0.5)
        self.wait(0.3)

        def swap(old, oldl, new, newl):
            self.play(FadeOut(old, scale=0.9), FadeOut(oldl), run_time=0.3)
            self.play(FadeIn(new, scale=0.9), FadeIn(newl, shift=UP * 0.04), run_time=0.45)

        A2 = station(i_quote()).move_to(pA)
        lA2 = over(A2, label("Reasoning model", "applies the FDA definition, quotes the record"), 0.18)
        N.say("One reasons over the definition and quotes the evidence.")
        swap(A, lA, A2, lA2)
        self.wait(0.4)
        B2 = station(i_layers()).move_to(pB)
        lB2 = under(B2, label("Trained classifier", "learned from thousands of committee decisions"), 0.18)
        N.say("The other has learned from thousands of committee decisions.")
        swap(B, lB, B2, lB2)
        self.wait(0.4)

        ok = VGroup(Circle(radius=r, stroke_color=P["ink"], stroke_width=LW, fill_color=P["soft"], fill_opacity=1), tick(0.3)).move_to(pY)
        ok[1].move_to(ok[0])
        lOK = over(ok, label("Confident", "recorded with quoted evidence"), 0.18)
        HUM = station(i_person(), ring=P["amber"]).move_to(pN)
        lHUM = under(HUM, label("Uncertain", "a human adjudicator decides"), 0.18)

        def run(ka, ta, kb, tb, agree):
            pa = [pD, [xBus, yc, 0], [xBus, yt, 0], pA]
            pb = [pD, [xBus, yc, 0], [xBus, yb, 0], pB]
            da, db = Dot(pD, radius=0.07, color=P["ink"]), Dot(pD, radius=0.07, color=P["ink"])
            self.add(da, db)
            self.play(MoveAlongPath(da, VMobject().set_points_as_corners([np.array(p, dtype=float) for p in pa])),
                      MoveAlongPath(db, VMobject().set_points_as_corners([np.array(p, dtype=float) for p in pb])),
                      run_time=0.6, rate_func=EASE)
            self.remove(da, db)
            a = tag(ta, ka).move_to(slotA)
            b = tag(tb, kb).move_to(slotB)
            self.play(FadeIn(a, scale=0.9), FadeIn(b, scale=0.9), run_time=0.3)
            col = P["ink"] if agree else P["amber"]
            tgt = pY if agree else pN
            if not agree:
                self.play(DIA.animate.set_stroke(col).set_fill(col, 0.22), run_time=0.25)
            yv = yt if agree else yb
            travel(self, [np.array([xMerge, yc, 0]), DIA.get_center(), np.array([xDia, yv, 0]), tgt], col, 0.7)
            ring = (ok if agree else HUM)[0]
            self.play(ring.animate.scale(1.12), rate_func=there_and_back, run_time=0.35)
            self.play(FadeOut(a), FadeOut(b), DIA.animate.set_stroke(P["ink"]).set_fill(P["soft"], 1), run_time=0.3)

        N.say("When they agree, the decision is recorded with its evidence.")
        swap(REC, lREC, ok, lOK)
        run("yes", "HF", "yes", "HF", True)
        run("no", "not HF", "no", "not HF", True)
        N.say("When they disagree, a human adjudicator decides.")
        self.play(FadeOut(CM, scale=0.9), FadeOut(lCM), no.animate.set_color(P["amber"]), nl.animate.set_color(P["amber"]), run_time=0.3)
        self.play(FadeIn(HUM, scale=0.9), FadeIn(lHUM, shift=DOWN * 0.04), run_time=0.45)
        run("yes", "HF", "no", "not HF", False)
        self.wait(2.4)


# =====================================================================
# FIG 3 — Every decision shows its work
# =====================================================================
class Evidence(Scene):
    def construct(self):
        self.add(kicker("Fig. 3 · Every decision shows its work"))
        N = Narrator(self, 3)
        sheet = Rectangle(width=6.3, height=5.75, stroke_color=P["ink"], stroke_width=1.4,
                          fill_color=P["soft"], fill_opacity=1).move_to([-3.45, 0.1, 0]).set_z_index(-2)
        hdr = mono("DISCHARGE SUMMARY · TRANSLATED · P. 3 OF 41", 14).move_to(sheet.get_corner(UL) + np.array([0.35, -0.38, 0]), aligned_edge=LEFT)
        rule = Line(sheet.get_left() + RIGHT * 0.35, sheet.get_right() + LEFT * 0.35, stroke_width=1, color=P["rule"]).next_to(hdr, DOWN, buff=0.16)
        rule.align_to(hdr, LEFT)
        txt = ["Admitted 20 May with dyspnea at rest",
               "and orthopnea for four days.",
               "Exam: bilateral pitting edema, basal",
               "crackles, raised JVP. NT-proBNP 4,820.",
               "Diagnosis: acute decompensated",
               "heart failure.",
               "IV furosemide 40 mg twice daily.",
               "Discharged 27 May, euvolemic."]
        L = VGroup(*[T(s, 25, P["ink"], SERIF) for s in txt])
        x0 = rule.get_left()[0]
        b0 = rule.get_bottom()[1] - 0.6
        for i, l in enumerate(L):
            l.shift([x0 - l.get_left()[0], (b0 - i * 0.555) - l[0].get_bottom()[1], 0])
        synth = mono("SYNTHETIC EXAMPLE", 12).move_to(sheet.get_corner(DL) + np.array([0.35, 0.28, 0]), aligned_edge=LEFT)

        N.say("The model reads the dossier against the FDA definition.")
        self.play(FadeIn(sheet), FadeIn(hdr), Create(rule), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.04) for l in L], lag_ratio=0.1), FadeIn(synth), run_time=1.1)

        crit = ["Primary diagnosis of heart failure", "Hospital stay longer than 24 hours", "At least one HF symptom",
                "At least two objective signs", "At least one HF treatment"]
        head = VGroup(mono("FDA / SCTI DEFINITION", 15), T("Heart-failure hospitalization", 26, weight=MEDIUM)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        rows = VGroup()
        for k, s in enumerate(crit):
            box = Square(0.34, stroke_color=P["ink"], stroke_width=1.4, fill_color=P["soft"], fill_opacity=1)
            num = mono(f"{k + 1}", 14)
            t = T(s, 23)
            rows.add(VGroup(box, t).arrange(RIGHT, buff=0.26))
        rows.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        right = VGroup(head, rows).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        right.move_to([0, 0.55, 0]).align_to([0.75, 0, 0], LEFT)
        self.play(FadeIn(head), LaggedStart(*[FadeIn(r, shift=LEFT * 0.06) for r in rows], lag_ratio=0.1), run_time=0.9)
        self.wait(0.3)

        N.say("Each criterion is tied to the sentence that satisfies it.")
        maps = [([0, 1], 2), ([2, 3], 3), ([4, 5], 0), ([6], 4), ([7], 1)]
        for li, ci in maps:
            grp = VGroup(*[L[i] for i in li])
            wash = VGroup(*[Rectangle(width=L[i].width + 0.12, height=0.34, stroke_width=0, fill_color=P["wash"], fill_opacity=1)
                            .move_to(L[i]).shift(DOWN * 0.02) for i in li]).set_z_index(-1)
            und = VGroup(*[Line(L[i].get_corner(DL) + DOWN * 0.07, L[i].get_corner(DR) + DOWN * 0.07, stroke_width=1.8, color=P["amber"])
                           for i in li])
            box = rows[ci][0]
            p0 = np.array([sheet.get_right()[0], grp.get_center()[1], 0])
            link = CubicBezier(p0, p0 + RIGHT * 0.4, box.get_left() + LEFT * 0.4, box.get_left() + LEFT * 0.06,
                               stroke_color=P["amber"], stroke_width=1.6)
            self.add(wash)
            self.play(FadeIn(wash), Create(und), run_time=0.3)
            self.play(Create(link), run_time=0.35)
            self.play(box.animate.set_fill(P["faint"], 1), Create(tick(0.28).move_to(box)), run_time=0.3)
            self.play(FadeOut(link), run_time=0.2)

        N.say("The decision arrives with its evidence.")
        v = VGroup(tag("HF hospitalization", "yes", 18), T("all five criteria met, every sentence quoted", 19, P["muted"])).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        v.next_to(rows, DOWN, buff=0.6).align_to(rows, LEFT)
        self.play(FadeIn(v, shift=UP * 0.06), run_time=0.5)
        self.wait(2.6)


# =====================================================================
# FIG 4 — Triage at trial scale (DELIVER)
# =====================================================================
class Triage(Scene):
    def construct(self):
        self.add(kicker("Fig. 4 · Triage at trial scale · DELIVER"))
        N = Narrator(self, 4)
        counts, hf = [7, 10, 16, 21, 46], [1, 3, 11, 18, 44]
        pct = ["17%", "32%", "66%", "85%", "96%"]
        names = ["confident\nnot HF", "probable\nnot HF", "uncertain", "probable\nHF", "confident\nHF"]
        scores = ["−2", "−1", "0", "+1", "+2"]
        r, sp = 0.1, 0.26

        dots = VGroup()
        for i in range(100):
            rr, cc = divmod(i, 10)
            dots.add(Circle(radius=r, stroke_color=P["muted"], stroke_width=1.3, fill_color=P["muted"], fill_opacity=0.3).move_to([cc * sp, -rr * sp, 0]))
        dots.move_to([-4.45, -0.15, 0])
        lab = VGroup(serif("1,597", 52), mono("EACH DOT ≈ 1% OF EVENTS", 14)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        lab.next_to(dots, UP, buff=0.35).align_to(dots, LEFT)

        N.say("DELIVER: 1,597 potential heart-failure hospitalizations.")
        self.play(FadeIn(lab[0], shift=UP * 0.06), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(d, scale=0.6) for d in dots], lag_ratio=0.008), FadeIn(lab[1]), run_time=1.1)
        self.wait(0.4)

        xs = [-1.45, 0.3, 2.05, 3.8, 5.55]
        base_y, width = -1.35, 4
        targets, assign = [], []
        for c in range(5):
            for j in range(counts[c]):
                rr, cc = divmod(j, width)
                targets.append(np.array([xs[c] + (cc - 1.5) * sp, base_y + rr * sp, 0]))
                assign.append((c, j < hf[c]))
        order = np.random.default_rng(3).permutation(100)
        axis = Line([xs[0] - 0.8, base_y - 0.32, 0], [xs[-1] + 0.8, base_y - 0.32, 0], color=P["rule"], stroke_width=1.4)
        sc = VGroup(*[mono(s, 20, P["ink"]).move_to([xs[c], base_y - 0.62, 0]) for c, s in enumerate(scores)])
        for m in sc:
            m.shift([0, (base_y - 0.72) - m[-1].get_bottom()[1], 0])
        def cstack(txt, ref):
            lines = [T(x, 17, P["muted"]) for x in txt.split("\n")]
            for k, ln in enumerate(lines):
                ln.set_x(ref.get_x())
                ln.shift([0, (ref.get_bottom()[1] - 0.32 - k * 0.28) - baseline_y(ln), 0])
            return VGroup(*lines)
        nm = VGroup(*[cstack(s, sc[c]) for c, s in enumerate(names)])
        axl = mono("AI SCORE", 14).next_to(sc[0], LEFT, buff=0.5)

        N.say("The AI scores each one, from confident no to confident yes.")
        self.play(Create(axis), FadeIn(sc), FadeIn(nm), FadeIn(axl), FadeOut(lab, shift=UP * 0.06), run_time=0.5)
        self.play(LaggedStart(*[dots[order[i]].animate.move_to(targets[i]) for i in range(100)], lag_ratio=0.012),
                  run_time=2.2, rate_func=EASE)
        self.wait(0.3)

        N.say("Higher scores were confirmed by the committee more often.")
        anims = []
        for i in range(100):
            d = dots[order[i]]
            anims.append(d.animate.set_fill(P["ink"] if assign[i][1] else P["soft"], 1).set_stroke(P["ink"]))
        leg = VGroup(Circle(radius=r, stroke_color=P["ink"], stroke_width=1.3, fill_color=P["ink"], fill_opacity=1),
                     T("committee confirmed", 17, P["muted"]),
                     Circle(radius=r, stroke_color=P["ink"], stroke_width=1.3, fill_color=P["soft"], fill_opacity=1),
                     T("committee rejected", 17, P["muted"])).arrange(RIGHT, buff=0.12)
        leg[2].shift(RIGHT * 0.25); leg[3].shift(RIGHT * 0.25)
        leg.to_corner(UR, buff=0.5)
        self.play(LaggedStart(*anims, lag_ratio=0.006), FadeIn(leg), run_time=1.3)
        tops = [base_y + (int(np.ceil(counts[c] / width)) - 1) * sp + 0.42 for c in range(5)]
        pl = VGroup(*[serif(pct[c], 32).move_to([xs[c], tops[c], 0]) for c in range(5)])
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.06) for p in pl], lag_ratio=0.12), run_time=0.9)
        self.wait(1.4)

        N.say("Only the uncertain middle goes to a physician.")
        unc = VGroup(*[dots[order[i]] for i in range(100) if assign[i][0] == 2])
        fr = SurroundingRectangle(VGroup(unc, pl[2]), color=P["amber"], buff=0.16, corner_radius=0.06, stroke_width=1.8)
        self.play(Create(fr), sc[2].animate.set_color(P["amber"]), nm[2].animate.set_color(P["amber"]), run_time=0.5)
        hum = station(i_person(), ring=P["amber"]).move_to([-5.9, 1.95, 0])
        hl = label("Physician review", "16% of events", align=LEFT).next_to(hum, RIGHT, buff=0.25)
        self.play(FadeIn(hum, scale=0.9), FadeIn(hl), run_time=0.45)
        self.play(unc.animate.arrange_in_grid(rows=2, cols=8, buff=0.07).scale(0.85).next_to(hum, DOWN, buff=0.35).align_to(hum, LEFT),
                  FadeOut(fr), FadeOut(pl[2]), run_time=1.1, rate_func=EASE)
        self.play(unc.animate.set_stroke(P["amber"]), run_time=0.25)
        out = VGroup(
            VGroup(serif("84%", 56), T("fewer committee reviews", 19, P["muted"])).arrange(DOWN, buff=0.02, aligned_edge=LEFT),
            VGroup(serif("91%", 56), T("agreement with the\nfull committee", 19, P["muted"])).arrange(DOWN, buff=0.02, aligned_edge=LEFT),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(unc, DOWN, buff=0.45).align_to(hum, LEFT)
        self.play(FadeIn(out[0], shift=UP * 0.06), run_time=0.45)
        self.play(FadeIn(out[1], shift=UP * 0.06), run_time=0.45)
        self.wait(2.8)


# =====================================================================
# FIG 5 — The trial result does not move
# =====================================================================
class Forest(Scene):
    def construct(self):
        self.add(kicker("Fig. 5 · Same trial result, either way"))
        N = Narrator(self, 2)
        x0, x1 = -1.9, 3.3
        lo, hi = np.log(0.6), np.log(1.2)
        X = lambda hr: x0 + (np.log(hr) - lo) / (hi - lo) * (x1 - x0)
        rows = [("head", "DELIVER", "HF hospitalization · dapagliflozin vs placebo"),
                ("row", "Committee", 0.77, 0.67, 0.89, "cec"),
                ("row", "AI · HF-NLP", 0.76, 0.66, 0.88, "ai"),
                ("gap",),
                ("head", "PARADISE-MI", "MACE · sacubitril/valsartan vs ramipril"),
                ("row", "Committee", 0.90, 0.77, 1.05, "cec"),
                ("row", "AI · Auto-MACE", 0.91, 0.78, 1.07, "ai"),
                ("row", "AI + physician review", 0.92, 0.79, 1.07, "hyb")]
        y, ys = 2.25, []
        for r in rows:
            if r[0] == "head":
                ys.append(y); y -= 0.7
            elif r[0] == "row":
                ys.append(y); y -= 0.58
            else:
                ys.append(None); y -= 0.3
        yb = y + 0.2
        axis = Line([x0, yb, 0], [x1, yb, 0], color=P["ink"], stroke_width=1.4)
        ticks = VGroup()
        for v in (0.6, 0.7, 0.8, 0.9, 1.0, 1.2):
            t = Line([X(v), yb, 0], [X(v), yb - 0.09, 0], color=P["ink"], stroke_width=1.4)
            ticks.add(t, mono(f"{v:.1f}", 16).next_to(t, DOWN, buff=0.08))
        null = DashedLine([X(1.0), 2.7, 0], [X(1.0), yb, 0], color=P["muted"], stroke_width=1.3, dash_length=0.07)
        nl = mono("NO DIFFERENCE", 13).next_to(null, UP, buff=0.1)
        xl = mono("HAZARD RATIO, LOG SCALE", 13).move_to([(x0 + x1) / 2, yb - 0.52, 0])
        fav = VGroup(T("← favors treatment", 17, P["muted"]).move_to([X(1.0) - 0.12, yb - 0.84, 0], aligned_edge=RIGHT),
                     T("favors control →", 17, P["muted"]).move_to([X(1.0) + 0.12, yb - 0.84, 0], aligned_edge=LEFT))
        hc = VGroup(mono("ADJUDICATED BY", 13).move_to([-6.6, 2.85, 0], aligned_edge=LEFT),
                    mono("HR (95% CI)", 13).move_to([3.85, 2.85, 0], aligned_edge=LEFT))
        N.say("Re-run each trial's primary analysis with AI-adjudicated events.")
        self.play(Create(axis), FadeIn(ticks), Create(null), FadeIn(nl), FadeIn(xl), FadeIn(hc), FadeIn(fav), run_time=0.8)
        cols = {"cec": P["ink"], "ai": P["accent"], "hyb": P["amber"]}
        for r, yy in zip(rows, ys):
            if r[0] == "head":
                h = VGroup(serif(r[1], 32), T(r[2], 18, P["muted"])).arrange(RIGHT, buff=0.28, aligned_edge=DOWN).move_to([-6.6, yy, 0], aligned_edge=LEFT)
                self.play(FadeIn(h, shift=RIGHT * 0.06), run_time=0.4)
            elif r[0] == "row":
                _, name, hr, a, b, k = r
                c = cols[k]
                nm = T(name, 21, P["ink"] if k == "cec" else c, weight=MEDIUM).move_to([-6.35, yy, 0], aligned_edge=LEFT)
                ci = Line([X(a), yy, 0], [X(b), yy, 0], color=c, stroke_width=2.2)
                caps = VGroup(*[Line([X(v), yy - 0.08, 0], [X(v), yy + 0.08, 0], color=c, stroke_width=2) for v in (a, b)])
                m = (Square(0.2, stroke_width=0, fill_color=c, fill_opacity=1) if k == "cec" else
                     Circle(radius=0.11, stroke_width=0, fill_color=c, fill_opacity=1)).move_to([X(hr), yy, 0])
                num = mono(f"{hr:.2f}  ({a:.2f}–{b:.2f})", 19, P["ink"] if k == "cec" else c).move_to([3.85, yy, 0], aligned_edge=LEFT)
                self.play(FadeIn(nm), Create(ci), FadeIn(caps), run_time=0.45)
                self.play(GrowFromCenter(m), FadeIn(num), run_time=0.3)
                if k == "ai" and name.endswith("NLP"):
                    N.say("The treatment effect barely moves.")
        self.wait(3.0)


# =====================================================================
# HERO — seamless loop
# =====================================================================
class Flow(Scene):
    def construct(self):
        TT, N = 10.0, 26
        R = 0.74
        cL = Circle(radius=R, stroke_color=P["ink"], stroke_width=LW, fill_color=P["soft"], fill_opacity=1).shift(LEFT * 0.4)
        cR = Circle(radius=R, stroke_color=P["ink"], stroke_width=LW, fill_opacity=0).shift(RIGHT * 0.4)
        lens = Intersection(cL, cR, stroke_width=0, fill_color=P["faint"], fill_opacity=1)
        gate = VGroup(cL, lens, cR)
        gl = mono("TWO INDEPENDENT AI READERS", 16).next_to(gate, DOWN, buff=0.32)
        x_in0, x_in1 = -7.6, -1.05
        exit_pt = np.array([1.0, 0, 0])
        laneY = {"acc": 1.5, "rej": -1.5, "unc": 0.0}
        hum_pos = np.array([5.15, 0, 0])

        def lane(cat):
            if cat == "unc":
                return Line(exit_pt, hum_pos + LEFT * 0.52)
            yy = laneY[cat]
            c = CubicBezier(exit_pt, exit_pt + RIGHT * 1.4, np.array([2.4, yy, 0]), np.array([3.6, yy, 0]))
            l = Line(np.array([3.6, yy, 0]), np.array([7.7, yy, 0]))
            p = VMobject(); p.append_points(c.points); p.append_points(l.points)
            return p
        paths = {c: lane(c) for c in ("acc", "rej", "unc")}
        guides = VGroup(*[paths[c].copy().set_stroke(P["rule"], 1.3) for c in paths])
        ing = VGroup(*[Line([x_in0, yy, 0], [x_in1 - 0.2, yy * 0.15, 0], stroke_color=P["rule"], stroke_width=1.3) for yy in (0.5, 0, -0.5)])
        hum = station(i_person(0.52), r=0.48, ring=P["amber"]).move_to(hum_pos)
        labs = VGroup(mono("CONFIDENT · EVENT", 15, P["ink"]).move_to([3.75, laneY["acc"] + 0.34, 0], aligned_edge=LEFT),
                      mono("UNCERTAIN · HUMAN REVIEW", 15, P["amber"]).next_to(hum, DOWN, buff=0.2),
                      mono("CONFIDENT · NO EVENT", 15, P["ink"]).move_to([3.75, laneY["rej"] - 0.34, 0], aligned_edge=LEFT))
        pat = ["acc", "rej", "acc", "acc", "unc", "acc", "rej", "acc", "rej", "acc", "unc", "acc", "acc",
               "rej", "acc", "acc", "unc", "rej", "acc", "acc", "rej", "acc", "unc", "acc", "rej", "acc"]
        lanes_in = [0.5, 0.0, -0.5]
        t = ValueTracker(0.0)
        parts = []
        for i in range(N):
            cat = pat[i]
            w, h = 0.3, 0.4
            doc = VGroup(Rectangle(width=w, height=h, stroke_color=P["ink"], stroke_width=1.5, fill_color=P["soft"], fill_opacity=1),
                         *[Line((-w/2 + 0.06, h/2 - 0.1 - k * 0.09, 0), (w/2 - 0.06 - (0.06 if k == 2 else 0), h/2 - 0.1 - k * 0.09, 0),
                                stroke_width=1.2, color=P["muted"]) for k in range(3)])
            if cat == "acc":
                dot = Circle(radius=0.095, stroke_color=P["ink"], stroke_width=1.5, fill_color=P["ink"], fill_opacity=1)
            elif cat == "rej":
                dot = Circle(radius=0.095, stroke_color=P["ink"], stroke_width=1.5, fill_color=P["soft"], fill_opacity=1)
            else:
                dot = Circle(radius=0.095, stroke_color=P["amber"], stroke_width=1.5, fill_color=P["amber"], fill_opacity=1)
            yl, phi = lanes_in[i % 3], i / N

            def ud(m, phi=phi, yl=yl):
                s = (t.get_value() / TT + phi) % 1.0
                if s < 0.5:
                    u = s / 0.5
                    m.move_to([x_in0 + (x_in1 - x_in0) * u, yl * (1 - u) + yl * 0.15 * u, 0])
                    m.set_opacity(1.0 if u < 0.88 else max(0.0, (1 - u) / 0.12))
                else:
                    m.set_opacity(0)

            def ut(m, phi=phi, cat=cat):
                s = (t.get_value() / TT + phi) % 1.0
                if s >= 0.56:
                    u = (s - 0.56) / 0.44
                    m.move_to(paths[cat].point_from_proportion(min(u, 1.0)))
                    op = min(1.0, u / 0.08)
                    if cat == "unc" and u > 0.85:
                        op = max(0.0, (1 - u) / 0.15)
                    m.set_opacity(op)
                else:
                    m.set_opacity(0)
            doc.add_updater(ud); dot.add_updater(ut)
            ud(doc); ut(dot)
            parts += [doc, dot]
        self.add(ing, guides, *parts, gate, gl, hum, labs)
        self.play(t.animate.set_value(TT - 1 / config.frame_rate), run_time=TT - 1 / config.frame_rate, rate_func=linear)


# =====================================================================
# FIG 6 — Anjana, the adjudicator's cockpit (sketch)
# =====================================================================
def mark(s=0.22):
    a = Circle(radius=s, stroke_color=P["ink"], stroke_width=1.6).shift(LEFT * s * 0.55)
    b = Circle(radius=s, stroke_color=P["ink"], stroke_width=1.6).shift(RIGHT * s * 0.55)
    lens = Intersection(a, b, stroke_width=0, fill_color=P["amber"], fill_opacity=1)
    return VGroup(lens, a, b)


def bar(w, h=0.07, c=None, op=1.0):
    return Rectangle(width=w, height=h, stroke_width=0, fill_color=c or P["rule"], fill_opacity=op)


def cross(size=0.16, color=None):
    c = color or P["muted"]
    return VGroup(Line(UL * size / 2, DR * size / 2, stroke_width=1.6, color=c), Line(UR * size / 2, DL * size / 2, stroke_width=1.6, color=c))


class App(Scene):
    def construct(self):
        self.add(kicker("Fig. 6 · Anjana, the adjudicator's cockpit"))
        N = Narrator(self, 5)
        W = RoundedRectangle(corner_radius=0.1, width=13.2, height=6.1, stroke_color=P["ink"], stroke_width=1.4,
                             fill_color=P["soft"], fill_opacity=1).move_to([0, 0.12, 0])
        L, R, TOP, BOT = W.get_left()[0], W.get_right()[0], W.get_top()[1], W.get_bottom()[1]
        topbar = Line([L, TOP - 0.5, 0], [R, TOP - 0.5, 0], stroke_width=1, color=P["rule"])
        brand = VGroup(mark(0.13), serif("Anjana", 24, P["ink"], ITALIC)).arrange(RIGHT, buff=0.16).move_to([L + 0.35, TOP - 0.25, 0], aligned_edge=LEFT)
        crumbs = mono("DEMO TRIAL · ADJUDICATOR WORKSPACE", 13).move_to([R - 0.35, TOP - 0.25, 0], aligned_edge=RIGHT)
        side_x = L + 2.05
        side = Line([side_x, TOP - 0.5, 0], [side_x, BOT, 0], stroke_width=1, color=P["rule"])
        nav = VGroup(
            VGroup(Square(0.12, stroke_width=0, fill_color=P["ink"], fill_opacity=1), T("My queue", 17, weight=MEDIUM)).arrange(RIGHT, buff=0.16),
            VGroup(Square(0.12, stroke_width=1, stroke_color=P["muted"]), T("Discussion", 17, P["muted"])).arrange(RIGHT, buff=0.16),
            VGroup(Square(0.12, stroke_width=1, stroke_color=P["muted"]), T("Signed", 17, P["muted"])).arrange(RIGHT, buff=0.16),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([L + 0.35, TOP - 1.1, 0], aligned_edge=UL)
        chrome = VGroup(W, topbar, brand, crumbs, side, nav)

        # ---------- view 1: queue ----------
        qx0, qx1 = side_x + 0.3, R - 4.0
        pv_x = R - 3.75
        pv_line = Line([R - 3.95, TOP - 0.5, 0], [R - 3.95, BOT, 0], stroke_width=1, color=P["rule"])
        qhead = VGroup(mono("TO REVIEW", 14, P["ink"]), mono("8", 14)).arrange(RIGHT, buff=0.2).move_to([qx0, TOP - 0.85, 0], aligned_edge=LEFT)
        events = [("Q3RT", "CV DEATH", "yes", "AI · CV death"), ("M8LD", "HF HOSP.", "no", "AI · reject"),
                  ("A7K2", "HF HOSP.", "no", "AI · reject"), ("V2NE", "HF HOSP.", "unc", "Uncertain"),
                  ("C9WA", "CV DEATH", "yes", "AI · CV death"), ("H4PX", "HF HOSP.", "yes", "AI · confirm"),
                  ("T6JB", "CV DEATH", "unc", "Uncertain"), ("K1SZ", "HF HOSP.", "no", "AI · reject")]
        rows = VGroup()
        for k, (code, typ, kind, rec) in enumerate(events):
            y = TOP - 1.35 - k * 0.52
            dot = Square(0.15, stroke_width=0, fill_color=P["amber"] if kind == "unc" else P["muted"], fill_opacity=1).move_to([qx0 + 0.08, y, 0])
            c = mono(code, 16, P["ink"], MEDIUM).next_to(dot, RIGHT, buff=0.2)
            ty = mono(typ, 13).move_to([qx0 + 1.5, y, 0], aligned_edge=LEFT)
            pb = bar(1.5, 0.08, P["rule"]).move_to([qx0 + 3.0, y, 0], aligned_edge=LEFT)
            tg = tag(rec, kind, 13).move_to([qx1 - 0.1, y, 0], aligned_edge=RIGHT)
            sep = Line([qx0 - 0.1, y - 0.26, 0], [qx1, y - 0.26, 0], stroke_width=0.8, color=P["faint"])
            rows.add(VGroup(dot, c, ty, pb, tg, sep))
        pv = VGroup(
            mono("PREVIEW", 13),
            T("Event A7K2", 22, weight=MEDIUM),
            mono("HF HOSPITALIZATION · AI: REJECT", 13),
            VGroup(*[bar(w, 0.07, P["rule"]) for w in (3.2, 3.0, 3.3, 2.6, 3.1, 2.2)]).arrange(DOWN, buff=0.17, aligned_edge=LEFT),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([pv_x, TOP - 0.8, 0], aligned_edge=UL)
        btn_open = VGroup(RoundedRectangle(corner_radius=0.06, width=1.7, height=0.44, stroke_width=0, fill_color=P["ink"], fill_opacity=1),
                          T("Open cockpit", 16, P["plate"], weight=MEDIUM))
        btn_open[1].move_to(btn_open[0])
        btn_form = VGroup(RoundedRectangle(corner_radius=0.06, width=1.6, height=0.44, stroke_width=1.2, stroke_color=P["ink"], fill_opacity=0),
                          T("Decision form", 16, weight=MEDIUM))
        btn_form[1].move_to(btn_form[0])
        btns = VGroup(btn_open, btn_form).arrange(RIGHT, buff=0.18).next_to(pv, DOWN, buff=0.35).align_to(pv, LEFT)

        N.say("The adjudicator's queue arrives pre-read by AI.")
        self.play(FadeIn(chrome), run_time=0.6)
        self.play(FadeIn(qhead), Create(pv_line), LaggedStart(*[FadeIn(r, shift=UP * 0.05) for r in rows], lag_ratio=0.08), run_time=1.2)
        sel = SurroundingRectangle(rows[2][:5], color=P["ink"], buff=0.12, stroke_width=1.6, corner_radius=0.05)
        self.play(Create(sel), run_time=0.4)
        self.play(FadeIn(pv, shift=LEFT * 0.06), FadeIn(btns, shift=LEFT * 0.06), run_time=0.6)
        self.wait(0.6)
        pulse(self, btn_open, 1.08, 0.35)
        queue_view = VGroup(qhead, rows, sel, pv, btns, pv_line)
        self.play(FadeOut(queue_view), run_time=0.45)

        # ---------- view 2: cockpit ----------
        dx0, dx1 = side_x + 0.3, R - 4.9
        sheet = Rectangle(width=dx1 - dx0, height=(TOP - 0.75) - (BOT + 0.25), stroke_color=P["rule"], stroke_width=1,
                          fill_color=P["plate"], fill_opacity=0.35).move_to([(dx0 + dx1) / 2, ((TOP - 0.75) + (BOT + 0.25)) / 2, 0])
        sl, st = sheet.get_left()[0], sheet.get_top()[1]
        pager = mono("‹  PAGE 1 OF 23  ›", 12).move_to([(dx0 + dx1) / 2, TOP - 0.62, 0])
        red = VGroup(bar(1.6, 0.34, P["redact"]).move_to([sl + 0.35, st - 0.4, 0], aligned_edge=UL),
                     bar(2.1, 0.22, P["redact"]).move_to([sl + 2.15, st - 0.35, 0], aligned_edge=UL),
                     bar(1.3, 0.34, P["redact"]).move_to([sl + 4.4, st - 0.4, 0], aligned_edge=UL))
        dtitle = serif("DISCHARGE SUMMARY", 19).move_to([(dx0 + dx1) / 2, st - 1.15, 0])
        dul = Line(dtitle.get_corner(DL) + DOWN * 0.05, dtitle.get_corner(DR) + DOWN * 0.05, stroke_width=1, color=P["ink"])
        fields = VGroup(*[VGroup(bar(0.9, 0.06, P["muted"]), bar(1.4 if k % 2 else 0.9, 0.18, P["redact"]) if k in (1, 2) else bar(1.2, 0.06, P["rule"])).arrange(RIGHT, buff=0.15)
                          for k in range(4)]).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to([sl + 0.4, st - 1.55, 0], aligned_edge=UL)
        dx_lines = VGroup(*[bar(w, 0.06, P["rule"]) for w in (3.6, 3.3, 3.8, 2.9, 3.5)]).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        dx_lines.move_to([sl + 0.4, st - 2.55, 0], aligned_edge=UL)
        quote = T("… was admitted on an elective basis for", 18, P["ink"], SERIF)
        quote.move_to([sl + 0.4, st - 3.6, 0], aligned_edge=LEFT)
        more = VGroup(*[bar(w, 0.06, P["rule"]) for w in (3.7, 3.4)]).arrange(DOWN, buff=0.14, aligned_edge=LEFT).next_to(quote, DOWN, buff=0.2).align_to(quote, LEFT)
        doc = VGroup(sheet, pager, red, dtitle, dul, fields, dx_lines, quote, more)

        px = R - 4.6
        pline = Line([R - 4.75, TOP - 0.5, 0], [R - 4.75, BOT, 0], stroke_width=1, color=P["rule"])
        rec = VGroup(mono("AI RECOMMENDATION", 13), T("Reject HF hospitalization", 23, weight=MEDIUM),
                     T("Chronic HF with edema and reduced EF,\nbut the admission was elective, not urgent.", 16, P["muted"])
                     ).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to([px, TOP - 0.8, 0], aligned_edge=UL)
        crit_def = [("Primary diagnosis", P["amber"], 1, 1), ("Encounter qualification", P["accent"], 0, 2),
                    ("Duration", P["ink"], 1, 0), ("Objective confirmation", P["ink"], 2, 3),
                    ("Symptoms", P["ink"], 3, 1), ("Treatment", P["ink"], 1, 2)]
        crit_h = mono("CRITERIA · EVIDENCE FOR / AGAINST", 12).next_to(rec, DOWN, buff=0.38).align_to(rec, LEFT)
        crit = VGroup()
        for k, (nm, col, f, a) in enumerate(crit_def):
            y = crit_h.get_bottom()[1] - 0.38 - k * 0.42
            d = Dot([px + 0.06, y, 0], radius=0.06, color=col)
            t = T(nm, 16).move_to([px + 0.28, y, 0], aligned_edge=LEFT)
            cnt = VGroup(tick(0.16, P["muted"], 1.6), mono(str(f), 14, P["ink"]), cross(0.13), mono(str(a), 14, P["ink"])).arrange(RIGHT, buff=0.09)
            cnt[2].shift(RIGHT * 0.1); cnt[3].shift(RIGHT * 0.1)
            cnt.move_to([R - 0.35, y, 0], aligned_edge=RIGHT)
            crit.add(VGroup(d, t, cnt))
        panel = VGroup(pline, rec, crit_h, crit)

        N.say("Open a case: the source dossier beside the AI's recommendation.")
        self.play(FadeIn(doc, shift=RIGHT * 0.05), run_time=0.6)
        self.play(Create(pline), FadeIn(rec, shift=LEFT * 0.05), run_time=0.5)
        self.play(FadeIn(crit_h), LaggedStart(*[FadeIn(c, shift=LEFT * 0.05) for c in crit], lag_ratio=0.1), run_time=0.9)
        self.wait(0.6)

        N.say("Every criterion links to the sentences behind it.")
        row = crit[1]
        hi = Rectangle(width=(R - 0.2) - (px - 0.15), height=0.36, stroke_width=0, fill_color=P["faint"], fill_opacity=1)
        hi.move_to([(R - 0.2 + px - 0.15) / 2, row.get_center()[1], 0]).set_z_index(-1)
        self.add(hi)
        self.play(FadeIn(hi), run_time=0.3)
        wash = Rectangle(width=quote.width + 0.14, height=0.36, stroke_width=0, fill_color=P["wash"], fill_opacity=1).move_to(quote).set_z_index(-1)
        und = Line(quote.get_corner(DL) + DOWN * 0.06, quote.get_corner(DR) + DOWN * 0.06, stroke_width=1.8, color=P["amber"])
        p0 = row[0].get_left() + LEFT * 0.12
        p1 = quote.get_right() + RIGHT * 0.12
        link = CubicBezier(p0, p0 + LEFT * 0.9, p1 + RIGHT * 0.9, p1, stroke_color=P["amber"], stroke_width=1.6)
        self.play(Create(link), run_time=0.55)
        self.add(wash)
        self.play(FadeIn(wash), Create(und), run_time=0.35)
        self.wait(1.4)
        self.play(FadeOut(link), run_time=0.3)

        # ---------- view 3: decision form ----------
        N.say("The adjudicator confirms or overrides, then signs.")
        form_h = mono("DECISION · IN REVIEW", 13).move_to([px, TOP - 0.8, 0], aligned_edge=UL)
        qs = [("Heart failure event confirmed?", "No"), ("Event classification", "Not an HF hospitalization"),
              ("Documentation", "Adequate"), ("Flag for discussion?", "No")]
        boxes, vals = VGroup(), VGroup()
        for k, (q, a) in enumerate(qs):
            top_y = form_h.get_bottom()[1] - 0.25 - k * 0.86
            bx = Rectangle(width=4.2, height=0.72, stroke_color=P["rule"], stroke_width=1, fill_color=P["soft"], fill_opacity=1)
            bx.move_to([px - 0.02, top_y, 0], aligned_edge=UL)
            ql = T(q, 14, P["muted"]).move_to(bx.get_corner(UL) + np.array([0.16, -0.2, 0]), aligned_edge=LEFT)
            av = T(a, 17, weight=MEDIUM).move_to(bx.get_corner(UL) + np.array([0.16, -0.5, 0]), aligned_edge=LEFT)
            boxes.add(VGroup(bx, ql)); vals.add(av)
        b_draft = VGroup(RoundedRectangle(corner_radius=0.06, width=1.35, height=0.44, stroke_width=1.2, stroke_color=P["ink"]), T("Save draft", 15, weight=MEDIUM))
        b_draft[1].move_to(b_draft[0])
        b_sign = VGroup(RoundedRectangle(corner_radius=0.06, width=1.6, height=0.44, stroke_width=0, fill_color=P["ink"], fill_opacity=1), T("Sign and save", 15, P["plate"], weight=MEDIUM))
        b_sign[1].move_to(b_sign[0])
        fb = VGroup(b_draft, b_sign).arrange(RIGHT, buff=0.16).move_to([R - 0.3, BOT + 0.45, 0], aligned_edge=RIGHT)
        self.play(FadeOut(VGroup(rec, crit_h, crit, hi), shift=LEFT * 0.05), run_time=0.4)
        self.play(FadeIn(form_h), LaggedStart(*[FadeIn(b, shift=UP * 0.04) for b in boxes], lag_ratio=0.1), FadeIn(fb), run_time=0.8)
        for v in vals:
            self.play(FadeIn(v, shift=RIGHT * 0.05), run_time=0.28)
        self.wait(0.3)
        pulse(self, b_sign, 1.08, 0.35)
        signed = VGroup(tick(0.2, P["ink"], 2), mono("SIGNED", 13, P["ink"])).arrange(RIGHT, buff=0.12).next_to(fb, UP, buff=0.22).align_to(fb, RIGHT)
        self.play(FadeIn(signed, shift=RIGHT * 0.05), run_time=0.35)
        self.wait(0.8)

        # ---------- view 4: back to queue ----------
        N.say("Then on to the next case.")
        self.play(FadeOut(VGroup(doc, pline, form_h, boxes, vals, fb, signed, wash, und)), run_time=0.45)
        rows[2][4].become(tag("Signed", "no", 13).move_to(rows[2][4], aligned_edge=RIGHT))
        rows[2][4][0].set_stroke(P["muted"]).set_fill(P["soft"])
        rows[2][4][1].set_color(P["muted"])
        sel2 = SurroundingRectangle(rows[3][:5], color=P["ink"], buff=0.12, stroke_width=1.6, corner_radius=0.05)
        self.play(FadeIn(qhead), Create(pv_line), FadeIn(rows), run_time=0.5)
        self.play(Create(sel2), run_time=0.4)
        pv2 = VGroup(mono("PREVIEW", 13), T("Event V2NE", 22, weight=MEDIUM), mono("HF HOSPITALIZATION · UNCERTAIN", 13, P["amber"]),
                     VGroup(*[bar(w, 0.07, P["rule"]) for w in (3.1, 3.3, 2.8, 3.2, 2.4)]).arrange(DOWN, buff=0.17, aligned_edge=LEFT)
                     ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([pv_x, TOP - 0.8, 0], aligned_edge=UL)
        self.play(FadeIn(pv2, shift=LEFT * 0.05), FadeIn(btns), run_time=0.5)
        self.wait(2.4)
