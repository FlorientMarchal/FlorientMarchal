"""Génère les SVG du README de profil (style affiche orienté data science).

Usage : python3 scripts/generer_svg.py assets
Autres styles conservés : branches design-affiche et design-blueprint.
"""
import math, os, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

CREAM, INK, MUTED = "#f2ede3", "#141414", "#5b554b"
RED, BLUE, SUN, GREEN = "#ff4d1f", "#2442ff", "#ffc21a", "#19a974"
SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Menlo, Consolas, 'Liberation Mono', monospace"

CSS = f"""
.s{{font-family:{SANS}}} .m{{font-family:{MONO}}}
.in{{opacity:0; animation:in .7s cubic-bezier(.2,.75,.2,1) forwards}}
.pop{{opacity:0; transform-box:fill-box; transform-origin:center; animation:pop .6s cubic-bezier(.3,1.45,.5,1) forwards}}
.left{{opacity:0; animation:left .8s cubic-bezier(.2,.75,.2,1) forwards}}
.draw{{stroke-dasharray:1; stroke-dashoffset:1; animation:draw 2s cubic-bezier(.55,.1,.35,1) forwards}}
.grow{{transform-box:fill-box; transform-origin:bottom; transform:scaleY(0); animation:grow .8s cubic-bezier(.2,.75,.2,1) forwards}}
@keyframes in{{from{{opacity:0; transform:translateY(10px)}} to{{opacity:1; transform:none}}}}
@keyframes left{{from{{opacity:0; transform:translateX(-30px)}} to{{opacity:1; transform:none}}}}
@keyframes pop{{from{{opacity:0; transform:scale(.3)}} to{{opacity:1; transform:scale(1)}}}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
@keyframes grow{{to{{transform:scaleY(1)}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes breathe{{from{{transform:scaleY(1)}} to{{transform:scaleY(.8)}}}}
@keyframes ring{{from{{transform:scale(.4); opacity:.9}} to{{transform:scale(2.2); opacity:0}}}}
"""


def svg(w, h, body, css="", label=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{label}">\n<style>{CSS}{css}</style>\n{body}\n</svg>\n')


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;")


def chips(x, y, items, dark=False, delay=.5, size=13):
    fg = CREAM if dark else INK
    out = []
    for i, t in enumerate(items):
        w = len(t) * size * 0.6 + 30
        out.append(f'<g class="pop" style="animation-delay:{delay + i * .07:.2f}s">'
                   f'<rect x="{x}" y="{y}" width="{w:.0f}" height="34" rx="17" fill="none" stroke="{fg}" stroke-width="1.6"/>'
                   f'<text x="{x + w / 2:.0f}" y="{y + 22}" text-anchor="middle" class="m" font-size="{size}" fill="{fg}">{esc(t)}</text></g>')
        x += w + 10
    return "".join(out)


# ---------------------------------------------------------------- bannière
def header():
    W, H = 1200, 480
    b = [f'<rect width="{W}" height="{H}" fill="{CREAM}"/>',
         f'<text x="48" y="48" class="m in" font-size="13" letter-spacing="3" fill="{INK}">FLORIENT MARCHAL — DATA SCIENCE</text>',
         f'<text x="1152" y="48" text-anchor="end" class="m in" font-size="13" letter-spacing="3" fill="{INK}">M1 MIASHS · MONTPELLIER · 2026</text>',
         f'<line x1="48" y1="64" x2="1152" y2="64" stroke="{INK}" stroke-width="2" class="in"/>']
    # composition : grand disque, histogramme et densité, nuage k-means, loi normale
    b.append(f'<circle cx="985" cy="232" r="138" fill="{RED}" class="pop" style="animation-delay:.2s"/>')
    base, x0, bw, n = 392, 872, 26, 10
    mu, sd = x0 + n * bw / 2, 52
    dens = lambda x: math.exp(-((x - mu) / sd) ** 2 / 2)
    for i in range(n):
        h = 165 * dens(x0 + (i + .5) * bw) + 12
        b.append(f'<rect x="{x0 + i * bw + 2}" y="{base - h:.0f}" width="{bw - 4}" height="{h:.0f}" fill="{INK}" '
                 f'style="transform-box:fill-box; transform-origin:bottom; transform:scaleY(0); '
                 f'animation:grow .8s cubic-bezier(.2,.75,.2,1) {.8 + i * .07:.2f}s forwards, '
                 f'breathe {2.2 + (i % 4) * .4:.1f}s ease-in-out {1.8 + i * .07:.2f}s infinite alternate"/>')
    curve = "M" + " L".join(f"{x:.0f} {base - 182 * dens(x) - 12:.0f}" for x in range(x0 - 20, x0 + n * bw + 21, 6))
    b.append(f'<path d="{curve}" pathLength="1" fill="none" stroke="{CREAM}" stroke-width="5" stroke-linecap="round" '
             f'class="draw" style="animation-delay:1.7s"/>')
    b.append(f'<line x1="852" y1="{base}" x2="1140" y2="{base}" stroke="{INK}" stroke-width="3" class="in" style="animation-delay:.7s"/>')
    b.append(f'<rect x="706" y="240" width="136" height="136" fill="{BLUE}" class="left" style="animation-delay:.45s"/>')
    clusters = [(CREAM, 738, 276, [(0, 0), (14, 8), (-6, 16), (10, -10), (22, 18)]),
                (SUN, 804, 298, [(0, 0), (-12, 10), (8, 14), (-4, -12), (14, -4)]),
                (INK, 756, 342, [(0, 0), (16, 4), (-10, 6), (6, -12), (24, -6)])]
    k = 0
    for col, cx, cy, pts in clusters:
        for dx, dy in pts:
            b.append(f'<circle cx="{cx + dx}" cy="{cy + dy}" r="5" fill="{col}" class="pop" style="animation-delay:{.9 + k * .05:.2f}s"/>')
            k += 1
    b.append(f'<rect x="1046" y="92" width="106" height="48" fill="{SUN}" class="pop" style="animation-delay:.6s"/>')
    b.append(f'<text x="1099" y="122" text-anchor="middle" class="m in" font-size="16" font-weight="700" fill="{INK}" '
             f'style="animation-delay:.9s">N(μ,σ²)</text>')
    b.append(f'<g style="transform-origin:985px 232px; animation:spin 14s linear infinite">'
             f'<circle cx="985" cy="84" r="8" fill="{INK}"/></g>')
    # nom et accroche
    b.append(f'<text x="42" y="196" class="s in" font-size="138" font-weight="800" letter-spacing="-5" '
             f'textLength="650" lengthAdjust="spacingAndGlyphs" fill="{INK}" style="animation-delay:.1s">FLORIENT</text>')
    b.append(f'<text x="42" y="320" class="s in" font-size="138" font-weight="800" letter-spacing="-5" '
             f'textLength="620" lengthAdjust="spacingAndGlyphs" fill="none" stroke="{INK}" stroke-width="2.5" '
             f'style="animation-delay:.25s">MARCHAL</text>')
    b.append(f'<text x="48" y="362" class="s in" font-size="20" fill="{INK}" style="animation-delay:.5s">'
             'Étudiant en M1 MIASHS, orienté data science :</text>')
    b.append(f'<text x="48" y="390" class="s in" font-size="20" font-weight="700" fill="{INK}" style="animation-delay:.6s">'
             'statistiques, machine learning et IA.</text>')
    # bandeau défilant
    words = ("STATISTIQUES ● MACHINE LEARNING ● RÉGRESSION ● ACP ● CLASSIFICATION ● "
             "SÉRIES TEMPORELLES ● NLP ● DATAVIZ ● R ● PYTHON ● ")
    L = 1640
    b.append(f'<rect x="0" y="420" width="{W}" height="60" fill="{INK}"/>')
    b.append('<g style="animation:marquee 28s linear infinite">'
             + "".join(f'<text x="{k * L}" y="457" class="m" font-size="19" letter-spacing="2" fill="{CREAM}" '
                       f'textLength="{L}" lengthAdjust="spacing">{words}</text>' for k in range(2))
             + '</g>')
    css = f"@keyframes marquee{{to{{transform:translateX(-{L}px)}}}}"
    return svg(W, H, "\n".join(b), css, "Florient Marchal, étudiant en M1 MIASHS orienté data science")


# ---------------------------------------------------------------- panneaux de projets
def panel(num, color, num_color, meta, title, desc, label, points, tags, art, art_css="", H=500, alt=""):
    W, P = 1200, 380
    b = [f'<rect width="{W}" height="{H}" fill="{CREAM}"/>',
         f'<rect width="{P}" height="{H}" fill="{color}"/>',
         f'<text x="34" y="128" class="s in" font-size="120" font-weight="800" letter-spacing="-4" fill="{num_color}">{num}</text>',
         f'<g>{art}</g>',
         f'<text x="420" y="64" class="m in" font-size="13" letter-spacing="2.5" fill="{MUTED}">{esc(meta)}</text>',
         f'<text x="1160" y="64" text-anchor="end" class="m in" font-size="13" letter-spacing="2.5" font-weight="700" fill="{INK}">DÉPÔT ↗</text>',
         f'<line x1="420" y1="80" x2="1160" y2="80" stroke="{INK}" stroke-width="2" class="in"/>',
         f'<text x="418" y="138" class="s in" font-size="46" font-weight="800" letter-spacing="-1.5" fill="{INK}" style="animation-delay:.1s">{esc(title)}</text>']
    y = 178
    for ln in desc:
        b.append(f'<text x="420" y="{y}" class="s in" font-size="17" fill="#2a2620" style="animation-delay:.2s">{esc(ln)}</text>')
        y += 26
    if points:
        y += 22
        b.append(f'<rect x="420" y="{y - 11}" width="12" height="12" fill="{color}" class="in" style="animation-delay:.3s"/>'
                 f'<text x="442" y="{y}" class="m in" font-size="12" letter-spacing="3" font-weight="700" fill="{INK}" style="animation-delay:.3s">{label}</text>')
        y += 34
        for i, p in enumerate(points):
            d = .4 + i * .1
            b.append(f'<rect x="420" y="{y - 10}" width="8" height="8" fill="{INK}" class="in" style="animation-delay:{d:.1f}s"/>'
                     f'<text x="442" y="{y}" class="s in" font-size="17" fill="{INK}" style="animation-delay:{d:.1f}s">{esc(p)}</text>')
            y += 31
    b.append(chips(420, H - 70, tags, delay=.6))
    return svg(W, H, "\n".join(b), art_css, alt)


def die(x, y, s, pips, delay, dur):
    r = s * .09
    pos = {2: [(.27, .27), (.73, .73)], 3: [(.25, .25), (.5, .5), (.75, .75)],
           5: [(.25, .25), (.75, .25), (.5, .5), (.25, .75), (.75, .75)],
           6: [(.27, .22), (.73, .22), (.27, .5), (.73, .5), (.27, .78), (.73, .78)]}[pips]
    dots = "".join(f'<circle cx="{x + s * a:.0f}" cy="{y + s * c:.0f}" r="{r:.1f}" fill="{INK}"/>' for a, c in pos)
    return (f'<g class="pop" style="animation-delay:{delay}s"><g style="transform-box:fill-box; transform-origin:center; '
            f'animation:tumble {dur}s ease-in-out {delay + .6}s infinite">'
            f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{s * .16:.0f}" fill="{CREAM}"/>{dots}</g></g>')


def projects():
    out = {}

    # 01 : série temporelle observée, prévision et intervalle de confiance
    obs = [(40, 360), (59, 338), (78, 318), (97, 330), (116, 304), (135, 280), (154, 290), (173, 264),
           (192, 250), (211, 262), (230, 240)]
    fc = [(230, 240), (260, 226), (290, 220), (320, 204), (350, 196)]
    spread = [0, 10, 18, 26, 34]
    band = ("M" + " L".join(f"{x} {y - s}" for (x, y), s in zip(fc, spread))
            + " L" + " L".join(f"{x} {y + s}" for (x, y), s in reversed(list(zip(fc, spread)))) + "Z")
    art = (f'<line x1="30" y1="440" x2="360" y2="440" stroke="{INK}" stroke-width="3"/>'
           f'<line x1="30" y1="440" x2="30" y2="180" stroke="{INK}" stroke-width="3"/>'
           f'<line x1="230" y1="186" x2="230" y2="440" stroke="{INK}" stroke-width="2" stroke-dasharray="5 6" class="in" style="animation-delay:1.6s"/>'
           f'<path d="{band}" fill="{CREAM}" opacity=".85" class="in" style="animation-delay:1.8s"/>'
           f'<path d="M{" L".join(f"{x} {y}" for x, y in obs)}" pathLength="1" fill="none" stroke="{INK}" stroke-width="4" '
           f'stroke-linejoin="round" class="draw" style="animation-delay:.3s"/>'
           + "".join(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{INK}" class="pop" style="animation-delay:{.4 + i * .1:.1f}s"/>'
                     for i, (x, y) in enumerate(obs))
           + f'<path d="M{" L".join(f"{x} {y}" for x, y in fc)}" fill="none" stroke="{RED}" stroke-width="4" '
             f'stroke-dasharray="10 7" class="in" style="animation-delay:2.1s"/>'
           + f'<circle cx="350" cy="196" r="7" fill="{RED}" class="pop" style="animation-delay:2.4s"/>'
           + f'<circle cx="350" cy="196" r="7" fill="none" stroke="{RED}" stroke-width="2" '
             f'style="transform-box:fill-box; transform-origin:center; animation:ring 1.8s ease-out 2.6s infinite"/>'
           + f'<text x="40" y="200" class="m in" font-size="12" letter-spacing="2" fill="{INK}" style="animation-delay:.6s">T °C</text>'
           + f'<text x="240" y="470" class="m in" font-size="12" letter-spacing="2" fill="{INK}" style="animation-delay:1.8s">PRÉVISION</text>'
           + f'<text x="40" y="470" class="m in" font-size="12" letter-spacing="2" fill="{INK}" style="animation-delay:.6s">OBSERVÉ</text>')
    out["01-agri"] = panel(
        "01", SUN, INK, "SCIENCE DES DONNÉES 4 · SÉRIES TEMPORELLES · 4 ÉTUDIANTS", "Future-Agriculteur",
        ["Un calendrier agricole intelligent : à partir d'un code postal, le site prévoit les",
         "températures et recommande quoi cultiver selon le jour, la semaine ou le mois."],
        "LA DÉMARCHE DATA",
        ["Données météo SYNOP : nettoyage, exploration et visualisation en Python",
         "Séries temporelles : modèles LSTM (Keras) et SARIMA, un modèle par station",
         "Prévisions au jour, à la semaine et au mois, traduites en conseils de cultures"],
        ["Python", "Pandas", "Keras", "SARIMA", "MySQL", "Chart.js"], art,
        alt="01 Future-Agriculteur : prévision de températures par séries temporelles (LSTM, SARIMA) pour un calendrier agricole")

    # 02 : espace d'embeddings, requête et plus proches voisins
    groups = [(CREAM, [(70, 210), (95, 190), (110, 228), (82, 245), (125, 205), (60, 180)]),
              (SUN, [(260, 200), (290, 220), (275, 245), (305, 190), (250, 230), (320, 228)]),
              (INK, [(110, 380), (140, 400), (90, 410), (130, 360), (160, 385), (75, 370)])]
    qx, qy = 200, 300
    neigh = [(250, 230), (160, 385), (130, 360)]
    art = "".join(f'<line x1="{qx}" y1="{qy}" x2="{x}" y2="{y}" stroke="{CREAM}" stroke-width="2" stroke-dasharray="6 6" '
                  f'style="opacity:0; animation:in .7s 1.4s forwards, flow 1s linear infinite"/>' for x, y in neigh)
    k = 0
    for col, pts in groups:
        for x, y in pts:
            art += f'<circle cx="{x}" cy="{y}" r="8" fill="{col}" class="pop" style="animation-delay:{.3 + k * .05:.2f}s"/>'
            k += 1
    art += (f'<circle cx="{qx}" cy="{qy}" r="14" fill="{RED}" class="pop" style="animation-delay:1.3s"/>'
            f'<circle cx="{qx}" cy="{qy}" r="14" fill="none" stroke="{RED}" stroke-width="3" '
            f'style="transform-box:fill-box; transform-origin:center; animation:ring 1.8s ease-out 1.6s infinite"/>'
            f'<text x="{qx + 22}" y="{qy + 5}" class="m in" font-size="12" letter-spacing="2" fill="{CREAM}" style="animation-delay:1.4s">REQUÊTE</text>'
            f'<text x="34" y="470" class="m in" font-size="12" letter-spacing="2" fill="{CREAM}" style="animation-delay:.6s">ESPACE D\'EMBEDDINGS · k PLUS PROCHES</text>')
    css = "@keyframes flow{to{stroke-dashoffset:-12}}"
    out["02-pairia"] = panel(
        "02", BLUE, CREAM, "PROJET DE STAGE · NLP · RAG · IA LOCALE", "PairIA",
        ["Une boutique de chaussures en ligne avec un assistant conversationnel qui tourne",
         "entièrement en local : des modèles open source, aucune API payante."],
        "LA PARTIE IA",
        ["Classification d'intentions : un CamemBERT affiné sur 8 classes",
         "Recherche sémantique : embeddings de texte et d'images (CLIP) dans Qdrant",
         "RAG avec LLaMA 3.1 et Qwen 2.5 en local via Ollama, réponses en 75 langues"],
        ["Python", "CamemBERT", "Qdrant", "Ollama", "FastAPI", "Docker"], art, css,
        alt="02 PairIA : assistant IA local pour un site e-commerce, avec classification d'intentions, recherche sémantique et RAG")

    # 03 : simulateur à curseurs et moyenne prédite
    sliders = ""
    for i, (y, col, dur) in enumerate([(205, SUN, 3.2), (265, RED, 4.1), (325, BLUE, 3.6)]):
        sliders += (f'<line x1="40" y1="{y}" x2="340" y2="{y}" stroke="{CREAM}" stroke-width="3" opacity=".5"/>'
                    f'<circle cx="110" cy="{y}" r="14" fill="{col}" style="animation:slide{i} {dur}s ease-in-out infinite alternate"/>')
    labels = "".join(f'<text x="40" y="{y - 18}" class="m" font-size="12" letter-spacing="2" fill="{CREAM}" opacity=".7">{t}</text>'
                     for y, t in [(205, "SOMMEIL"), (265, "TRAVAIL"), (325, "ÉCRANS")])
    bar = (f'<text x="40" y="392" class="m" font-size="12" letter-spacing="2" fill="{CREAM}">ŷ · MOYENNE PRÉDITE</text>'
           f'<rect x="40" y="406" width="300" height="34" fill="none" stroke="{CREAM}" stroke-width="2"/>'
           f'<rect x="44" y="410" width="292" height="26" fill="{GREEN}" style="transform-box:fill-box; transform-origin:left; '
           f'animation:res 3.6s ease-in-out infinite alternate"/>')
    css = ("@keyframes slide0{to{transform:translateX(170px)}} @keyframes slide1{to{transform:translateX(120px)}}"
           "@keyframes slide2{to{transform:translateX(-50px)}} @keyframes res{from{transform:scaleX(.45)} to{transform:scaleX(.9)}}")
    out["03-orga"] = panel(
        "03", INK, CREAM, "PROJET D'ÉQUIPE · RÉGRESSION LINÉAIRE · AGILE", "Orga+",
        ["Une plateforme web pour aider les étudiants à s'organiser : diagnostic des habitudes,",
         "graphiques de suivi, simulateur de résultats et forum d'entraide."],
        "LA PARTIE DATA",
        ["Régression linéaire sous R sur un jeu Kaggle de 400 profils d'étudiants",
         "Simulateur à curseurs : sommeil, travail, écrans → moyenne prédite",
         "Tableaux de bord de suivi des habitudes ; application PHP et MySQL"],
        ["R", "Régression", "PHP", "MySQL", "JavaScript"], labels + sliders + bar, css,
        alt="03 Orga+ : simulateur de résultats fondé sur une régression linéaire")

    # 04 : dés
    art = die(48, 210, 120, 5, .3, 4) + die(200, 300, 100, 3, .45, 5) + die(130, 380, 80, 6, .6, 4.5) \
        + die(250, 190, 76, 2, .5, 6)
    css = "@keyframes tumble{0%,70%,100%{transform:rotate(0)} 80%{transform:rotate(-20deg)} 90%{transform:rotate(12deg)}}"
    out["04-casino"] = panel(
        "04", RED, CREAM, "COURS DE PROGRAMMATION AGENTIQUE · M1 · ~25 ÉTUDIANTS", "Casino Fantôme",
        ["Un simulateur de casino 100 % fictif : 13 jeux à débloquer, niveaux, classement et",
         "boutique. Tout le code est écrit par des agents IA, que la promo pilote et relit."],
        "MA PART · GROUPE 4, APPLICATION",
        ["Les écrans Lobby, Profil, Classement, création de profil et page 404",
         "L'intégration des 11 interfaces de jeu du groupe 3 dans la page de jeu",
         "24 pull requests fusionnées, 7 revues de code et une vingtaine d'issues"],
        ["Agents IA", "React", "Vite", "JavaScript", "Git"], art, css,
        alt="04 Casino Fantôme : simulateur de casino fictif codé par des agents IA, cours de programmation agentique")

    # 05 : pile de fiches, version courte
    cards = "".join(
        f'<g style="transform:translate({190 + dx}px, {232 + dy}px) rotate({r}deg)">'
        f'<rect x="-95" y="-58" width="190" height="116" rx="10" fill="{CREAM}" stroke="{INK}" stroke-width="2.5"/></g>'
        for dx, dy, r in [(-14, 10, -9), (12, 4, 6)])
    top = (f'<g style="transform:translate(190px, 228px)"><g style="animation:flip 5s ease-in-out infinite">'
           f'<rect x="-95" y="-58" width="190" height="116" rx="10" fill="{CREAM}" stroke="{INK}" stroke-width="2.5"/>'
           f'<text x="0" y="10" text-anchor="middle" class="s" font-size="30" font-weight="800" fill="{INK}">ACP ?</text></g></g>')
    css = "@keyframes flip{0%,40%,60%,100%{transform:scaleX(1)} 50%{transform:scaleX(0)}}"
    out["05-revision"] = panel(
        "05", GREEN, CREAM, "PROJET PERSO · EN LIGNE", "Mes révisions",
        ["Mon site de révision du M1 : ACP, régression, classification, optimisation…",
         "avec flashcards, QCM et TP en R et Python qui tournent dans le navigateur."],
        "", [], ["Svelte", "webR", "Pyodide", "D3.js"], cards + top, css, H=320,
        alt="05 Mes révisions : site de révision du M1 MIASHS")
    return out


# ---------------------------------------------------------------- outils
def tools():
    rows = [("LANGAGES", SUN, ["R", "Python", "SQL", "JavaScript", "PHP"]),
            ("DATA", RED, ["Pandas", "NumPy", "Matplotlib", "Jupyter", "Keras", "Ollama", "Qdrant"]),
            ("MÉTHODES", "#7d8bff", ["Régression", "ACP", "Classification", "Séries temporelles", "NLP · RAG", "Dataviz"]),
            ("BASES & WEB", GREEN, ["MySQL", "CouchDB", "ArangoDB", "D3.js", "React", "Svelte", "Docker", "Git"])]
    W, H = 1200, 120 + len(rows) * 62 + 24
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>',
         f'<text x="48" y="64" class="s in" font-size="40" font-weight="800" letter-spacing="-1" fill="{CREAM}">Boîte à outils</text>',
         f'<circle cx="1132" cy="52" r="20" fill="{RED}" class="pop"/><rect x="1070" y="34" width="36" height="36" fill="{SUN}" class="pop" style="animation-delay:.15s"/>']
    for k, (lab, col, items) in enumerate(rows):
        y = 112 + k * 62
        b.append(f'<text x="48" y="{y + 23}" class="m in" font-size="14" letter-spacing="3" font-weight="700" fill="{col}" '
                 f'style="animation-delay:{.2 + k * .15:.2f}s">{esc(lab)}</text>')
        b.append(chips(230, y, items, dark=True, delay=.3 + k * .15, size=14))
    return svg(W, H, "\n".join(b), label="Boîte à outils : " + ", ".join(i for r in rows for i in r[2]))


files = {"header.svg": header(), "tools.svg": tools()}
files.update({f"{k}.svg": v for k, v in projects().items()})
for name, content in files.items():
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)
print(sorted(files))
