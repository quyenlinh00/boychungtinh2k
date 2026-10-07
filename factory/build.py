#!/usr/bin/env python3
"""Xưởng làm web: đọc file thông tin một doanh nghiệp (JSON) -> xuất website hoàn chỉnh.

Dùng:
    python3 build.py                       # dựng tất cả file trong clients/
    python3 build.py clients/ten-tiem.json # dựng một khách

Kết quả nằm ở out/<slug>/index.html (kèm thư mục images/ nếu khách có ảnh).
Chỉ dùng thư viện có sẵn của Python, không cần cài thêm gì.
"""
import datetime
import html
import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "out"

MAKER_NAME = "Quyền Linh"
MAKER_ZALO = "0936007937"

# Mỗi loại hình có bảng màu, tên mục và nút bấm riêng.
PRESETS = {
    "salon": {
        "label": "Tiệm tóc & làm đẹp",
        "services_title": "Dịch vụ & bảng giá",
        "cta": "Đặt lịch",
        "when": "Ngày giờ muốn đến",
        "dark": True,
        "bg": "#0b0b10", "card": "rgba(255,255,255,0.05)", "text": "#f5f1ea",
        "accent": "#d9a441", "ink": "#16110a",
    },
    "clinic": {
        "label": "Phòng khám & nha khoa",
        "services_title": "Dịch vụ & chi phí tham khảo",
        "cta": "Đặt lịch khám",
        "when": "Ngày giờ muốn khám",
        "dark": False,
        "bg": "#f7fafc", "card": "#ffffff", "text": "#0f172a",
        "accent": "#0d9488", "ink": "#ffffff",
    },
    "edu": {
        "label": "Trung tâm đào tạo",
        "services_title": "Khóa học & học phí",
        "cta": "Đăng ký tư vấn",
        "when": "Khóa học quan tâm",
        "dark": False,
        "bg": "#f8f7ff", "card": "#ffffff", "text": "#14132b",
        "accent": "#4f46e5", "ink": "#ffffff",
    },
    "fnb": {
        "label": "Quán cà phê & nhà hàng",
        "services_title": "Menu nổi bật",
        "cta": "Đặt bàn",
        "when": "Ngày giờ & số người",
        "dark": False,
        "bg": "#fbf6ee", "card": "#ffffff", "text": "#2a1d12",
        "accent": "#b4541a", "ink": "#ffffff",
    },
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Be Vietnam Pro','Inter',system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.65;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
img{max-width:100%;display:block}
.wrap{width:min(1080px,100% - 32px);margin-inline:auto}
section{padding:84px 0}
h1{font-size:clamp(2.2rem,6vw,4rem);line-height:1.1;letter-spacing:-.035em;font-weight:800}
h2{font-size:clamp(1.6rem,3.6vw,2.4rem);line-height:1.18;letter-spacing:-.03em;font-weight:800;margin-bottom:12px}
.eyebrow{font-size:.78rem;letter-spacing:.18em;text-transform:uppercase;color:var(--accent);font-weight:700;margin-bottom:12px}
.dim{color:var(--dim)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:14px 26px;border-radius:999px;font-weight:700;font-size:.98rem;border:1.5px solid transparent;cursor:pointer;font-family:inherit;transition:transform .2s,box-shadow .2s}
.btn:hover{transform:translateY(-2px)}
.btn-main{background:var(--accent);color:var(--ink);box-shadow:0 10px 30px var(--glow)}
.btn-line{border-color:var(--line);background:var(--card);color:var(--text)}
.btn-sm{padding:10px 20px;font-size:.88rem}
.btn:focus-visible,summary:focus-visible,a:focus-visible,input:focus-visible,textarea:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.ribbon{background:var(--accent);color:var(--ink);text-align:center;font-size:.8rem;font-weight:700;padding:8px 16px}
.top{position:sticky;top:0;z-index:40;background:var(--bar);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-bottom:1px solid var(--line)}
.bar{display:flex;align-items:center;justify-content:space-between;gap:16px;height:64px}
.logo{font-weight:800;letter-spacing:-.02em;font-size:1.05rem}
.links{display:flex;align-items:center;gap:26px;font-size:.92rem;color:var(--dim)}
.links a:hover{color:var(--text)}
.hero{padding:96px 0 84px;position:relative;overflow:hidden;background-size:cover;background-position:center}
.hero::before{content:"";position:absolute;width:520px;height:520px;border-radius:50%;background:var(--accent);filter:blur(130px);opacity:.2;top:-180px;right:-120px}
.hero .wrap{position:relative}
.hero.photo{padding:150px 0 120px;color:#fff}
.hero.photo::before{display:none}
.hero.photo .dim{color:rgba(255,255,255,.82)}
.hero p.lead{font-size:clamp(1rem,2vw,1.2rem);max-width:600px;margin:20px 0 32px}
.cta-row{display:flex;gap:12px;flex-wrap:wrap}
.chips{display:flex;gap:10px;flex-wrap:wrap;margin-top:36px}
.chip{padding:9px 16px;border-radius:999px;background:var(--card);border:1px solid var(--line);font-size:.86rem}
.hero.photo .chip{background:rgba(255,255,255,.14);border-color:rgba(255,255,255,.25);color:#fff}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:28px}
.card .n{width:38px;height:38px;border-radius:11px;background:var(--accent);color:var(--ink);display:grid;place-items:center;font-weight:800;margin-bottom:16px}
.card h3{font-size:1.08rem;margin-bottom:6px}
.svc{margin-top:30px;border-top:1px solid var(--line)}
.row{display:flex;justify-content:space-between;gap:20px;padding:20px 4px;border-bottom:1px solid var(--line)}
.row h3{font-size:1.04rem}
.row p{font-size:.92rem;color:var(--dim);margin-top:2px}
.price{font-weight:800;color:var(--accent);white-space:nowrap}
.two{display:grid;grid-template-columns:1.3fr 1fr;gap:28px;align-items:start}
.info h3{font-size:1rem;margin-bottom:10px}
.info dl{display:grid;gap:14px;font-size:.95rem}
.info dt{font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:var(--dim);font-weight:600}
.shots{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.shots img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:16px}
.quote p{font-size:1rem;margin-bottom:14px}
.quote span{font-size:.88rem;color:var(--dim)}
.faq{display:grid;gap:12px;max-width:780px;margin-top:28px}
details{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:2px 20px}
summary{cursor:pointer;padding:16px 0;font-weight:600;list-style:none;display:flex;justify-content:space-between;gap:16px}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";color:var(--accent);font-size:1.4rem;line-height:1}
details[open] summary::after{content:"\\2212"}
details p{color:var(--dim);padding:0 0 18px;font-size:.94rem}
form{display:grid;gap:14px}
label{font-size:.85rem;font-weight:600;display:grid;gap:6px}
input,textarea{font:inherit;color:var(--text);background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:13px 14px;width:100%}
textarea{min-height:92px;resize:vertical}
.note{font-size:.84rem;color:var(--dim)}
.ok,.err{display:none;padding:14px 16px;border-radius:12px;font-size:.92rem}
.ok{background:rgba(16,185,129,.14);border:1px solid rgba(16,185,129,.4)}
.err{background:rgba(239,68,68,.12);border:1px solid rgba(239,68,68,.4)}
iframe{width:100%;height:280px;border:0;border-radius:16px;margin-bottom:14px}
footer{padding:34px 0 40px;border-top:1px solid var(--line);color:var(--dim);font-size:.86rem;text-align:center}
.dock{display:none}
@media (max-width:760px){
 section{padding:62px 0}
 body{padding-bottom:76px}
 .links a:not(.btn){display:none}
 .grid3,.two,.shots{grid-template-columns:1fr}
 .hero{padding:64px 0 56px}
 .hero.photo{padding:96px 0 72px}
 .cta-row .btn{width:100%}
 .row{flex-direction:column;gap:6px}
 .dock{display:grid;grid-template-columns:1fr 1fr;gap:10px;position:fixed;left:0;right:0;bottom:0;z-index:50;padding:10px 14px calc(10px + env(safe-area-inset-bottom));background:var(--bar);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-top:1px solid var(--line)}
 .dock .btn{padding:13px 10px}
}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}.btn{transition:none}}
"""

JS = """
(function(){
  var f=document.getElementById('dat-lich-form');
  if(!f) return;
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var ok=document.getElementById('f-ok'),er=document.getElementById('f-err');
    ok.style.display='none';er.style.display='none';
    var btn=f.querySelector('button[type=submit]');btn.disabled=true;
    var body=new URLSearchParams(new FormData(f)).toString();
    fetch(f.getAttribute('action')||'/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:body})
      .then(function(r){if(!r.ok)throw new Error('bad');f.reset();ok.style.display='block';})
      .catch(function(){er.style.display='block';})
      .then(function(){btn.disabled=false;});
  });
})();
"""


def esc(value):
    return html.escape(str(value), quote=True)


def digits(value):
    return re.sub(r"\D", "", str(value))


def fail(msg):
    sys.exit("LỖI: " + msg)


def load_client(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"không đọc được {path}: {exc}")
    for key in ("slug", "type", "name", "address", "phone"):
        if not data.get(key):
            fail(f"{path}: thiếu mục '{key}'")
    if data["type"] not in PRESETS:
        fail(f"{path}: loại hình '{data['type']}' không có. Chọn một trong: {', '.join(PRESETS)}")
    if not re.fullmatch(r"[a-z0-9-]+", data["slug"]):
        fail(f"{path}: 'slug' chỉ gồm chữ thường không dấu, số và dấu gạch ngang")
    if not data.get("services"):
        fail(f"{path}: cần ít nhất 1 dịch vụ trong 'services'")
    return data


def safe_image(name):
    base = Path(str(name)).name
    if not re.fullmatch(r"[\w.-]+\.(jpe?g|png|webp|avif)", base, re.I):
        fail(f"tên ảnh không hợp lệ: {name}")
    return base


def build_head(c, p):
    name, area = c["name"], c.get("area", "")
    category = c.get("category", p["label"])
    where = f"{area}, Hà Nội" if area else "Hà Nội"
    title = f"{name} — {category} tại {where}"
    desc = c.get("description") or c.get("tagline") or f"{name}: {category} tại {where}."
    ld = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": name,
        "telephone": digits(c["phone"]),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": c["address"],
            "addressLocality": "Hà Nội",
            "addressCountry": "VN",
        },
    }
    ld_json = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")
    dim = "rgba(255,255,255,.68)" if p["dark"] else "rgba(15,23,42,.68)"
    line = "rgba(255,255,255,.1)" if p["dark"] else "rgba(15,23,42,.1)"
    bar = "rgba(11,11,16,.78)" if p["dark"] else "rgba(255,255,255,.82)"
    accent = c.get("accent") or p["accent"]
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", accent):
        fail(f"{c['slug']}: màu 'accent' phải dạng #rrggbb")
    root = (
        f":root{{--bg:{p['bg']};--card:{p['card']};--text:{p['text']};--dim:{dim};--line:{line};"
        f"--bar:{bar};--accent:{accent};--ink:{p['ink']};--glow:{accent}55}}"
    )
    return f"""<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:type" content="website" />
<meta name="theme-color" content="{esc(p['bg'])}" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<script type="application/ld+json">{ld_json}</script>
<style>{root}{CSS}</style>"""


def build_body(c, p):
    name = esc(c["name"])
    category = esc(c.get("category", p["label"]))
    cta = esc(c.get("cta", p["cta"]))
    zalo = "https://zalo.me/" + digits(c.get("zalo") or c["phone"])
    tel = "tel:" + digits(c["phone"])
    addr = c["address"]
    maps_dir = "https://www.google.com/maps/search/?api=1&query=" + quote(addr)
    maps_embed = "https://www.google.com/maps?q=" + quote(addr) + "&output=embed"
    images = c.get("images", {})
    hero_img = safe_image(images["hero"]) if images.get("hero") else None
    gallery = [safe_image(g) for g in images.get("gallery", [])]

    parts = []
    if c.get("ribbon"):
        parts.append(f'<div class="ribbon">{esc(c["ribbon"])}</div>')

    nav = ['<a href="#dich-vu">' + esc(c.get("services_title", p["services_title"]).split(" &")[0]) + "</a>", '<a href="#gioi-thieu">Giới thiệu</a>']
    if c.get("faq"):
        nav.append('<a href="#hoi-dap">Hỏi đáp</a>')
    nav.append('<a href="#lien-he">Liên hệ</a>')
    parts.append(
        f'<header class="top"><div class="wrap bar"><a class="logo" href="#top">{name}</a>'
        f'<nav class="links">{"".join(nav)}<a class="btn btn-main btn-sm" href="#lien-he">{cta}</a></nav></div></header>'
    )

    tagline = esc(c.get("tagline") or f"{c['name']} — {c.get('category', p['label'])}")
    lead = esc(c.get("about_short") or c.get("description") or "")
    hero_style = ""
    hero_cls = "hero"
    if hero_img:
        hero_cls = "hero photo"
        hero_style = (
            f' style="background-image:linear-gradient(180deg,rgba(0,0,0,.55),rgba(0,0,0,.72)),url(images/{esc(hero_img)})"'
        )
    chips = []
    if c.get("hours"):
        chips.append(f'<span class="chip">🕒 {esc(c["hours"][0])}</span>')
    chips.append(f'<span class="chip">📍 {esc(c.get("area") or "Hà Nội")}</span>')
    parts.append(
        f'<main id="top"><section class="{hero_cls}"{hero_style}><div class="wrap">'
        f'<div class="eyebrow">{category}</div><h1>{tagline}</h1>'
        + (f'<p class="lead dim">{lead}</p>' if lead else "")
        + f'<div class="cta-row"><a class="btn btn-main" href="#lien-he">{cta}</a>'
        f'<a class="btn btn-line" href="{esc(tel)}">Gọi {esc(c["phone"])}</a></div>'
        f'<div class="chips">{"".join(chips)}</div></div></section>'
    )

    if c.get("highlights"):
        cards = "".join(
            f'<div class="card"><div class="n">{i}</div><h3>{esc(h["title"])}</h3><p class="dim">{esc(h["text"])}</p></div>'
            for i, h in enumerate(c["highlights"][:3], 1)
        )
        parts.append(f'<section style="padding-top:20px"><div class="wrap"><div class="grid3">{cards}</div></div></section>')

    rows = "".join(
        f'<div class="row"><div><h3>{esc(s["name"])}</h3>'
        + (f'<p>{esc(s["desc"])}</p>' if s.get("desc") else "")
        + "</div>"
        + (f'<div class="price">{esc(s["price"])}</div>' if s.get("price") else "")
        + "</div>"
        for s in c["services"]
    )
    parts.append(
        f'<section id="dich-vu"><div class="wrap"><div class="eyebrow">{category}</div>'
        f'<h2>{esc(c.get("services_title", p["services_title"]))}</h2><div class="svc">{rows}</div></div></section>'
    )

    hours = "".join(f"<dd>{esc(h)}</dd>" for h in c.get("hours", []))
    about = esc(c.get("about") or c.get("description") or "")
    parts.append(
        '<section id="gioi-thieu"><div class="wrap two"><div>'
        f'<div class="eyebrow">Giới thiệu</div><h2>{name}</h2>'
        + (f'<p class="dim">{about}</p>' if about else "")
        + '</div><div class="card info"><dl>'
        + (f"<div><dt>Giờ mở cửa</dt>{hours}</div>" if hours else "")
        + f'<div><dt>Địa chỉ</dt><dd>{esc(addr)}</dd></div>'
        f'<div><dt>Điện thoại</dt><dd><a href="{esc(tel)}">{esc(c["phone"])}</a></dd></div>'
        + (f'<div><dt>Facebook</dt><dd><a href="{esc(c["facebook"])}" rel="noopener" target="_blank">Xem fanpage</a></dd></div>' if c.get("facebook") else "")
        + "</dl></div></div></section>"
    )

    if gallery:
        shots = "".join(f'<img src="images/{esc(g)}" alt="{name}" loading="lazy" />' for g in gallery)
        parts.append(f'<section><div class="wrap"><div class="eyebrow">Hình ảnh</div><h2>Không gian & công việc thực tế</h2><div class="shots" style="margin-top:26px">{shots}</div></div></section>')

    if c.get("testimonials"):
        qs = "".join(
            f'<div class="card quote"><p>“{esc(t["text"])}”</p><span>— {esc(t["who"])}</span></div>'
            for t in c["testimonials"][:3]
        )
        parts.append(f'<section><div class="wrap"><div class="eyebrow">Khách nói gì</div><h2>Phản hồi từ khách hàng</h2><div class="grid3" style="margin-top:26px">{qs}</div></div></section>')

    if c.get("faq"):
        qa = "".join(f'<details><summary>{esc(i["q"])}</summary><p>{esc(i["a"])}</p></details>' for i in c["faq"])
        parts.append(f'<section id="hoi-dap"><div class="wrap"><div class="eyebrow">Hỏi đáp</div><h2>Câu hỏi thường gặp</h2><div class="faq">{qa}</div></div></section>')

    parts.append(
        '<section id="lien-he"><div class="wrap two"><div>'
        f'<div class="eyebrow">Liên hệ</div><h2>{cta}</h2>'
        '<p class="dim" style="margin-bottom:22px">Để lại thông tin, bên mình liên hệ lại sớm nhất có thể.</p>'
        '<form id="dat-lich-form" name="dat-lich" method="POST" action="/" data-netlify="true" netlify-honeypot="bot-field">'
        '<input type="hidden" name="form-name" value="dat-lich" />'
        '<p hidden><label>Đừng điền ô này <input name="bot-field" /></label></p>'
        '<label>Họ tên<input name="ho_ten" required autocomplete="name" /></label>'
        '<label>Số điện thoại<input name="so_dien_thoai" type="tel" required autocomplete="tel" inputmode="tel" /></label>'
        f'<label>{esc(p["when"])}<input name="thoi_gian" /></label>'
        '<label>Ghi chú (nếu có)<textarea name="ghi_chu"></textarea></label>'
        f'<button class="btn btn-main" type="submit">Gửi {cta.lower()}</button>'
        '<div class="ok" id="f-ok" role="status">Đã nhận thông tin. Bên mình sẽ liên hệ lại sớm.</div>'
        f'<div class="err" id="f-err" role="alert">Chưa gửi được. Bạn gọi {esc(c["phone"])} hoặc nhắn Zalo giúp mình nhé.</div>'
        "</form></div><div>"
        f'<iframe src="{esc(maps_embed)}" title="Bản đồ {name}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
        f'<a class="btn btn-line" href="{esc(maps_dir)}" target="_blank" rel="noopener">Chỉ đường</a> '
        f'<a class="btn btn-line" href="{esc(zalo)}" target="_blank" rel="noopener">Nhắn Zalo</a>'
        "</div></div></section></main>"
    )

    credit = ""
    if c.get("credit"):
        credit = f' · Website bởi {esc(MAKER_NAME)} · Zalo {esc(MAKER_ZALO)}'
    parts.append(
        f'<footer><div class="wrap">© {datetime.date.today().year} {name} · {esc(addr)}{credit}</div></footer>'
        f'<div class="dock"><a class="btn btn-line" href="{esc(tel)}">Gọi ngay</a>'
        f'<a class="btn btn-main" href="{esc(zalo)}" target="_blank" rel="noopener">Nhắn Zalo</a></div>'
    )
    return "".join(parts)


def build_one(path):
    c = load_client(path)
    p = PRESETS[c["type"]]
    page = (
        '<!DOCTYPE html>\n<html lang="vi">\n<head>\n'
        + build_head(c, p)
        + "\n</head>\n<body>\n"
        + build_body(c, p)
        + f"\n<script>{JS}</script>\n</body>\n</html>\n"
    )
    dest = OUT / c["slug"]
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "index.html").write_text(page, encoding="utf-8")

    src_images = Path(path).resolve().parent / c["slug"] / "images"
    wanted = []
    if c.get("images", {}).get("hero"):
        wanted.append(safe_image(c["images"]["hero"]))
    wanted += [safe_image(g) for g in c.get("images", {}).get("gallery", [])]
    if wanted:
        (dest / "images").mkdir(exist_ok=True)
        for fname in wanted:
            src = src_images / fname
            if not src.is_file():
                fail(f"{c['slug']}: không thấy ảnh {src}")
            shutil.copy2(src, dest / "images" / fname)
    print(f"OK  {c['slug']:<22} -> {dest / 'index.html'}")


def main():
    targets = sys.argv[1:] or sorted(str(p) for p in (ROOT / "clients").glob("*.json"))
    if not targets:
        fail("chưa có file khách nào trong clients/")
    for t in targets:
        build_one(t)


if __name__ == "__main__":
    main()
