"""Génère les SVG du README de profil (palette du site de révision).

Usage : python3 scripts/generer_svg.py assets
"""
import os, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

C = dict(bg="#eef1f4", grid="#dfe5ec", paper="#ffffff", paper2="#f6f8fb", ink="#172033", ink2="#2d3749",
         muted="#525d6f", line="#d3d9e2", accent="#1f4fb5", soft="#e8eef9", red="#b83226",
         margin="#e3786e", good="#16703d", warn="#955700", fgrid="#e8edf5")
SERIF = "Georgia, 'Iowan Old Style', 'Times New Roman', serif"
SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Menlo, Consolas, 'Liberation Mono', monospace"

BASE_CSS = f"""
.mono{{font-family:{MONO}}} .serif{{font-family:{SERIF}}} .sans{{font-family:{SANS}}}
.pop{{opacity:0; transform-box:fill-box; transform-origin:center; animation:pop .5s cubic-bezier(.3,1.45,.5,1) forwards}}
.fade{{opacity:0; animation:fade .6s ease forwards}}
.draw{{stroke-dasharray:1000; stroke-dashoffset:1000; animation:draw 1.4s cubic-bezier(.55,.1,.35,1) forwards}}
@keyframes pop{{from{{opacity:0; transform:scale(.2)}} to{{opacity:1; transform:scale(1)}}}}
@keyframes fade{{from{{opacity:0; transform:translateY(6px)}} to{{opacity:1; transform:none}}}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes nudge{{0%,70%,100%{{transform:translateX(0)}} 85%{{transform:translateX(5px)}}}}
"""


def svg(w, h, body, css="", label=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{label}">\n<style>{BASE_CSS}{css}</style>\n{body}\n</svg>\n')


def grid_bg(w, h, step=24, fill=C["bg"], stroke=C["grid"], pid="g"):
    return (f'<defs><pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
            f'<path d="M{step} 0H0V{step}" fill="none" stroke="{stroke}" stroke-width="1"/></pattern>'
            f'<clipPath id="{pid}c"><rect x="0" y="0" width="{w}" height="{h}" rx="16"/></clipPath></defs>'
            f'<g clip-path="url(#{pid}c)"><rect width="{w}" height="{h}" fill="{fill}"/>'
            f'<rect width="{w}" height="{h}" fill="url(#{pid})"/></g>')


def chip(x, y, text, color, delay=0.0, size=13):
    w = len(text) * size * 0.61 + 36
    return (f'<g class="pop" style="animation-delay:{delay:.2f}s">'
            f'<rect x="{x}" y="{y}" width="{w:.0f}" height="30" rx="15" fill="{C["paper"]}" stroke="{C["line"]}"/>'
            f'<circle cx="{x + 16}" cy="{y + 15}" r="4.5" fill="{color}"/>'
            f'<text x="{x + 28}" y="{y + 19.5}" class="mono" font-size="{size}" fill="{C["ink2"]}">{text}</text></g>'), w


# ---------------------------------------------------------------- bannière
def header():
    W, H = 1200, 400
    b = [grid_bg(W, H)]
    b.append(f'<line x1="64" y1="0" x2="64" y2="{H}" stroke="{C["margin"]}" stroke-width="2"/>')
    b.append(f'<text x="100" y="82" class="mono fade" font-size="14" letter-spacing="3" fill="{C["muted"]}">'
             'M1 MIASHS · PAUL-VALÉRY MONTPELLIER 3 · 2026-2027</text>')
    b.append(f'<text x="98" y="160" class="serif fade" style="animation-delay:.15s" font-size="68" '
             f'font-weight="700" fill="{C["ink"]}" letter-spacing="-1">Florient Marchal</text>')
    b.append(f'<path class="draw" style="animation-delay:.6s" d="M102 182 C 210 172, 360 190, 470 178 S 600 174, 640 180" '
             f'fill="none" stroke="{C["red"]}" stroke-width="4" stroke-linecap="round"/>')
    b.append(f'<text x="100" y="230" class="sans fade" style="animation-delay:.35s" font-size="22" fill="{C["ink2"]}">'
             'Statistiques, science des données et outils web.</text>')
    # terminal
    tx, ty = 100, 262
    b.append(f'<g class="fade" style="animation-delay:.6s"><rect x="{tx}" y="{ty}" width="560" height="54" rx="10" '
             f'fill="{C["ink"]}"/><circle cx="{tx + 20}" cy="{ty + 27}" r="4" fill="{C["margin"]}"/>'
             f'<text x="{tx + 36}" y="{ty + 33}" class="mono" font-size="18" fill="#8fb0f0">&gt;</text></g>')
    cmd = "lm(curiosite ~ donnees + code)"
    cmd_show = "lm(curiosité ~ données + code)"
    cw = len(cmd) * 18 * 0.602
    x0 = tx + 58
    b.append(f'<defs><clipPath id="type"><rect x="{x0}" y="{ty}" width="0" height="54">'
             f'<animate attributeName="width" from="0" to="{cw + 4:.0f}" begin="1.1s" dur="2.2s" fill="freeze"/>'
             f'</rect></clipPath></defs>')
    b.append(f'<text x="{x0}" y="{ty + 33}" class="mono" font-size="18" fill="#e8eef9" clip-path="url(#type)">{cmd_show}</text>')
    b.append(f'<rect x="{x0}" y="{ty + 17}" width="10" height="21" fill="#8fb0f0" style="animation:blink 1s steps(1) infinite">'
             f'<animate attributeName="x" from="{x0}" to="{x0 + cw + 4:.0f}" begin="1.1s" dur="2.2s" fill="freeze"/></rect>')
    b.append(f'<text x="{tx + 4}" y="{ty + 86}" class="mono fade" style="animation-delay:3.5s" font-size="15" fill="{C["good"]}">'
             'R² = 0,97 · p &lt; 0,001 · résidus bien sages ✓</text>')
    # panneau graphique
    px, py, pw, ph = 770, 46, 380, 308
    b.append(f'<g class="fade" style="animation-delay:.3s">'
             f'<rect x="{px}" y="{py + 4}" width="{pw}" height="{ph}" rx="14" fill="#c9d2de" opacity=".5"/>'
             f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="14" fill="{C["paper"]}" stroke="{C["line"]}"/>'
             f'<text x="{px + 22}" y="{py + 32}" class="mono" font-size="12" letter-spacing="2" fill="{C["muted"]}">FIG. 1 · MOINDRES CARRÉS</text></g>')
    ox, oy = 812, 318
    b.append(f'<g class="fade" style="animation-delay:.5s" stroke="{C["ink2"]}" stroke-width="1.5" fill="none">'
             f'<path d="M{ox} {oy}H1124M{ox} {oy}V84"/><path d="M1118 {oy - 5}L1126 {oy}L1118 {oy + 5}M{ox - 5} 90L{ox} 82L{ox + 5} 90"/></g>')
    b.append(f'<text x="1112" y="{oy + 22}" class="serif fade" style="animation-delay:.5s" font-size="16" font-style="italic" fill="{C["ink2"]}">x</text>')
    b.append(f'<text x="{ox - 22}" y="96" class="serif fade" style="animation-delay:.5s" font-size="16" font-style="italic" fill="{C["ink2"]}">y</text>')
    xs = [840, 863, 886, 909, 932, 955, 978, 1001, 1024, 1047, 1070, 1093]
    noise = [12, -10, 8, -14, 6, 15, -9, 5, -12, 10, -6, 8]
    line = lambda x: 292 - 0.62 * (x - 826)
    for i, (x, n) in enumerate(zip(xs, noise)):
        y = line(x) + n
        if i in (1, 3, 8):
            b.append(f'<line x1="{x}" y1="{y:.0f}" x2="{x}" y2="{line(x):.0f}" stroke="{C["red"]}" stroke-width="1.5" '
                     f'stroke-dasharray="3 3" class="fade" style="animation-delay:3.0s"/>')
        col = C["red"] if i in (5, 9) else C["accent"]
        b.append(f'<circle cx="{x}" cy="{y:.0f}" r="6" fill="{col}" class="pop" style="animation-delay:{.7 + i * .09:.2f}s"/>')
    b.append(f'<line x1="826" y1="{line(826):.0f}" x2="1112" y2="{line(1112):.0f}" stroke="{C["ink"]}" stroke-width="2.5" '
             f'stroke-linecap="round" class="draw" style="animation-delay:1.9s"/>')
    b.append(f'<text x="840" y="128" class="serif fade" style="animation-delay:2.8s" font-size="20" font-style="italic" '
             f'fill="{C["ink"]}">y = β₀ + β₁x + ε</text>')
    return svg(W, H, "\n".join(b), label="Florient Marchal, M1 MIASHS : statistiques, science des données et outils web")


# ---------------------------------------------------------------- cartes
def card(W, H, color, kicker, title, lines, tags, icon, cta="Ouvrir", label=""):
    b = [f'<defs><clipPath id="k"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14"/></clipPath>'
         f'<pattern id="fg" width="16" height="16" patternUnits="userSpaceOnUse"><path d="M16 0H0V16" fill="none" '
         f'stroke="{C["fgrid"]}"/></pattern></defs>',
         f'<rect x="1" y="5" width="{W - 2}" height="{H - 6}" rx="14" fill="#c9d2de" opacity=".45"/>',
         f'<rect x="1" y="1" width="{W - 2}" height="{H - 6}" rx="14" fill="{C["paper"]}" stroke="{C["line"]}"/>',
         f'<rect x="1" y="1" width="7" height="{H}" fill="{color}" clip-path="url(#k)"/>',
         f'<rect x="34" y="30" width="84" height="84" rx="12" fill="{C["paper2"]}" stroke="{C["line"]}"/>',
         f'<rect x="35" y="31" width="82" height="82" rx="11" fill="url(#fg)"/>',
         f'<g transform="translate(34 30)">{icon}</g>',
         f'<text x="140" y="54" class="mono fade" font-size="12" letter-spacing="2" fill="{C["muted"]}">{kicker}</text>',
         f'<text x="139" y="92" class="serif fade" style="animation-delay:.1s" font-size="30" font-weight="700" fill="{C["ink"]}">{title}</text>']
    for i, ln in enumerate(lines):
        b.append(f'<text x="140" y="{128 + i * 24}" class="sans fade" style="animation-delay:.2s" font-size="16" fill="{C["ink2"]}">{ln}</text>')
    x = 34
    ty = H - 58
    for i, (t, col) in enumerate(tags):
        g, w = chip(x, ty, t, col, delay=.4 + i * .08, size=12)
        b.append(g)
        x += w + 8
    b.append(f'<g style="animation:nudge 2.4s ease-in-out infinite"><text x="{W - 34}" y="{ty + 20}" text-anchor="end" '
             f'class="sans" font-size="16" font-weight="600" fill="{color}">{cta} →</text></g>')
    return svg(W, H, "\n".join(b), label=label)


ICON_DICE = f'''<g style="transform-box:fill-box;transform-origin:center;animation:roll 3s ease-in-out infinite">
<rect x="18" y="18" width="48" height="48" rx="10" fill="{C["paper"]}" stroke="{C["red"]}" stroke-width="2.5"/>
<g fill="{C["red"]}"><circle cx="31" cy="31" r="4"/><circle cx="53" cy="31" r="4"/><circle cx="42" cy="42" r="4"/>
<circle cx="31" cy="53" r="4"/><circle cx="53" cy="53" r="4"/></g></g>'''
CSS_DICE = "@keyframes roll{0%,60%,100%{transform:rotate(0)} 75%{transform:rotate(-14deg)} 88%{transform:rotate(8deg)}}"

ICON_CHAT = f'''<path d="M14 20h46a8 8 0 0 1 8 8v20a8 8 0 0 1-8 8H34l-12 10v-10h-8a8 8 0 0 1-8-8V28a8 8 0 0 1 8-8z"
fill="{C["soft"]}" stroke="{C["accent"]}" stroke-width="2.5"/>
<g fill="{C["accent"]}"><circle cx="26" cy="38" r="4" style="animation:dot 1.2s infinite"/>
<circle cx="38" cy="38" r="4" style="animation:dot 1.2s .2s infinite"/><circle cx="50" cy="38" r="4" style="animation:dot 1.2s .4s infinite"/></g>'''
CSS_CHAT = "@keyframes dot{0%,60%,100%{opacity:.25} 30%{opacity:1}}"

ICON_SPROUT = f'''<path d="M18 68h48" stroke="{C["warn"]}" stroke-width="3" stroke-linecap="round"/>
<path class="draw" d="M42 68 C 42 56, 41 46, 42 32" fill="none" stroke="{C["good"]}" stroke-width="3" stroke-linecap="round"/>
<path class="pop" style="animation-delay:.9s" d="M42 46 C 30 46, 22 38, 22 28 C 34 28, 42 36, 42 46z" fill="{C["good"]}"/>
<path class="pop" style="animation-delay:1.2s" d="M42 38 C 52 38, 62 30, 62 20 C 50 20, 42 28, 42 38z" fill="#2fa266"/>'''

ICON_KANBAN = f'''<g fill="none" stroke="{C["line"]}" stroke-width="1.5"><rect x="12" y="16" width="18" height="52" rx="4"/>
<rect x="33" y="16" width="18" height="52" rx="4"/><rect x="54" y="16" width="18" height="52" rx="4"/></g>
<g fill="{C["warn"]}" opacity=".35"><rect x="15" y="22" width="12" height="9" rx="2"/><rect x="36" y="22" width="12" height="9" rx="2"/>
<rect x="57" y="22" width="12" height="9" rx="2"/><rect x="57" y="34" width="12" height="9" rx="2"/></g>
<rect x="15" y="36" width="12" height="9" rx="2" fill="{C["warn"]}" style="animation:move 4s ease-in-out infinite"/>'''
CSS_KANBAN = "@keyframes move{0%,15%{transform:translate(0,0)} 40%,55%{transform:translate(21px,0)} 80%,100%{transform:translate(42px,12px)}}"


def project_cards():
    W, H = 590, 250
    out = {}
    out["agentic"] = card(W, H, C["red"], "PROJET DE PROMO · AGENTS IA", "Casino Fantôme",
                          ["Un simulateur de casino 100 % fictif, codé par", "des agents IA et supervisé par 25 étudiants."],
                          [("React", "#149eca"), ("Vite", "#646cff"), ("Agents IA", C["red"])], ICON_DICE,
                          label="Casino Fantôme : projet de promo M1AgenticCoding")
    out["agentic"] = out["agentic"].replace("</style>", CSS_DICE + "</style>")
    out["pairia"] = card(W, H, C["accent"], "PROJET DE STAGE", "PairIA",
                         ["Une boutique de chaussures en ligne avec un", "assistant IA open source qui tourne en local."],
                         [("Python", "#3776ab"), ("PHP", "#777bb4"), ("IA locale", C["accent"])], ICON_CHAT,
                         label="PairIA : projet de stage, e-commerce avec chatbot IA local")
    out["pairia"] = out["pairia"].replace("</style>", CSS_CHAT + "</style>")
    out["agri"] = card(W, H, C["good"], "PROJET D'ÉQUIPE · DONNÉES", "Future-Agriculteur",
                       ["Un calendrier agricole intelligent : données,", "base SQL, modèles prédictifs et site web."],
                       [("Python", "#3776ab"), ("SQL", "#4479a1"), ("PHP", "#777bb4")], ICON_SPROUT,
                       label="Future-Agriculteur : calendrier agricole intelligent")
    out["orga"] = card(W, H, C["warn"], "PROJET D'ÉQUIPE · BIEN-ÊTRE", "Orga+",
                       ["Une plateforme pour étudiants : diagnostic des", "habitudes, visualisations et simulations."],
                       [("PHP", "#777bb4"), ("R", "#276dc3"), ("JavaScript", "#d4b106")], ICON_KANBAN,
                       label="Orga+ : plateforme d'organisation pour étudiants")
    out["orga"] = out["orga"].replace("</style>", CSS_KANBAN + "</style>")
    return out


# ---------------------------------------------------------------- carte vedette
def featured():
    W, H = 1200, 290
    b = [f'<defs><clipPath id="k"><rect x="1" y="1" width="{W - 2}" height="{H - 6}" rx="14"/></clipPath>'
         f'<pattern id="fg" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{C["fgrid"]}"/></pattern></defs>',
         f'<rect x="1" y="5" width="{W - 2}" height="{H - 6}" rx="14" fill="#c9d2de" opacity=".45"/>',
         f'<rect x="1" y="1" width="{W - 2}" height="{H - 6}" rx="14" fill="{C["paper"]}" stroke="{C["line"]}"/>',
         f'<rect x="760" y="1" width="440" height="{H}" fill="url(#fg)" clip-path="url(#k)"/>',
         f'<line x1="760" y1="1" x2="760" y2="{H - 5}" stroke="{C["margin"]}" stroke-width="2"/>',
         f'<rect x="1" y="1" width="8" height="{H}" fill="{C["accent"]}" clip-path="url(#k)"/>',
         f'<text x="44" y="56" class="mono fade" font-size="13" letter-spacing="2" fill="{C["muted"]}">PROJET PHARE · EN LIGNE</text>',
         f'<text x="42" y="104" class="serif fade" style="animation-delay:.1s" font-size="42" font-weight="700" fill="{C["ink"]}">Mes révisions</text>',
         f'<path class="draw" style="animation-delay:.5s" d="M45 120 C 120 113, 220 126, 318 116" fill="none" stroke="{C["red"]}" stroke-width="3.5" stroke-linecap="round"/>',
         f'<text x="44" y="160" class="sans fade" style="animation-delay:.2s" font-size="18" fill="{C["ink2"]}">Le site de révision de mon M1 : 7 cours, fiches et formulaires, flashcards,</text>',
         f'<text x="44" y="186" class="sans fade" style="animation-delay:.2s" font-size="18" fill="{C["ink2"]}">QCM, annales corrigées et TP R, Python et D3 exécutés dans le navigateur.</text>']
    x = 44
    for i, (t, col) in enumerate([("Svelte", "#ff3e00"), ("webR", "#276dc3"), ("Pyodide", "#3776ab"),
                                  ("D3.js", "#f9a03c"), ("KaTeX", "#008080"), ("Supabase", "#3ecf8e")]):
        g, w = chip(x, 216, t, col, delay=.5 + i * .08)
        b.append(g)
        x += w + 8
    b.append(f'<g style="animation:nudge 2.4s ease-in-out infinite"><text x="726" y="236" text-anchor="end" class="sans" '
             f'font-size="17" font-weight="600" fill="{C["accent"]}">Voir le site →</text></g>')
    # pile de flashcards à droite
    cx, cy = 980, 140
    b.append(f'<g transform="translate({cx} {cy}) rotate(-8)"><rect x="-110" y="-66" width="220" height="132" rx="12" fill="{C["paper2"]}" stroke="{C["line"]}"/></g>')
    b.append(f'<g transform="translate({cx} {cy}) rotate(5)"><rect x="-110" y="-66" width="220" height="132" rx="12" fill="{C["paper2"]}" stroke="{C["line"]}"/></g>')
    face = lambda tag, txt, sub, col, cls: (
        f'<g class="{cls}"><rect x="-110" y="-66" width="220" height="132" rx="12" fill="{C["paper"]}" stroke="{col}" stroke-width="2"/>'
        f'<text x="-92" y="-38" class="mono" font-size="11" letter-spacing="2" fill="{col}">{tag}</text>'
        f'<text x="0" y="6" text-anchor="middle" class="serif" font-size="22" font-weight="700" fill="{C["ink"]}">{txt}</text>'
        f'<text x="0" y="34" text-anchor="middle" class="sans" font-size="13" fill="{C["muted"]}">{sub}</text></g>')
    b.append(f'<g transform="translate({cx} {cy})"><g style="animation:flip 6s ease-in-out infinite">'
             + face("QUESTION", "Inertie totale ?", "ACP · flashcard 12/61", C["accent"], "fq")
             + face("RÉPONSE", "I = tr(VM)", "somme des valeurs propres", C["good"], "fr")
             + '</g></g>')
    css = ("@keyframes flip{0%,40%{transform:scaleX(1)} 50%{transform:scaleX(0)} 60%,90%{transform:scaleX(1)} 95%{transform:scaleX(0)} 100%{transform:scaleX(1)}}"
           ".fq{animation:fq 6s steps(1) infinite} .fr{animation:fr 6s steps(1) infinite}"
           "@keyframes fq{0%{opacity:1} 50%{opacity:0} 95%{opacity:1}} @keyframes fr{0%{opacity:0} 50%{opacity:1} 95%{opacity:0}}")
    return svg(W, H, "\n".join(b), css, label="Mes révisions : site de révision du M1 MIASHS")


# ---------------------------------------------------------------- outils
def tools():
    W, H = 1200, 230
    b = [grid_bg(W, H, pid="tg"),
         f'<line x1="64" y1="0" x2="64" y2="{H}" stroke="{C["margin"]}" stroke-width="2"/>',
         f'<text x="100" y="52" class="mono fade" font-size="13" letter-spacing="2" fill="{C["muted"]}">FORMULAIRE · À CONNAÎTRE PAR CŒUR</text>',
         f'<text x="98" y="92" class="serif fade" font-size="32" font-weight="700" fill="{C["ink"]}">Ma boîte à outils</text>']
    rows = [("01  DONNÉES", [("R", "#276dc3"), ("Python", "#3776ab"), ("Pandas", "#150458"), ("NumPy", "#4dabcf"),
                             ("Jupyter", "#f37626"), ("SQL", "#4479a1"), ("CouchDB", "#e42528"), ("ArangoDB", "#68a063")]),
            ("02  WEB", [("JavaScript", "#d4b106"), ("Svelte", "#ff3e00"), ("D3.js", "#f9a03c"), ("PHP", "#777bb4"),
                         ("Vite", "#646cff"), ("Git", "#f05032")])]
    d = .3
    for r, (lab, items) in enumerate(rows):
        y = 124 + r * 50
        b.append(f'<text x="100" y="{y + 20}" class="mono fade" font-size="13" font-weight="600" fill="{C["accent"]}">{lab}</text>')
        x = 230
        for t, col in items:
            g, w = chip(x, y, t, col, delay=d)
            b.append(g)
            x += w + 10
            d += .06
    return svg(W, H, "\n".join(b), label="Outils : R, Python, Pandas, NumPy, Jupyter, SQL, CouchDB, ArangoDB, JavaScript, Svelte, D3.js, PHP, Vite, Git")


files = {"header.svg": header(), "revision.svg": featured(), "tools.svg": tools()}
for k, v in project_cards().items():
    files[f"{k}.svg"] = v
for name, content in files.items():
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)
print(sorted(files))
