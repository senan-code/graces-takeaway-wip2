#!/usr/bin/env python3
"""Build script for the Grace's Takeaway site. No dependencies, Python 3.8+.

    python3 tools/build.py

What it does:
  1. Checks that the opening hours in index.html agree with each other
     (the JSON-LD block in <head> and the hours table). Stops if not.
  2. Builds menu.html from the MENU data below, reusing the header, footer
     and JSON-LD from index.html so they never drift apart.
  3. Builds graces-preview.html: one self-contained file (CSS, JS and logo
     inlined, home and menu on one page) that can be sent or opened offline.

To change a price or item: edit MENU below, then run the script.
Source: the owner's printed menu (photo supplied Oct 2026). Prices may be
out of date and allergen numbers are not yet transcribed; confirm with the owner.
"""

import base64
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# MENU DATA
# Each item: (name, price, description). Price is a number in euro, None for
# "no individual price", or a string printed as-is.
# ---------------------------------------------------------------------------

MENU = [
    {
        "id": "chicken",
        "title": "Grace's chicken",
        "intro": "All Grace's fried chicken is cooked from fresh in a pressure-sealed chamber, "
                 "using our own special recipe coating.",
        "groups": [
            {
                "title": None,
                "items": [
                    ("Junior Box", 4.50, "1 piece: drumstick, wing, thigh"),
                    ("Breast Box", 6.20, None),
                    ("Snack Box", 6.40, "2 pieces: drumstick, wing, thigh"),
                    ("Dinner Box", 7.50, "3 pieces: drumstick, wing, thigh"),
                    ("Fillet Box", 6.30, None),
                    ("3 Fillet Strip Snack Box", 6.50, None),
                    ("5 Fillet Strip Dinner Box", 8.00, None),
                    ("Family Box", 22.50, "8 pieces, 3 chips, Grace's gravy and a large Coke"),
                    ("Breast", 3.70, None),
                    ("Drumstick", 2.50, None),
                    ("Wing", 2.50, None),
                    ("Thigh", 2.50, None),
                    ("Grace's Fillet", 3.50, None),
                ],
                "foot": ["Add any topping to a chicken box for €1.20."],
            },
            {
                "title": "Grace's breast in a bun",
                "items": [
                    ("Classic", 5.50, "Creamy mayonnaise, iceberg lettuce, ripe tomato"),
                    ("BBQ Melt", 6.40, "Smokey BBQ sauce, mayonnaise, cheese, crispy bacon and iceberg lettuce"),
                ],
            },
            {
                "title": "Grace's chicken fillet strips",
                "items": [
                    ("3 Fillet Strips + Dip", 4.00, None),
                    ("5 Fillet Strips + Dip", 5.50, None),
                ],
            },
        ],
    },
    {
        "id": "burgers",
        "title": "Burgers",
        "groups": [
            {
                "title": None,
                "items": [
                    ("Regular Burger", 2.70, None),
                    ("Cheese Burger", 3.00, None),
                    ("Salad Burger", 3.40, None),
                    ("Double Cheese Burger", 4.20, None),
                    ("Quarter Pounder with Salad", 4.40, None),
                    ("Quarter Pounder with Cheese & Salad", 4.70, None),
                    ("Half Pounder with Salad", 5.50, None),
                    ("Farmhouse Quarter Pounder", 5.90, "Served with bacon, egg, red sauce and onions"),
                    ("Chicken Burger", 4.20, None),
                    ("Ribsteak Burger", 4.30, None),
                    ("Veggie Sandwich with Cheese & Salad", 2.70, None),
                    ("Veggie Burger", 4.00, None),
                    ("Add cheese", 0.30, None),
                    ("Add bacon / egg", 1.00, None),
                ],
            },
        ],
    },
    {
        "id": "kebabs",
        "title": "Kebabs",
        "intro": "All our kebabs use only the highest quality ingredients and are cooked fresh to order.",
        "groups": [
            {
                "title": None,
                "items": [
                    ("Doner Kebab", 6.20, None),
                    ("Doner Kebab Box", 7.50, None),
                    ("Tandoori Chicken Kebab", 6.50, None),
                    ("Tandoori Chicken Kebab Box", 7.80, None),
                    ("Mixed Kebab", 6.50, None),
                    ("Mixed Kebab Box", 7.80, None),
                    ("Veggie Kebab", 5.50, "Made with a veggie burger"),
                    ("Veggie Kebab Box", 6.50, "Made with a veggie burger"),
                    ("Southern Fried Chicken Fillet Kebab", 6.80, None),
                    ("Southern Fried Chicken Fillet Kebab Box", 7.80, None),
                ],
                "foot": ["All served with mixed salad, garlic and chilli sauce."],
            },
        ],
    },
    {
        "id": "wraps",
        "title": "Wraps",
        "groups": [
            {
                "title": None,
                "items": [
                    ("All Wraps", 6.20, None),
                ],
                "choices": [
                    ("Choose one sauce", "Garlic, taco, curry, sweet chilli mayo, BBQ, mayo, red sauce, "
                                         "Grace's gravy or spicy chilli"),
                    ("Choose one meat filling", "Grace's chicken fillet strips, ribsteak, 4oz burger, sausages, "
                                                "taco mince, doner kebab or chicken kebab"),
                    ("Choose up to four toppings", "Chips, cheese, lettuce, onion or tomato"),
                ],
            },
            {
                "title": None,
                "items": [
                    ("Wrap, no meat", 5.50, None),
                    ("Add another meat filling", 2.50, None),
                    ("Add bacon", 1.00, None),
                ],
            },
        ],
    },
    {
        "id": "pizza",
        "title": "Pizza",
        "groups": [
            {
                "title": None,
                "banner": [("Small 10″", 8.50), ("Large 14″", 12.50)],
                "items": [
                    ("Margherita", "10″ €7.00 · 14″ €11.00", "Mozzarella cheese and Grace's fresh pizza sauce"),
                    ("Pepperoni", None, "Mozzarella cheese and pepperoni"),
                    ("Romana", None, "Mozzarella cheese, ham and mushroom"),
                    ("Hawaiian", None, "Ham and pineapple"),
                    ("Etna", None, "Mozzarella cheese, chorizo, jalapeño peppers, onions, peppers and chilli flakes"),
                    ("Rustica", None, "Goats cheese, sun-ripened tomatoes, onion and fresh basil"),
                    ("Mediterranean", None, "Mozzarella cheese, salami, ham, mushroom and olives"),
                    ("BBQ", None, "Mozzarella cheese, BBQ sauce, onions, peppers, chicken and bacon"),
                    ("Vegetarian", None, "Mozzarella cheese, onion, peppers, sweetcorn and mushroom"),
                    ("Doner", None, "Mozzarella cheese, doner meat, garlic and spicy chilli sauce"),
                ],
                "choices": [
                    ("Make your own pizza with up to 4 toppings",
                     "Mozzarella, pepperoni, salami, ham, chorizo, chicken, bacon, mushrooms, olives, sweetcorn, "
                     "onions, peppers, pineapple, jalapeño peppers, sun-ripened tomatoes, goats cheese, fresh basil"),
                ],
            },
            {
                "title": "Garlic bread & sweet",
                "items": [
                    ("Garlic Pizza Bread", 4.50, None),
                    ("Garlic Pizza Bread with Cheese", 5.50, None),
                    ("Nutella Bites", 4.00, None),
                ],
            },
        ],
    },
    {
        "id": "chips",
        "title": "Chips",
        "groups": [
            {
                "title": None,
                "items": [
                    ("Half Chip", 2.15, "1 scoop"),
                    ("Small Chip", 3.00, "2 scoops"),
                    ("Salad Chip", 5.50, None),
                    ("Chip Butty", 3.60, None),
                    ("1 Topped Chip", 4.50, None),
                    ("2 Topped Chip", 5.50, None),
                    ("Bacon & Cheese Chip", 5.85, None),
                    ("Taco Mince Chip", 6.50, "Served with mince, cheese and taco sauce"),
                    ("Extra toppings", 0.65, "Cheese, curry, Grace's gravy, taco, mayo, red sauce, garlic mayo"),
                ],
            },
        ],
    },
    {
        "id": "fish",
        "title": "Fish",
        "groups": [
            {
                "title": None,
                "items": [
                    ("Fresh Beer Battered Fish", 6.00, "Served with lemon and tartare sauce"),
                    ("Fresh Fish Supper Box", 8.00, None),
                ],
            },
        ],
    },
    {
        "id": "sides",
        "title": "Sides & dips",
        "groups": [
            {
                "title": "Sides",
                "items": [
                    ("Bacon / Egg", 1.00, None),
                    ("Sausage", 1.30, None),
                    ("Battered Sausage", 1.60, None),
                    ("Onion Rings", 3.50, "Homemade"),
                    ("Chicken Nuggets x6", 3.00, None),
                    ("Chicken Chunks x6", 3.70, "Succulent breast meat in a light batter"),
                ],
            },
            {
                "title": "Dips",
                "items": [
                    ("Curry", 1.70, None),
                    ("Garlic", 1.70, None),
                    ("Taco", 1.70, None),
                    ("BBQ", 1.70, None),
                    ("Sweet Chilli Mayo", 1.70, None),
                    ("Mayo", 1.40, None),
                    ("Red Sauce", 0.80, None),
                    ("Spicy Chilli", 1.90, None),
                    ("Grace's Gravy", 1.70, "Homemade"),
                ],
            },
        ],
    },
    {
        "id": "kids",
        "title": "Kids' meals",
        "groups": [
            {
                "title": None,
                "items": [
                    ("Chicken Nugget Meal", 4.20, "100% breast meat"),
                    ("Cheese Burger / Burger Meal", 4.20, "100% Irish beef"),
                    ("Sausage Meal", 4.20, None),
                ],
                "foot": ["All kids' meals include a Capri-Sun drink."],
            },
        ],
    },
]

NAV_LABELS = {
    "chicken": "Chicken", "burgers": "Burgers", "kebabs": "Kebabs", "wraps": "Wraps",
    "pizza": "Pizza", "chips": "Chips", "fish": "Fish", "sides": "Sides & dips", "kids": "Kids",
}

# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

e = html.escape


def euro(value):
    return f"€{value:.2f}"


def render_price(price):
    if price is None:
        return ""
    if isinstance(price, str):
        return f'<span class="price">{e(price)}</span>'
    return f'<span class="price">{euro(price)}</span>'


def render_group(group):
    out = ['<div class="menu-group">']
    if group.get("title"):
        out.append(f'<h3>{e(group["title"])}</h3>')
    if group.get("banner"):
        sizes = "".join(f"<div>{e(label)} <span>{euro(p)}</span></div>" for label, p in group["banner"])
        out.append(f'<div class="size-banner">{sizes}</div>')
    out.append('<ul class="menu-list">')
    for name, price, desc in group["items"]:
        out.append('<li class="menu-item">')
        out.append(f'<span class="name">{e(name)}</span>{render_price(price)}')
        if desc:
            out.append(f'<span class="desc">{e(desc)}</span>')
        out.append("</li>")
    out.append("</ul>")
    if group.get("choices"):
        out.append('<ul class="choices">')
        for label, text in group["choices"]:
            out.append(f"<li><strong>{e(label)}:</strong> {e(text)}</li>")
        out.append("</ul>")
    if group.get("foot"):
        out.append('<div class="menu-foot">' + "".join(f"<p>{e(t)}</p>" for t in group["foot"]) + "</div>")
    out.append("</div>")
    return "\n".join(out)


def render_menu_body():
    nav = "".join(f'<li><a href="#{c["id"]}">{e(NAV_LABELS[c["id"]])}</a></li>' for c in MENU)
    sections = []
    for cat in MENU:
        parts = [f'<section class="menu-section" id="{cat["id"]}" aria-labelledby="{cat["id"]}-h">',
                 f'<h2 id="{cat["id"]}-h">{e(cat["title"])}</h2>']
        if cat.get("intro"):
            parts.append(f'<p class="menu-intro">{e(cat["intro"])}</p>')
        parts.extend(render_group(g) for g in cat["groups"])
        parts.append("</section>")
        sections.append("\n".join(parts))
    return f"""<div class="page-hero">
  <div class="wrap">
    <p class="status" data-status hidden></p>
    <h1>Our menu</h1>
    <p>Fried chicken, burgers, kebabs, wraps, pizza, chips and more. Call <a href="tel:+35351643759" style="color:var(--gold)">051 643 759</a> to order.</p>
  </div>
</div>
<nav class="cat-nav" aria-label="Menu sections">
  <div class="wrap"><ul>{nav}</ul></div>
</nav>
<div class="wrap">
  <div class="menu-notice" role="note">
    <strong>Allergies:</strong> if you have a food allergy or intolerance, please tell us when you order
    and ask us about the allergens in any dish. Prices may change; please check when ordering.
  </div>
{chr(10).join(sections)}
</div>"""


# ---------------------------------------------------------------------------
# Helpers for reading index.html
# ---------------------------------------------------------------------------

def between(text, start, end):
    i = text.index(start)
    j = text.index(end, i) + len(end)
    return text[i:j]


def jsonld_block(index_html):
    m = re.search(r'<script type="application/ld\+json">.*?</script>', index_html, re.S)
    if not m:
        sys.exit("ERROR: no JSON-LD block found in index.html")
    return m.group(0)


def fmt_time(hhmm):
    h, m = map(int, hhmm.split(":"))
    suffix = "pm" if h >= 12 else "am"
    h12 = h % 12 or 12
    return f"{h12}{':%02d' % m if m else ''}{suffix}"


def check_hours(index_html):
    """The JSON-LD hours and the visible table must say the same thing."""
    data = json.loads(re.sub(r"^<script[^>]*>|</script>$", "", jsonld_block(index_html)))
    expected = {}
    for spec in data["openingHoursSpecification"]:
        for day in spec["dayOfWeek"]:
            expected[day] = f'{fmt_time(spec["opens"])} – {fmt_time(spec["closes"])}'
    rows = re.findall(r'<tr data-day="(\w+)"[^>]*>.*?<td>(.*?)</td></tr>', index_html)
    if len(rows) != 7:
        sys.exit(f"ERROR: expected 7 rows in the hours table, found {len(rows)}")
    problems = []
    for day, shown in rows:
        want = expected.get(day, "Closed")
        if html.unescape(shown).strip() != want:
            problems.append(f"  {day}: table says '{shown}', JSON-LD says '{want}'")
    if problems:
        sys.exit("ERROR: opening hours in index.html disagree:\n" + "\n".join(problems))
    print("Hours check: table and JSON-LD agree.")


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build_menu_page(index_html, menu_body):
    head_links = between(index_html, '<meta name="robots"', 'href="styles.css">')
    header = between(index_html, "<!-- HEADER", "<!-- /HEADER -->")
    footer = between(index_html, "<!-- FOOTER", "<!-- /FOOTER -->")
    # Same-page links on the home page need to point back to it from here.
    for frag in ("#hours", "#find-us", "#order"):
        header = header.replace(f'href="{frag}"', f'href="index.html{frag}"')
        footer = footer.replace(f'href="{frag}"', f'href="index.html{frag}"')
    header = header.replace('<a href="menu.html">', '<a href="menu.html" aria-current="page">')
    footer = footer.replace('<a class="btn btn-outline" href="menu.html">Menu</a>',
                            '<a class="btn btn-outline" href="index.html">Home</a>')
    return f"""<!doctype html>
<!-- GENERATED by tools/build.py from the MENU data. Do not edit by hand. -->
<html lang="en-IE">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Menu | Grace's Takeaway, Piltown</title>
  <meta name="description" content="Full menu and prices for Grace's Takeaway, Main Street, Piltown: fried chicken, burgers, kebabs, wraps, pizza, chips, fish, sides and kids' meals.">
  {head_links}
  {jsonld_block(index_html)}
  <script src="script.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  {header}
  <main id="main">
{menu_body}
  </main>
  {footer}
</body>
</html>
"""


def build_preview(index_html, menu_body):
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    js = (ROOT / "script.js").read_text(encoding="utf-8")
    logo = base64.b64encode((ROOT / "assets" / "logo.png").read_bytes()).decode("ascii")
    page = index_html
    page = page.replace('<link rel="stylesheet" href="styles.css">', f"<style>\n{css}\n</style>")
    page = page.replace('<script src="script.js" defer></script>', "")
    page = page.replace("</body>", f"<script>\n{js}\n</script>\n</body>")
    page = page.replace("assets/logo.png", f"data:image/png;base64,{logo}")
    page = page.replace('href="index.html"', 'href="#main"')
    page = page.replace('href="menu.html#', 'href="#')
    page = page.replace('href="menu.html"', 'href="#menu"')
    page = page.replace("</main>", f'<section id="menu">\n{menu_body}\n</section>\n</main>')
    return "<!-- GENERATED by tools/build.py: single-file preview (home + menu). Do not edit by hand. -->\n" + page


def main():
    index_html = (ROOT / "index.html").read_text(encoding="utf-8")
    check_hours(index_html)
    menu_body = render_menu_body()
    (ROOT / "menu.html").write_text(build_menu_page(index_html, menu_body), encoding="utf-8")
    (ROOT / "graces-preview.html").write_text(build_preview(index_html, menu_body), encoding="utf-8")
    items = sum(len(g["items"]) for c in MENU for g in c["groups"])
    print(f"Built menu.html and graces-preview.html: {len(MENU)} categories, {items} items.")


if __name__ == "__main__":
    main()
