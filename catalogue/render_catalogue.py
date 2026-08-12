#!/usr/bin/env python3
"""jobreadycv.za WhatsApp catalogue slides + product tiles."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/home/user/sfiso/catalogue")
SLIDES = ROOT / "slides"
PRODUCTS = ROOT / "products"
SLIDES.mkdir(parents=True, exist_ok=True)
PRODUCTS.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
S = 1080  # square product tile

NAVY = (11, 18, 32, 255)
NAVY2 = (16, 24, 40, 255)
GOLD = (196, 162, 101, 255)
GOLD_DIM = (196, 162, 101, 80)
CREAM = (244, 237, 224, 255)
MUTED = (196, 186, 170, 255)
ALERT = (232, 93, 76, 255)
OK = (125, 206, 160, 255)
WA = (37, 211, 102, 255)
INK = (11, 18, 32, 255)

SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def fnt(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def bg(w=W, h=H, variant=0) -> Image.Image:
    img = Image.new("RGBA", (w, h), NAVY)
    px = img.load()
    for y in range(h):
        t = y / h
        for x in range(w):
            cx, cy = (x - w / 2) / w, (y - h / 2) / h
            v = 1 - min(1.0, (cx * cx * 1.2 + cy * cy) * 0.9)
            r = int((11 + 7 * t) * (0.70 + 0.30 * v))
            g = int((18 + 8 * t) * (0.70 + 0.30 * v))
            b = int((32 + 12 * t + variant) * (0.74 + 0.26 * v))
            px[x, y] = (r, g, b, 255)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 10], fill=GOLD)
    d.rectangle([0, h - 10, w, h], fill=GOLD)
    return img


def tw(draw, text, font) -> float:
    return draw.textlength(text, font=font)


def wrap(draw, text, font, max_w) -> list[str]:
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if tw(draw, trial, font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def center(draw, text, font, y, fill=CREAM):
    draw.text(((W - tw(draw, text, font)) / 2, y), text, font=font, fill=fill)
    box = font.getbbox(text)
    return y + (box[3] - box[1])


def kicker(draw, text, y=90):
    font = fnt(SANS_B, 22)
    t = text.upper()
    center(draw, t, font, y, GOLD)
    ww = tw(draw, t, font)
    draw.rectangle([W / 2 - 36, y + 36, W / 2 + 36, y + 40], fill=GOLD)
    return y + 70


def wordmark(draw, y=None):
    font = fnt(SANS, 28)
    label = "jobreadycv.za"
    yy = H - 92 if y is None else y
    center(draw, label, font, yy, GOLD)


def save(img: Image.Image, folder: Path, name: str) -> Path:
    p = folder / name
    img.convert("RGB").save(p, "PNG", optimize=True)
    print("wrote", p)
    return p


def rounded(draw, box, r, fill=None, outline=None, width=2):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def slide_01_cover():
    img = bg(variant=0)
    d = ImageDraw.Draw(img)
    kicker(d, "WHATSAPP CATALOGUE  ·  2026")
    y = 360
    y = center(d, "Get job-ready.", fnt(SERIF_B, 78), y, CREAM) + 18
    y = center(d, "Get hired.", fnt(SERIF_B, 78), y, GOLD) + 50
    sub = fnt(SANS, 32)
    for line in wrap(d, "ATS-ready CVs, cover letters and LinkedIn — written for South Africa, not Brooklyn.", sub, 860):
        y = center(d, line, sub, y, MUTED) + 10
    # stats
    y = 980
    stats = [("3.2×", "more callbacks"), ("48k+", "CVs built"), ("4.9", "from 2,400 reviews")]
    gap = 320
    x0 = 90
    for i, (n, l) in enumerate(stats):
        xx = x0 + i * gap
        d.text((xx, y), n, font=fnt(SANS_B, 52), fill=GOLD)
        d.text((xx, y + 70), l, font=fnt(SANS, 22), fill=MUTED)
    # wa pill
    rounded(d, [180, 1380, 900, 1500], 60, fill=WA)
    d.text((330, 1412), "Chat on WhatsApp", font=fnt(SANS_B, 36), fill=INK)
    center(d, "+27 68 251 0828  ·  no forms, no card", fnt(SANS, 24), 1540, MUTED)
    wordmark(d)
    return save(img, SLIDES, "01-cover.png")


def slide_02_pain():
    img = bg(variant=1)
    d = ImageDraw.Draw(img)
    kicker(d, "WHY THE SILENCE")
    y = 340
    y = center(d, "80 applications.", fnt(SANS_B, 70), y, CREAM) + 8
    y = center(d, "Zero callbacks.", fnt(SANS_B, 70), y, ALERT) + 50
    body = fnt(SANS, 34)
    copy = [
        "It's usually not your degree.",
        "It's the file.",
        "",
        "The robot at the bank never opened it.",
        "The Sandton recruiter gave you 6 seconds.",
        "Page one did no work.",
    ]
    y = 780
    for line in copy:
        fill = GOLD if "file" in line else MUTED
        if not line:
            y += 20
            continue
        y = center(d, line, body, y, fill) + 14
    wordmark(d)
    return save(img, SLIDES, "02-pain.png")


def slide_03_kit():
    img = bg()
    d = ImageDraw.Draw(img)
    kicker(d, "THE KIT")
    center(d, "Four things that get you in the room.", fnt(SERIF_B, 40), 200, CREAM)
    items = [
        ("01", "ATS CV", "SA format. 2–3 pages. Passes SuccessFactors, Oracle, Workday, PNet."),
        ("02", "Cover letter", "Sounds like you on a good day. Names the desk, not ChatGPT."),
        ("03", "LinkedIn rewrite", "Headline recruiters actually search. Role · proof · city."),
        ("04", "Interview brief", "Talking points from YOUR story. Walk in fluent."),
    ]
    y = 320
    for num, title, desc in items:
        rounded(d, [80, y, 1000, y + 280], 22, outline=GOLD, width=2)
        d.text((120, y + 36), num, font=fnt(SANS_B, 26), fill=GOLD)
        d.text((220, y + 28), title, font=fnt(SANS_B, 40), fill=CREAM)
        yy = y + 110
        for line in wrap(d, desc, fnt(SANS, 28), 760):
            d.text((220, yy), line, font=fnt(SANS, 28), fill=MUTED)
            yy += 38
        y += 310
    wordmark(d)
    return save(img, SLIDES, "03-kit.png")


def plan_slide(fname, kicker_t, name, price, note, bullets, badge=None, accent=GOLD):
    img = bg()
    d = ImageDraw.Draw(img)
    kicker(d, kicker_t)
    if badge:
        bw = tw(d, badge, fnt(SANS_B, 22)) + 48
        rounded(d, [(W - bw) / 2, 200, (W + bw) / 2, 258], 20, fill=accent)
        center(d, badge, fnt(SANS_B, 22), 210, INK)
        y = 310
    else:
        y = 240
    y = center(d, name, fnt(SERIF_B, 72), y, CREAM) + 8
    y = center(d, price, fnt(SANS_B, 92), y + 10, accent) + 8
    y = center(d, note, fnt(SANS, 28), y + 8, MUTED) + 50
    box_top = y
    box_h = 80 + len(bullets) * 88
    rounded(d, [80, box_top, 1000, box_top + box_h], 24, outline=GOLD, width=2)
    yy = box_top + 40
    for b in bullets:
        d.text((130, yy), "✓", font=fnt(SANS_B, 34), fill=OK)
        xx = 200
        for line in wrap(d, b, fnt(SANS, 30), 720):
            d.text((xx, yy + 4), line, font=fnt(SANS, 30), fill=CREAM)
            yy += 40
        yy += 28
    wordmark(d)
    return save(img, SLIDES, fname)


def slide_07_compare():
    img = bg(variant=1)
    d = ImageDraw.Draw(img)
    kicker(d, "PICK YOUR HUNT")
    center(d, "Start free. Upgrade the month you're applying.", fnt(SANS, 28), 200, MUTED)
    headers = ["", "Starter", "Pro", "Career"]
    rows = [
        ("Price", "R0", "R99/mo", "R199/mo"),
        ("CVs", "1", "Unlimited", "Unlimited"),
        ("Letters", "Basic draft", "Unlimited", "Unlimited"),
        ("ATS score", "Yes", "Priority", "Priority"),
        ("LinkedIn", "—", "Full rewrite", "Full + banner"),
        ("Tailor ad", "—", "One click", "Per vacancy"),
        ("Interview", "—", "—", "Every application"),
        ("Human review", "—", "—", "1 / month"),
    ]
    y = 280
    cols = [90, 360, 600, 820]
    h = 88
    rounded(d, [70, y, 1010, y + h], 16, fill=GOLD)
    for j, cell in enumerate(headers):
        d.text((cols[j], y + 28), cell, font=fnt(SANS_B, 26), fill=INK)
    y += h + 10
    stripe = (22, 32, 48, 255)
    for i, row in enumerate(rows):
        if i % 2 == 0:
            rounded(d, [70, y, 1010, y + h], 10, fill=stripe)
        for j, cell in enumerate(row):
            font = fnt(SANS_B, 24) if j == 0 else fnt(SANS, 24)
            color = GOLD if j == 0 else CREAM
            if cell == "—":
                color = (130, 130, 140, 255)
            d.text((cols[j], y + 28), cell, font=font, fill=color)
        y += h
    center(d, "Cancel the month you land the offer.", fnt(SANS, 26), y + 30, MUTED)
    wordmark(d)
    return save(img, SLIDES, "07-compare.png")


def slide_08_proof():
    img = bg()
    d = ImageDraw.Draw(img)
    kicker(d, "FROM OVERLOOKED TO IN THE ROOM")
    quotes = [
        ("Thandiwe · Discovery · Sandton", "Three interviews in two weeks — including the one I accepted."),
        ("Sipho · Takealot · Cape Town", "A recruiter messaged me four days after the LinkedIn rewrite."),
        ("Thabo · Woolworths · Joburg", "Six months of silence. Two tailored CVs. Then the panel."),
        ("Anika · Standard Bank · Pretoria", "Rebuilt Sunday. Sent Monday. Offer signed Friday."),
    ]
    y = 250
    for who, q in quotes:
        rounded(d, [80, y, 1000, y + 300], 20, outline=GOLD, width=2)
        qq = f'“{q}”'
        yy = y + 36
        for line in wrap(d, qq, fnt(SERIF, 30), 820):
            d.text((120, yy), line, font=fnt(SERIF, 30), fill=CREAM)
            yy += 42
        d.text((120, y + 230), who, font=fnt(SANS, 22), fill=GOLD)
        y += 330
    wordmark(d)
    return save(img, SLIDES, "08-proof.png")


def slide_09_how():
    img = bg(variant=1)
    d = ImageDraw.Draw(img)
    kicker(d, "HOW IT WORKS")
    center(d, "No eight-page wizard. No card up front.", fnt(SANS, 28), 200, MUTED)
    steps = [
        ("01", "WhatsApp us", "Role, city, and your current CV — even a photo of a printed one."),
        ("02", "We shape it", "SA English. ATS-safe. Proof instead of duties. You stay in control."),
        ("03", "You apply today", "PDF + Word. LinkedIn paste. Interview talking points if you're on Career."),
    ]
    y = 320
    for num, title, desc in steps:
        d.ellipse([90, y + 10, 190, y + 110], outline=GOLD, width=3)
        d.text((112, y + 36), num, font=fnt(SANS_B, 28), fill=GOLD)
        d.text((230, y + 18), title, font=fnt(SANS_B, 42), fill=CREAM)
        yy = y + 90
        for line in wrap(d, desc, fnt(SANS, 30), 740):
            d.text((230, yy), line, font=fnt(SANS, 30), fill=MUTED)
            yy += 40
        y += 340
    rounded(d, [160, 1480, 920, 1590], 55, fill=WA)
    d.text((300, 1510), "Send the messy draft", font=fnt(SANS_B, 34), fill=INK)
    wordmark(d)
    return save(img, SLIDES, "09-how.png")


def slide_10_cta():
    img = bg()
    d = ImageDraw.Draw(img)
    kicker(d, "YOUR MOVE")
    y = 340
    y = center(d, "Your next interview", fnt(SERIF_B, 58), y, CREAM) + 10
    y = center(d, "is one honest CV away.", fnt(SERIF_B, 58), y, GOLD) + 50
    for line in [
        "We do not sell jobs.",
        "We do not take your ID.",
        "We do not charge a placement fee.",
        "We write the file the robot can read",
        "and the human will stop for.",
    ]:
        y = center(d, line, fnt(SANS, 32), y, MUTED) + 12
    rounded(d, [140, 1100, 940, 1230], 65, fill=WA)
    d.text((250, 1138), "WhatsApp +27 68 251 0828", font=fnt(SANS_B, 32), fill=INK)
    center(d, "Say: “I want a CV that gets interviews.”", fnt(SANS, 26), 1280, CREAM)
    center(d, "Starter R0  ·  Pro R99/mo  ·  Career R199/mo", fnt(SANS, 24), 1360, GOLD)
    center(d, "Usually reply in minutes.", fnt(SANS, 24), 1440, MUTED)
    wordmark(d)
    return save(img, SLIDES, "10-cta.png")


def product_tile(fname, eyebrow, title, price, lines, badge=None):
    img = bg(S, S, variant=0)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S, 10], fill=GOLD)
    d.rectangle([0, S - 10, S, S], fill=GOLD)
    if badge:
        rounded(d, [70, 70, 360, 140], 18, fill=GOLD)
        d.text((92, 88), badge.upper(), font=fnt(SANS_B, 22), fill=INK)
    d.text((70, 180), eyebrow.upper(), font=fnt(SANS_B, 22), fill=GOLD)
    d.text((70, 230), title, font=fnt(SERIF_B, 64), fill=CREAM)
    d.text((70, 330), price, font=fnt(SANS_B, 56), fill=GOLD)
    y = 430
    for line in lines:
        d.text((70, y), "✓  " + line, font=fnt(SANS, 30), fill=CREAM)
        y += 56
    d.text((70, 960), "jobreadycv.za", font=fnt(SANS, 26), fill=GOLD)
    return save(img, PRODUCTS, fname)


def main():
    slide_01_cover()
    slide_02_pain()
    slide_03_kit()
    plan_slide(
        "04-starter.png",
        "PLAN 01",
        "Starter",
        "R0",
        "Forever free. One proper CV.",
        [
            "1 CV, 3 premium SA templates",
            "SA English & local format",
            "Live ATS score on every draft",
            "PDF export, no watermark",
            "Basic cover-letter draft",
        ],
    )
    plan_slide(
        "05-pro.png",
        "PLAN 02",
        "Pro",
        "R99/mo",
        "Billed in rand. Most chosen.",
        [
            "Unlimited CVs & cover letters",
            "40+ industry templates",
            "Tailor to a PNet / Careers24 ad",
            "Full LinkedIn rewrite kit",
            "PDF + Word  ·  priority ATS",
        ],
        badge="MOST CHOSEN",
        accent=GOLD,
    )
    plan_slide(
        "06-career.png",
        "PLAN 03",
        "Career",
        "R199/mo",
        "The whole hunt, handled.",
        [
            "Everything in Pro",
            "Interview brief per application",
            "Keyword targeting per vacancy",
            "1 human review each month",
            "LinkedIn banner & featured set",
        ],
    )
    slide_07_compare()
    slide_08_proof()
    slide_09_how()
    slide_10_cta()

    product_tile(
        "p-starter.png",
        "Plan",
        "Starter CV",
        "R0",
        ["1 SA-format CV", "ATS score", "PDF, no watermark", "Basic cover letter"],
        "FREE",
    )
    product_tile(
        "p-pro.png",
        "Plan",
        "Pro Hunt",
        "R99/mo",
        ["Unlimited CVs + letters", "Ad tailoring", "LinkedIn rewrite", "PDF + Word"],
        "MOST CHOSEN",
    )
    product_tile(
        "p-career.png",
        "Plan",
        "Career",
        "R199/mo",
        ["Everything in Pro", "Interview brief", "Human review / mo", "LinkedIn banner"],
    )
    product_tile(
        "p-cv.png",
        "Service",
        "ATS CV",
        "from R0",
        ["2–3 page SA CV", "SuccessFactors-safe", "Proof, not duties", "City + title + number"],
    )
    product_tile(
        "p-letter.png",
        "Service",
        "Cover letter",
        "in Pro",
        ["Sounds like you", "Names the company", "No ChatGPT sludge", "One page, tight"],
    )
    product_tile(
        "p-linkedin.png",
        "Service",
        "LinkedIn kit",
        "in Pro",
        ["Role · proof · city", "About in 5 lines", "Experience bullets", "Searchable, not vibes"],
    )
    product_tile(
        "p-interview.png",
        "Service",
        "Interview brief",
        "in Career",
        ["Tell me about yourself", "Weakness, done right", "Why this desk", "From your actual CV"],
    )
    print("done")


if __name__ == "__main__":
    main()
