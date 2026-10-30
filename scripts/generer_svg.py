"""Génère les SVG du README de profil (style plan d'ingénieur : planches, cotes, cartouches).

Usage : python3 scripts/generer_svg.py assets
L'ancien style « affiche » est sur la branche design-affiche.
"""
import os, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

BG, BG2 = "#123a7a", "#0f3270"
LINE, FAINT = "#eaf2ff", "rgba(234,242,255,.55)"
CYAN, GOLD, CORAL = "#7fd3ff", "#ffd166", "#ff8a7a"
SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Menlo, Consolas, 'Liberation Mono', monospace"

CSS = f"""
.s{{font-family:{SANS}}} .m{{font-family:{MONO}}}
.d{{fill:none; stroke:{LINE}; stroke-width:2; stroke-linecap:round; stroke-linejoin:round;
   stroke-dasharray:1; stroke-dashoffset:1; animation:draw 1.6s cubic-bezier(.55,.1,.35,1) forwards}}
.dc{{stroke:{CORAL}; stroke-width:2.5}}
.dim{{fill:none; stroke:{CYAN}; stroke-width:1.2; stroke-dasharray:1; stroke-dashoffset:1; animation:draw 1s ease forwards}}
.in{{opacity:0; animation:in .6s ease forwards}}
.pop{{opacity:0; transform-box:fill-box; transform-origin:center; animation:pop .5s cubic-bezier(.3,1.45,.5,1) forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
@keyframes in{{from{{opacity:0}} to{{opacity:1}}}}
@keyframes pop{{from{{opacity:0; transform:scale(.2)}} to{{opacity:1; transform:scale(1)}}}}
@keyframes blink{{50%{{opacity:.2}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
"""


def svg(w, h, body, css="", label=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{label}">\n<style>{CSS}{css}</style>\n{body}\n</svg>\n')


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;")


def P(d, delay=0.0, cls="d", extra=""):
    """Tracé qui se dessine tout seul."""
    return f'<path d="{d}" pathLength="1" class="{cls}" style="animation-delay:{delay:.2f}s" {extra}/>'


def sheet(W, H):
    """Fond quadrillé, cadre double et graduations."""
    b = [f'<defs><pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse">'
         f'<path d="M20 0H0V20" fill="none" stroke="rgba(234,242,255,.07)"/></pattern>'
         f'<pattern id="G" width="100" height="100" patternUnits="userSpaceOnUse">'
         f'<path d="M100 0H0V100" fill="none" stroke="rgba(234,242,255,.14)"/></pattern></defs>',
         f'<rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#g)"/>'
         f'<rect width="{W}" height="{H}" fill="url(#G)"/>',
         f'<rect x="12" y="12" width="{W - 24}" height="{H - 24}" fill="none" stroke="{LINE}" stroke-width="2.5"/>',
         f'<rect x="20" y="20" width="{W - 40}" height="{H - 40}" fill="none" stroke="{FAINT}" stroke-width="1"/>']
    ticks = "".join(f"M{x} 12V20M{x} {H - 20}V{H - 12}" for x in range(100, W, 100)) \
        + "".join(f"M12 {y}H20M{W - 20} {y}H{W - 12}" for y in range(100, H, 100))
    b.append(f'<path d="{ticks}" stroke="{LINE}" stroke-width="1.5"/>')
    return "".join(b)


def cartouche(x, y, cells, widths, h=56):
    """Cartouche de plan : rangée de cases étiquette / valeur."""
    out = ['<g class="in" style="animation-delay:.6s">']
    cx = x
    for (lab, val), w in zip(cells, widths):
        out.append(f'<rect x="{cx}" y="{y}" width="{w}" height="{h}" fill="{BG2}" stroke="{LINE}" stroke-width="1.5"/>'
                   f'<text x="{cx + 12}" y="{y + 19}" class="m" font-size="10.5" letter-spacing="1.5" fill="{CYAN}">{esc(lab)}</text>'
                   f'<text x="{cx + 12}" y="{y + 42}" class="m" font-size="13.5" fill="{LINE}">{esc(val)}</text>')
        cx += w
    out.append('</g>')
    return "".join(out)


def dimh(x1, x2, y, label, delay):
    """Cote horizontale."""
    mid = (x1 + x2) / 2
    return (P(f"M{x1:.0f} {y - 8}V{y + 8}M{x2:.0f} {y - 8}V{y + 8}M{x1:.0f} {y}H{x2:.0f}", delay, "dim")
            + P(f"M{x1 + 9:.0f} {y - 4}L{x1:.0f} {y}L{x1 + 9:.0f} {y + 4}M{x2 - 9:.0f} {y - 4}L{x2:.0f} {y}L{x2 - 9:.0f} {y + 4}", delay, "dim")
            + f'<rect x="{mid - len(label) * 4.2 - 6:.0f}" y="{y - 9}" width="{len(label) * 8.4 + 12:.0f}" height="18" fill="{BG}" class="in" style="animation-delay:{delay + .4:.2f}s"/>'
            + f'<text x="{mid:.0f}" y="{y + 4}" text-anchor="middle" class="m in" font-size="12" fill="{CYAN}" style="animation-delay:{delay + .4:.2f}s">{esc(label)}</text>')


def dimv(x, y1, y2, label, delay):
    """Cote verticale."""
    mid = (y1 + y2) / 2
    return (P(f"M{x - 8} {y1}H{x + 8}M{x - 8} {y2}H{x + 8}M{x} {y1}V{y2}", delay, "dim")
            + P(f"M{x - 4} {y1 + 9}L{x} {y1}L{x + 4} {y1 + 9}M{x - 4} {y2 - 9}L{x} {y2}L{x + 4} {y2 - 9}", delay, "dim")
            + f'<text x="{x + 12}" y="{mid + 4:.0f}" class="m in" font-size="12" fill="{CYAN}" style="animation-delay:{delay + .4:.2f}s">{esc(label)}</text>')


def note(x, y, tx, ty, text, delay):
    """Ligne de rappel avec annotation, écrite à gauche du point de rappel."""
    return (P(f"M{x} {y}L{tx} {ty}H{tx - 50}", delay, "dim")
            + f'<circle cx="{x}" cy="{y}" r="3.5" fill="{GOLD}" class="pop" style="animation-delay:{delay:.2f}s"/>'
            + f'<text x="{tx - 56}" y="{ty + 4}" text-anchor="end" class="m in" font-size="13" fill="{GOLD}" style="animation-delay:{delay + .5:.2f}s">{esc(text)}</text>')


# ---------------------------------------------------------------- bannière
def header():
    W, H = 1200, 440
    b = [sheet(W, H)]
    b.append(f'<text x="56" y="76" class="m in" font-size="13" letter-spacing="3" fill="{CYAN}">PLANCHE 00 / 05 · PROFIL</text>')
    b.append(f'<text x="54" y="150" class="m in" font-size="62" font-weight="700" letter-spacing="2" textLength="600" '
             f'lengthAdjust="spacingAndGlyphs" fill="{LINE}" style="animation-delay:.15s">FLORIENT MARCHAL</text>')
    b.append(P("M56 172H654", .5))
    b.append(f'<text x="56" y="212" class="s in" font-size="21" fill="{LINE}" style="animation-delay:.4s">'
             'Étudiant en M1 MIASHS. Statistiques, IA et web :</text>')
    b.append(f'<text x="56" y="242" class="s in" font-size="21" font-weight="700" fill="{GOLD}" style="animation-delay:.5s">'
             'je conçois des outils à partir de données.</text>')
    b.append(cartouche(56, 312, [("DESSINÉ PAR", "F. MARCHAL"), ("FORMATION", "M1 MIASHS"),
                                 ("LIEU", "MONTPELLIER"), ("ÉCHELLE", "1:1")], [160, 150, 160, 128], h=60))
    # dessin technique : cercle, nuage de points, droite ajustée
    cx, cy, r = 935, 205, 150
    b.append(P(f"M{cx - r} {cy}a{r} {r} 0 1 0 {2 * r} 0a{r} {r} 0 1 0 {-2 * r} 0", .2))
    b.append(P(f"M{cx - r - 25} {cy}H{cx + r + 25}M{cx} {cy - r - 25}V{cy + r + 25}", .3, "dim"))
    pts = [(-110, 70), (-80, 40), (-60, 62), (-30, 18), (-5, 30), (20, -8), (45, 6), (70, -40), (95, -28), (115, -70)]
    for i, (dx, dy) in enumerate(pts):
        b.append(f'<circle cx="{cx + dx}" cy="{cy + dy}" r="5" fill="{GOLD if i in (3, 7) else LINE}" class="pop" '
                 f'style="animation-delay:{1 + i * .08:.2f}s"/>')
    b.append(P(f"M{cx - 135} {cy + 78}L{cx + 135} {cy - 82}", 1.9, "d dc"))
    b.append(note(cx - 110, cy + 70, cx - 160, cy + 92, "ŷ = β₀ + β₁x", 2.4))
    b.append(dimh(cx - r, cx + r, cy + r + 40, "Ø 300", 1.2))
    b.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="none" stroke="{GOLD}" stroke-width="2" style="animation:blink 1.6s infinite"/>')
    return svg(W, H, "\n".join(b), label="Florient Marchal, étudiant en M1 MIASHS : statistiques, IA et web")


# ---------------------------------------------------------------- planches de projets
def plate(num, title, desc, label, points, cells, widths, art, css="", H=470, alt=""):
    W = 1200
    b = [sheet(W, H), f'<line x1="430" y1="20" x2="430" y2="{H - 20}" stroke="{FAINT}" stroke-width="1"/>',
         f'<g>{art}</g>',
         f'<text x="40" y="52" class="m in" font-size="12" letter-spacing="3" fill="{CYAN}">PLANCHE {num} / 05</text>',
         f'<text x="460" y="74" class="m in" font-size="38" font-weight="700" letter-spacing="1" fill="{LINE}" style="animation-delay:.1s">{esc(title.upper())}</text>',
         P(f"M462 90H{462 + len(title) * 23.8:.0f}", .4)]
    y = 126
    for ln in desc:
        b.append(f'<text x="460" y="{y}" class="s in" font-size="16.5" fill="{LINE}" style="animation-delay:.2s">{esc(ln)}</text>')
        y += 25
    if points:
        y += 18
        b.append(f'<text x="460" y="{y}" class="m in" font-size="11.5" letter-spacing="3" fill="{GOLD}" style="animation-delay:.3s">{esc(label)}</text>')
        y += 30
        for i, p in enumerate(points):
            d = .4 + i * .12
            b.append(f'<text x="460" y="{y}" class="m in" font-size="13" font-weight="700" fill="{GOLD}" style="animation-delay:{d:.2f}s">{"ABC"[i]}</text>'
                     f'<text x="486" y="{y}" class="s in" font-size="16" fill="{LINE}" style="animation-delay:{d:.2f}s">{esc(p)}</text>')
            y += 29
    b.append(cartouche(460, H - 96, cells, widths))
    return svg(W, H, "\n".join(b), css, alt)


def projects():
    out = {}
    # 01 : dé en perspective isométrique, bille qui roule sur une trajectoire
    cx, cy, s = 215, 265, 100
    k = s * .87
    top = [(cx, cy - s), (cx + k, cy - s / 2), (cx, cy), (cx - k, cy - s / 2)]
    path = "M" + "L".join(f"{x:.0f} {y:.0f}" for x, y in top) + "Z"
    path += f"M{cx - k:.0f} {cy - s / 2:.0f}V{cy + s / 2:.0f}L{cx} {cy + s:.0f}L{cx + k:.0f} {cy + s / 2:.0f}V{cy - s / 2:.0f}M{cx} {cy}V{cy + s:.0f}"
    pips = [(cx, cy - s / 2, 0),
            (cx - k * .3, cy - s * .15 + s * .2, 1), (cx - k * .7, cy - s * .35 + s * .6, 1),
            (cx + k * .25, cy - s * .125 + s * .2, 2), (cx + k * .5, cy - s * .25 + s * .45, 2), (cx + k * .75, cy - s * .375 + s * .7, 2)]
    skew = lambda f, x, y: "" if f == 0 else f'transform="skewY({30 if f == 1 else -30} {x:.0f} {y:.0f})" '
    pipsvg = "".join(
        f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{12 if f == 0 else 7}" ry="{7 if f == 0 else 10}" '
        f'{skew(f, x, y)}'
        f'fill="{GOLD}" class="pop" style="animation-delay:{1.4 + i * .1:.2f}s"/>'
        for i, (x, y, f) in enumerate(pips))
    orbit = "M60 150C110 80 320 80 370 150"
    art = (P(path, .2) + pipsvg + P(orbit, 1.0, "dim")
           + f'<circle r="7" fill="{CORAL}"><animateMotion dur="3s" begin="0s" repeatCount="indefinite" path="{orbit}"/></circle>'
           + dimh(cx - k, cx + k, cy + s + 36, "13 JEUX", 1.0))
    out["01-casino"] = plate(
        "01", "Casino Fantôme",
        ["Un simulateur de casino 100 % fictif : 13 jeux à débloquer, niveaux, classement",
         "et boutique. Tout le code est écrit par des agents IA, pilotés et relus par la promo."],
        "MA PART · GROUPE 4, APPLICATION",
        ["Les écrans Lobby, Profil, Classement, création de profil et page 404",
         "L'intégration des 11 interfaces de jeu du groupe 3 dans la page de jeu",
         "24 pull requests fusionnées, 7 revues de code et une vingtaine d'issues"],
        [("CONTEXTE", "COURS DE PROGRAMMATION AGENTIQUE"), ("ÉQUIPE", "~25 ÉTUDIANTS"), ("STACK", "REACT · VITE")],
        [320, 160, 220], art,
        alt="Planche 01, Casino Fantôme : simulateur de casino fictif, cours de programmation agentique")

    # 02 : schéma du pipeline de l'assistant
    boxes = ["QUESTION CLIENT", "CAMEMBERT · INTENTION", "RAG · QDRANT", "LLM · OLLAMA"]
    art = ""
    for i, t in enumerate(boxes):
        y = 80 + i * 80
        art += P(f"M70 {y}H360V{y + 46}H70Z", .2 + i * .25)
        art += (f'<text x="215" y="{y + 28}" text-anchor="middle" class="m in" font-size="13" letter-spacing="1" fill="{LINE}" '
                f'style="animation-delay:{.6 + i * .25:.2f}s">{t}</text>')
        if i < 3:
            art += P(f"M215 {y + 46}V{y + 80}M209 {y + 72}L215 {y + 80}L221 {y + 72}", .45 + i * .25, "dim")
    art += f'<circle r="6" fill="{GOLD}"><animateMotion dur="2.6s" begin="0s" repeatCount="indefinite" path="M215 103V343"/></circle>'
    art += P("M360 343C400 343 400 400 360 400H90", 1.4, "dim")
    art += f'<text x="70" y="430" class="m in" font-size="12" letter-spacing="1" fill="{GOLD}" style="animation-delay:1.8s">→ RÉPONSE · 75 LANGUES</text>'
    out["02-pairia"] = plate(
        "02", "PairIA",
        ["Une boutique de chaussures en ligne complète, avec un assistant conversationnel",
         "qui tourne entièrement en local : aucune API payante, que des modèles open source."],
        "CE QUE FAIT LE PROJET",
        ["Chatbot client : recherche en langage naturel, par photo (CLIP) ou à la voix",
         "Chatbot admin : il gère la boutique en langage naturel avec 25 outils",
         "Pipeline RAG sur Qdrant, intentions classées par un CamemBERT affiné"],
        [("CONTEXTE", "PROJET DE STAGE"), ("ÉQUIPE", "3 PERSONNES"), ("STACK", "PYTHON · FASTAPI · PHP")],
        [200, 170, 330], art,
        alt="Planche 02, PairIA : boutique de chaussures en ligne avec assistant IA local, projet de stage")

    # 03 : plante cotée, courbe de température, soleil
    rays = "".join(f'<line x1="330" y1="58" x2="330" y2="48" stroke="{GOLD}" stroke-width="2" transform="rotate({a} 330 90)"/>'
                   for a in range(0, 360, 45))
    art = (P("M60 420H370", .2)
           + P("M200 420V250", .4)
           + P("M200 330C170 330 145 312 140 285C170 285 195 300 200 330", .9)
           + P("M200 300C228 300 252 282 258 254C228 254 205 270 200 300", 1.1)
           + P("M200 260C188 240 190 220 200 205C210 220 212 240 200 260", 1.3)
           + dimv(300, 205, 420, "J+30", 1.4)
           + P("M60 185C110 120 150 120 190 160S270 210 320 130", .6, "d dc")
           + f'<text x="60" y="110" class="m in" font-size="12" letter-spacing="1" fill="{CORAL}" style="animation-delay:1s">T °C · LSTM / SARIMA</text>'
           + P("M354 90a24 24 0 1 0 -48 0a24 24 0 1 0 48 0", .3)
           + f'<g style="transform-origin:330px 90px; animation:spin 16s linear infinite">{rays}</g>')
    out["03-agri"] = plate(
        "03", "Future-Agriculteur",
        ["Un calendrier agricole intelligent pour les agriculteurs débutants : on entre un code",
         "postal, le site recommande quoi cultiver selon le jour, la semaine ou le mois."],
        "CE QUE FAIT LE PROJET",
        ["Prévision des températures station par station, avec les données SYNOP",
         "Modèles LSTM et SARIMA entraînés pour plusieurs villes françaises",
         "Site PHP et MySQL, avec visualisations et explication des modèles"],
        [("CONTEXTE", "SCIENCE DES DONNÉES 4"), ("ÉQUIPE", "4 ÉTUDIANTS"), ("STACK", "PYTHON · KERAS · PHP")],
        [240, 160, 300], art,
        alt="Planche 03, Future-Agriculteur : calendrier agricole intelligent avec prévisions de températures")

    # 04 : schéma des curseurs du simulateur
    art = ""
    for i, (y, t, dur) in enumerate([(130, "SOMMEIL", 3.2), (200, "TRAVAIL", 4.1), (270, "ÉCRANS", 3.6)]):
        art += P(f"M70 {y}H360", .2 + i * .2)
        art += P("".join(f"M{x} {y - 5}V{y + 5}" for x in range(70, 361, 29)), .3 + i * .2, "dim")
        art += (f'<text x="70" y="{y - 16}" class="m in" font-size="11.5" letter-spacing="2" fill="{CYAN}" '
                f'style="animation-delay:{.5 + i * .2:.2f}s">{t}</text>')
        art += (f'<g style="animation:sl{i} {dur}s ease-in-out infinite alternate"><circle cx="150" cy="{y}" r="11" fill="{BG}" '
                f'stroke="{GOLD}" stroke-width="2.5"/></g>')
    art += P("M70 340H360V376H70Z", 1.0)
    art += (f'<rect x="74" y="344" width="282" height="28" fill="{CORAL}" opacity=".85" style="transform-box:fill-box; '
            f'transform-origin:left; animation:res 3.6s ease-in-out infinite alternate"/>')
    art += (f'<text x="70" y="406" class="m in" font-size="12" letter-spacing="1" fill="{GOLD}" '
            f'style="animation-delay:1.2s">ŷ = β₀ + Σ βᵢxᵢ → MOYENNE</text>')
    css = ("@keyframes sl0{to{transform:translateX(150px)}} @keyframes sl1{to{transform:translateX(110px)}}"
           "@keyframes sl2{to{transform:translateX(-60px)}} @keyframes res{from{transform:scaleX(.45)} to{transform:scaleX(1)}}")
    out["04-orga"] = plate(
        "04", "Orga+",
        ["Une plateforme web pour aider les étudiants à s'organiser : diagnostic des",
         "habitudes, graphiques de suivi, simulateur de résultats et forum d'entraide."],
        "CE QUE FAIT LE PROJET",
        ["Un simulateur fondé sur une régression linéaire (R), sur 400 profils Kaggle",
         "« Et si je dormais 30 min de plus ? » : l'impact estimé sur la moyenne",
         "Personas, story map, MCD ; requêtes préparées et mots de passe hachés"],
        [("CONTEXTE", "PROJET D'ÉQUIPE · AGILE"), ("ÉQUIPE", "5 ÉTUDIANTS"), ("STACK", "PHP · MYSQL · R · JS")],
        [260, 160, 280], art, css,
        alt="Planche 04, Orga+ : plateforme d'organisation pour étudiants avec simulateur de résultats")

    # 05 : pile de fiches, version courte
    art = (P("M110 105H330V215H110Z", .2, "d", 'transform="rotate(-6 220 160)"')
           + P("M110 105H330V215H110Z", .4, "d", 'transform="rotate(4 220 160)"')
           + '<g style="transform:translate(220px,160px)"><g style="animation:flip 5s ease-in-out infinite">'
           + f'<rect x="-110" y="-55" width="220" height="110" fill="{BG2}" stroke="{GOLD}" stroke-width="2"/>'
           + f'<text x="0" y="8" text-anchor="middle" class="m" font-size="22" font-weight="700" fill="{GOLD}">Q ?</text></g></g>')
    css = "@keyframes flip{0%,40%,60%,100%{transform:scaleX(1)} 50%{transform:scaleX(0)}}"
    out["05-revision"] = plate(
        "05", "Mes révisions",
        ["Mon site de révision du M1 : fiches, flashcards, QCM, annales corrigées,",
         "et TP en R, Python et D3 qui s'exécutent dans le navigateur."],
        "", [], [("CONTEXTE", "PROJET PERSO"), ("STACK", "SVELTE · WEBR · PYODIDE")], [200, 300], art, css, H=290,
        alt="Planche 05, Mes révisions : site de révision du M1 MIASHS")
    return out


# ---------------------------------------------------------------- nomenclature des outils
def tools():
    cols = [("DONNÉES", ["R", "Python", "Pandas", "Jupyter", "SQL", "CouchDB", "ArangoDB"]),
            ("IA", ["Ollama", "Qdrant", "Keras", "CamemBERT", "Agents IA"]),
            ("WEB", ["PHP", "JavaScript", "React", "Svelte", "D3.js", "MySQL", "Docker", "Git"])]
    n = max(len(c[1]) for c in cols)
    W, rh, top = 1200, 30, 104
    H = top + 40 + n * rh + 44
    b = [sheet(W, H),
         f'<text x="40" y="58" class="m in" font-size="12" letter-spacing="3" fill="{CYAN}">NOMENCLATURE</text>',
         f'<text x="40" y="86" class="m in" font-size="24" font-weight="700" letter-spacing="1" fill="{LINE}">OUTILS</text>']
    xs = [40, 120, 470, 820, 1160]
    b.append(f'<rect x="40" y="{top}" width="1120" height="40" fill="{BG2}" class="in"/>')
    for i, t in enumerate(["REP.", "DONNÉES", "IA", "WEB"]):
        b.append(f'<text x="{xs[i] + 14}" y="{top + 26}" class="m in" font-size="12" letter-spacing="2.5" fill="{GOLD}">{t}</text>')
    bottom = top + 40 + n * rh
    grid = f"M40 {top}H1160V{bottom}H40Z" + "".join(f"M{x} {top}V{bottom}" for x in xs[1:-1]) \
        + "".join(f"M40 {top + 40 + r * rh}H1160" for r in range(n))
    b.append(P(grid, .1))
    for r in range(n):
        y = top + 40 + r * rh + 20
        d = .5 + r * .07
        b.append(f'<text x="54" y="{y}" class="m in" font-size="13" fill="{CYAN}" style="animation-delay:{d:.2f}s">{r + 1:02d}</text>')
        for c, (_, items) in enumerate(cols):
            if r < len(items):
                b.append(f'<text x="{xs[c + 1] + 14}" y="{y}" class="m in" font-size="14" fill="{LINE}" '
                         f'style="animation-delay:{d:.2f}s">{esc(items[r])}</text>')
    return svg(W, H, "\n".join(b), label="Nomenclature des outils : " + ", ".join(i for c in cols for i in c[1]))


files = {"header.svg": header(), "tools.svg": tools()}
files.update({f"{k}.svg": v for k, v in projects().items()})
for name, content in files.items():
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)
print(sorted(files))
