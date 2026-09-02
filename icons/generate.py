#!/usr/bin/env python3
import urllib.request, os, re

OUT = os.path.dirname(os.path.abspath(__file__))
BG  = "#5c36d8"
FG  = "#42e790"

SECTORS = [
    ("IT-u-Informatik",               "device-laptop"),
    ("Gesundheit-u-Pflege",           "stethoscope"),
    ("Landwirtschaft-u-Natur",        "tractor"),
    ("Elektrotechnik-u-Elektronik",   "bolt"),
    ("Metalltechnik-u-Maschinenbau",  "engine"),
    ("Bau-u-Tiefbau",                 "crane"),
    ("Hochbau-u-Ausbau",              "building"),
    ("Logistik-u-Transport",          "truck"),
    ("Handel-u-Kaufmaennisch",        "shopping-cart"),
    ("Gastronomie-u-Hotel",           "chef-hat"),
    ("Soziales-u-Paedagogik",         "school"),
    ("Buero-u-Verwaltung",            "briefcase"),
    ("Fahrzeugtechnik",               "car"),
    ("Chemie-Pharma-u-Labor",         "flask"),
    ("Medien-u-Marketing",            "speakerphone"),
    ("Holz-u-Moebel",                 "armchair"),
    ("Lebensmittelhandwerk",          "bread"),
    ("Maler-u-Raumausstattung",       "paint"),
    ("Textil-u-Bekleidung",           "shirt"),
    ("Koerperpflege-u-Beauty",        "scissors"),
    ("Umwelt-u-Entsorgung",           "recycle"),
    ("Druck-u-Papier",                "printer"),
    ("Sicherheit-u-Service",          "shield-lock"),
    ("Technisches-Zeichnen-u-Vermessung", "ruler-measure"),
    ("Schmuck-Optik-u-Uhren",         "diamond"),
    ("Musikinstrumentenbau",          "guitar-pick"),
    ("Glas-u-Keramik",                "glass-full"),
    ("Leder-u-Schuh",                 "shoe"),
    ("Bergbau-u-Rohstoffe",           "pick"),
]

BASE_URL = "https://raw.githubusercontent.com/tabler/tabler-icons/main/icons/outline/{}.svg"

def fetch_paths(name):
    url = BASE_URL.format(name)
    with urllib.request.urlopen(url) as r:
        svg = r.read().decode()
    # extract inner elements (path, circle, line, polyline, rect, etc.)
    inner = re.sub(r'<svg[^>]*>', '', svg)
    inner = re.sub(r'</svg>', '', inner).strip()
    # strip comments, fill/stroke attrs
    inner = re.sub(r'<!--.*?-->', '', inner, flags=re.DOTALL)
    inner = re.sub(r'\s*(stroke|fill)="[^"]*"', '', inner)
    return inner.strip()

def make_icon(sector, icon_name):
    paths = fetch_paths(icon_name)
    # 512×512 canvas; tabler viewBox is 0 0 24 24
    # scale icon to ~300×300 centered in 512×512 → translate(106,106) scale(12.5)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <rect width="512" height="512" rx="96" fill="{BG}"/>
  <g transform="translate(106,106) scale(12.5)" stroke="{FG}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none">
    {paths}
  </g>
</svg>'''
    out_path = os.path.join(OUT, f"{sector}.svg")
    with open(out_path, "w") as f:
        f.write(svg)
    print(f"  ✓ {sector} ({icon_name})")

print("Generating 29 industry icons…")
for sector, icon in SECTORS:
    try:
        make_icon(sector, icon)
    except Exception as e:
        print(f"  ✗ {sector} ({icon}): {e}")
print("Done.")
