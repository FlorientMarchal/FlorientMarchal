"""Génère les SVG du README de profil (style affiche : aplats de couleur, formes géométriques).

Usage : python3 scripts/generer_svg.py assets
"""
import os, sys

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
.draw{{stroke-dasharray:1200; stroke-dashoffset:1200; animation:draw 2s cubic-bezier(.55,.1,.35,1) forwards}}
.grow{{transform-box:fill-box; transform-origin:bottom; transform:scaleY(0); animation:grow .8s cubic-bezier(.2,.75,.2,1) forwards}}
@keyframes in{{from{{opacity:0; transform:translateY(10px)}} to{{opacity:1; transform:none}}}}
@keyframes left{{from{{opacity:0; transform:translateX(-30px)}} to{{opacity:1; transform:none}}}}
@keyframes pop{{from{{opacity:0; transform:scale(.3)}} to{{opacity:1; transform:scale(1)}}}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
@keyframes grow{{to{{transform:scaleY(1)}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes breathe{{from{{transform:scaleY(1)}} to{{transform:scaleY(.72)}}}}
"""


def svg(w, h, body, css="", label=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{label}">\n<style>{CSS}{css}</style>\n{body}\n</svg>\n')


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;")


def chips(x, y, items, dark=False, delay=.5, size=13):
    fg, stroke = (CREAM, CREAM) if dark else (INK, INK)
    out = []
    for i, t in enumerate(items):
        w = len(t) * size * 0.6 + 30
        out.append(f'<g class="pop" style="animation-delay:{delay + i * .07:.2f}s">'
                   f'<rect x="{x}" y="{y}" width="{w:.0f}" height="34" rx="17" fill="none" stroke="{stroke}" stroke-width="1.6"/>'
                   f'<text x="{x + w / 2:.0f}" y="{y + 22}" text-anchor="middle" class="m" font-size="{size}" fill="{fg}">{esc(t)}</text></g>')
        x += w + 10
    return "".join(out)


# ---------------------------------------------------------------- bannière
def header():
    W, H = 1200, 480
    b = [f'<rect width="{W}" height="{H}" fill="{CREAM}"/>',
         f'<text x="48" y="48" class="m in" font-size="13" letter-spacing="3" fill="{INK}">FLORIENT MARCHAL — PROFIL</text>',
         f'<text x="1152" y="48" text-anchor="end" class="m in" font-size="13" letter-spacing="3" fill="{INK}">M1 MIASHS · MONTPELLIER · 2026</text>',
         f'<line x1="48" y1="64" x2="1152" y2="64" stroke="{INK}" stroke-width="2" class="in"/>']
    # composition géométrique
    b.append(f'<circle cx="985" cy="232" r="138" fill="{RED}" class="pop" style="animation-delay:.2s"/>')
    b.append(f'<rect x="770" y="250" width="130" height="130" fill="{BLUE}" class="left" style="animation-delay:.45s"/>')
    b.append(f'<rect x="1060" y="96" width="92" height="46" fill="{SUN}" class="pop" style="animation-delay:.6s"/>')
    for i, (x, h) in enumerate([(915, 120), (955, 190), (995, 150), (1035, 230), (1075, 175)]):
        b.append(f'<rect x="{x}" y="{392 - h}" width="26" height="{h}" fill="{INK}" class="grow" '
                 f'style="animation:grow .8s cubic-bezier(.2,.75,.2,1) {.8 + i * .12:.2f}s forwards, '
                 f'breathe {2 + i * .35:.2f}s ease-in-out {1.8 + i * .12:.2f}s infinite alternate"/>')
    b.append(f'<line x1="890" y1="392" x2="1130" y2="392" stroke="{INK}" stroke-width="3" class="in" style="animation-delay:.7s"/>')
    b.append(f'<g style="transform-origin:985px 232px; animation:spin 14s linear infinite">'
             f'<circle cx="985" cy="84" r="8" fill="{INK}"/></g>')
    # nom
    b.append(f'<text x="42" y="196" class="s in" font-size="138" font-weight="800" letter-spacing="-5" '
             f'textLength="650" lengthAdjust="spacingAndGlyphs" fill="{INK}" style="animation-delay:.1s">FLORIENT</text>')
    b.append(f'<text x="42" y="320" class="s in" font-size="138" font-weight="800" letter-spacing="-5" '
             f'textLength="620" lengthAdjust="spacingAndGlyphs" fill="none" stroke="{INK}" stroke-width="2.5" '
             f'style="animation-delay:.25s">MARCHAL</text>')
    b.append(f'<text x="48" y="362" class="s in" font-size="20" fill="{INK}" style="animation-delay:.5s">'
             'Étudiant en M1 MIASHS. Statistiques, IA et web :</text>')
    b.append(f'<text x="48" y="390" class="s in" font-size="20" font-weight="700" fill="{INK}" style="animation-delay:.6s">'
             'j\'aime transformer des données en outils.</text>')
    # bandeau défilant
    words = "STATISTIQUES ● SCIENCE DES DONNÉES ● IA LOCALE ● VISUALISATION ● R ● PYTHON ● PHP ● REACT ● "
    L = 1300
    b.append(f'<rect x="0" y="420" width="{W}" height="60" fill="{INK}"/>')
    b.append(f'<g style="animation:marquee 22s linear infinite">'
             + "".join(f'<text x="{k * L}" y="457" class="m" font-size="19" letter-spacing="2" fill="{CREAM}" '
                       f'textLength="{L}" lengthAdjust="spacing">{words}</text>' for k in range(2))
             + '</g>')
    css = f"@keyframes marquee{{to{{transform:translateX(-{L}px)}}}}"
    return svg(W, H, "\n".join(b), css, "Florient Marchal, étudiant en M1 MIASHS : statistiques, IA et web")


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
    pos = {1: [(.5, .5)], 2: [(.27, .27), (.73, .73)], 3: [(.25, .25), (.5, .5), (.75, .75)],
           4: [(.27, .27), (.73, .27), (.27, .73), (.73, .73)],
           5: [(.25, .25), (.75, .25), (.5, .5), (.25, .75), (.75, .75)],
           6: [(.27, .22), (.73, .22), (.27, .5), (.73, .5), (.27, .78), (.73, .78)]}[pips]
    dots = "".join(f'<circle cx="{x + s * a:.0f}" cy="{y + s * c:.0f}" r="{r:.1f}" fill="{INK}"/>' for a, c in pos)
    return (f'<g class="pop" style="animation-delay:{delay}s"><g style="transform-box:fill-box; transform-origin:center; '
            f'animation:tumble {dur}s ease-in-out {delay + .6}s infinite">'
            f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{s * .16:.0f}" fill="{CREAM}"/>{dots}</g></g>')


def projects():
    out = {}
    art = die(48, 210, 120, 5, .3, 4) + die(200, 300, 100, 3, .45, 5) + die(130, 380, 80, 6, .6, 4.5) \
        + die(250, 190, 76, 2, .5, 6)
    css = "@keyframes tumble{0%,70%,100%{transform:rotate(0)} 80%{transform:rotate(-20deg)} 90%{transform:rotate(12deg)}}"
    out["01-casino"] = panel(
        "01", RED, CREAM, "COURS DE PROGRAMMATION AGENTIQUE · M1 · ~25 ÉTUDIANTS", "Casino Fantôme",
        ["Un simulateur de casino 100 % fictif : 13 jeux à débloquer, niveaux, classement et",
         "boutique. Tout le code est écrit par des agents IA, que la promo pilote et relit."],
        "MA PART · GROUPE 4, APPLICATION",
        ["Les écrans Lobby, Profil, Classement, création de profil et page 404",
         "L'intégration des 11 interfaces de jeu du groupe 3 dans la page de jeu",
         "24 pull requests fusionnées, 7 revues de code et une vingtaine d'issues"],
        ["React", "Vite", "JavaScript", "Agents IA", "Git"], art, css,
        alt="01 Casino Fantôme : simulateur de casino fictif codé par des agents IA, projet de promo")

    bubble1 = (f'<g style="animation:b1 6s ease-in-out infinite"><rect x="40" y="190" width="240" height="78" rx="20" fill="{CREAM}"/>'
               f'<path d="M64 268 l0 24 l26 -24z" fill="{CREAM}"/>'
               f'<rect x="62" y="214" width="170" height="10" rx="5" fill="{INK}" opacity=".8"/>'
               f'<rect x="62" y="236" width="120" height="10" rx="5" fill="{INK}" opacity=".35"/></g>')
    bubble2 = (f'<g style="animation:b2 6s ease-in-out infinite"><rect x="110" y="310" width="230" height="78" rx="20" fill="{INK}"/>'
               f'<path d="M316 388 l0 24 l-26 -24z" fill="{INK}"/>'
               + "".join(f'<circle cx="{196 + k * 28}" cy="349" r="8" fill="{SUN}" style="animation:dot 1.2s {k * .2:.1f}s infinite"/>'
                         for k in range(3)) + '</g>')
    nodes = "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="{CREAM}" opacity=".55"/>' for x, y in
                    [(300, 150), (340, 175), (320, 215), (350, 240)])
    links = f'<path d="M300 150L340 175L320 215L350 240M300 150L320 215" stroke="{CREAM}" stroke-width="1.5" opacity=".4" fill="none"/>'
    css = ("@keyframes b1{0%{opacity:0; transform:translateY(12px)} 8%,85%{opacity:1; transform:none} 95%,100%{opacity:0}}"
           "@keyframes b2{0%,25%{opacity:0; transform:translateY(12px)} 33%,85%{opacity:1; transform:none} 95%,100%{opacity:0}}"
           "@keyframes dot{0%,60%,100%{opacity:.3} 30%{opacity:1}}")
    out["02-pairia"] = panel(
        "02", BLUE, CREAM, "PROJET DE STAGE · E-COMMERCE ET IA LOCALE", "PairIA",
        ["Une boutique de chaussures en ligne complète, avec un assistant conversationnel qui",
         "tourne entièrement en local : aucune API payante, que des modèles open source."],
        "CE QUE FAIT LE PROJET",
        ["Chatbot client : recherche en langage naturel, par photo (CLIP) ou à la voix (Whisper)",
         "Chatbot admin : il gère la boutique en langage naturel avec 25 outils (function calling)",
         "Pipeline RAG sur Qdrant, intentions classées par un CamemBERT affiné, LLM via Ollama"],
        ["Python", "FastAPI", "Ollama", "Qdrant", "PHP", "MySQL", "Docker"], links + nodes + bubble1 + bubble2, css,
        alt="02 PairIA : boutique de chaussures en ligne avec un assistant IA local, projet de stage")

    curve = "M30 330 C 80 250, 120 250, 165 300 S 250 360, 290 280 S 340 200, 360 220"
    sprouts = "".join(
        f'<g class="grow" style="animation-delay:{1.4 + k * .25:.2f}s"><path d="M{x} 460V{460 - h}" stroke="{INK}" stroke-width="4"/>'
        f'<path d="M{x} {470 - h} c-18 0-28-10-28-24 c16 0 28 8 28 24z" fill="{INK}"/>'
        f'<path d="M{x} {482 - h} c16 0 26-10 26-22 c-14 0-26 8-26 22z" fill="{INK}"/></g>'
        for k, (x, h) in enumerate([(80, 60), (170, 90), (260, 70)]))
    art = (f'<circle cx="300" cy="190" r="40" fill="{RED}" style="transform-box:fill-box; transform-origin:center; '
           f'animation:pulse 3s ease-in-out infinite"/>'
           f'<path d="{curve}" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" class="draw" style="animation-delay:.3s"/>'
           f'<line x1="30" y1="462" x2="350" y2="462" stroke="{INK}" stroke-width="4"/>' + sprouts)
    css = "@keyframes pulse{50%{transform:scale(1.12)}}"
    out["03-agri"] = panel(
        "03", SUN, INK, "PROJET D'ÉQUIPE · SCIENCE DES DONNÉES 4 · 4 ÉTUDIANTS", "Future-Agriculteur",
        ["Un calendrier agricole intelligent pour les agriculteurs débutants : on entre un code",
         "postal, le site recommande quoi cultiver selon le jour, la semaine ou le mois."],
        "CE QUE FAIT LE PROJET",
        ["Prévision des températures station par station, à partir des données SYNOP",
         "Modèles LSTM et SARIMA entraînés pour plusieurs villes françaises",
         "Site PHP et MySQL, avec des pages de visualisation et d'explication des modèles"],
        ["Python", "Keras", "SARIMA", "MySQL", "PHP", "Chart.js"], art, css,
        alt="03 Future-Agriculteur : calendrier agricole intelligent avec prévisions de températures")

    sliders = ""
    for k, (y, col, dur) in enumerate([(205, SUN, 3.2), (265, RED, 4.1), (325, BLUE, 3.6)]):
        sliders += (f'<line x1="40" y1="{y}" x2="340" y2="{y}" stroke="{CREAM}" stroke-width="3" opacity=".5"/>'
                    f'<circle cx="110" cy="{y}" r="14" fill="{col}" style="animation:slide{k} {dur}s ease-in-out infinite alternate"/>')
    labels = "".join(f'<text x="40" y="{y - 18}" class="m" font-size="12" letter-spacing="2" fill="{CREAM}" opacity=".7">{t}</text>'
                     for y, t in [(205, "SOMMEIL"), (265, "TRAVAIL"), (325, "ÉCRANS")])
    bar = (f'<text x="40" y="392" class="m" font-size="12" letter-spacing="2" fill="{CREAM}">MOYENNE PRÉDITE</text>'
           f'<rect x="40" y="406" width="300" height="34" fill="none" stroke="{CREAM}" stroke-width="2"/>'
           f'<rect x="44" y="410" width="292" height="26" fill="{GREEN}" style="transform-box:fill-box; transform-origin:left; '
           f'animation:res 3.6s ease-in-out infinite alternate"/>')
    css = ("@keyframes slide0{to{transform:translateX(170px)}} @keyframes slide1{to{transform:translateX(120px)}}"
           "@keyframes slide2{to{transform:translateX(-50px)}} @keyframes res{from{transform:scaleX(.45)} to{transform:scaleX(.9)}}")
    out["04-orga"] = panel(
        "04", INK, CREAM, "PROJET D'ÉQUIPE · PLATEFORME ÉTUDIANTE · MÉTHODE AGILE", "Orga+",
        ["Une plateforme web pour aider les étudiants à s'organiser : diagnostic des habitudes,",
         "graphiques de suivi, simulateur de résultats et forum d'entraide."],
        "CE QUE FAIT LE PROJET",
        ["Un simulateur fondé sur une régression linéaire (R), entraînée sur 400 profils Kaggle",
         "« Et si je dormais 30 min de plus ? » : l'impact estimé sur la moyenne, avec des curseurs",
         "Personas, story map et MCD ; requêtes préparées, filtrage XSS, mots de passe hachés"],
        ["PHP", "MySQL", "R", "JavaScript", "Figma"], labels + sliders + bar, css,
        alt="04 Orga+ : plateforme d'organisation pour étudiants avec simulateur de résultats")

    cards = "".join(
        f'<g style="transform:translate({190 + dx}px, {232 + dy}px) rotate({r}deg)">'
        f'<rect x="-95" y="-58" width="190" height="116" rx="10" fill="{CREAM}" stroke="{INK}" stroke-width="2.5"/></g>'
        for dx, dy, r in [(-14, 10, -9), (12, 4, 6)])
    top = (f'<g style="transform:translate(190px, 228px)"><g style="animation:flip 5s ease-in-out infinite">'
           f'<rect x="-95" y="-58" width="190" height="116" rx="10" fill="{CREAM}" stroke="{INK}" stroke-width="2.5"/>'
           f'<text x="0" y="10" text-anchor="middle" class="s" font-size="30" font-weight="800" fill="{INK}">Q ?</text></g></g>')
    css = "@keyframes flip{0%,40%,60%,100%{transform:scaleX(1)} 50%{transform:scaleX(0)}}"
    out["05-revision"] = panel(
        "05", GREEN, CREAM, "PROJET PERSO · EN LIGNE", "Mes révisions",
        ["Mon site de révision du M1 : fiches, flashcards, QCM, annales corrigées,",
         "et TP en R, Python et D3 qui s'exécutent dans le navigateur."],
        "", [], ["Svelte", "webR", "Pyodide", "D3.js"], cards + top, css, H=320,
        alt="05 Mes révisions : site de révision du M1 MIASHS")
    return out


# ---------------------------------------------------------------- outils
def tools():
    W, H = 1200, 330
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>',
         f'<text x="48" y="64" class="s in" font-size="40" font-weight="800" letter-spacing="-1" fill="{CREAM}">Boîte à outils</text>',
         f'<circle cx="1132" cy="52" r="20" fill="{RED}" class="pop"/><rect x="1070" y="34" width="36" height="36" fill="{SUN}" class="pop" style="animation-delay:.15s"/>']
    rows = [("DONNÉES", SUN, ["R", "Python", "Pandas", "Jupyter", "SQL", "CouchDB", "ArangoDB"]),
            ("IA", RED, ["Ollama", "Qdrant", "Keras", "CamemBERT", "Agents IA"]),
            ("WEB", "#7d8bff", ["PHP", "JavaScript", "React", "Svelte", "D3.js", "MySQL", "Docker", "Git"])]
    for k, (lab, col, items) in enumerate(rows):
        y = 116 + k * 66
        b.append(f'<text x="48" y="{y + 23}" class="m in" font-size="14" letter-spacing="3" font-weight="700" fill="{col}" '
                 f'style="animation-delay:{.2 + k * .15:.2f}s">{lab}</text>')
        b.append(chips(190, y, items, dark=True, delay=.3 + k * .15, size=14))
    return svg(W, H, "\n".join(b), label="Boîte à outils : " + ", ".join(i for r in rows for i in r[2]))


files = {"header.svg": header(), "tools.svg": tools()}
files.update({f"{k}.svg": v for k, v in projects().items()})
for name, content in files.items():
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)
print(sorted(files))
