#!/usr/bin/env python3
"""Xưởng làm web (bản 2): đọc file thông tin một doanh nghiệp (JSON) -> xuất website hoàn chỉnh.

Dùng:
    python3 build.py                       # dựng tất cả file trong clients/
    python3 build.py clients/ten-tiem.json # dựng một khách

Kết quả nằm ở out/<slug>/index.html (kèm thư mục images/ nếu khách có ảnh thật).
Chỉ dùng thư viện có sẵn của Python, không cần cài thêm gì.

Ảnh thật: đặt ảnh vào clients/<slug>/images/ rồi khai báo trong JSON:
    "images": {"hero": "phong-kham.jpg", "gallery": ["a.jpg", "b.jpg", "c.jpg"]}
Có ảnh hero thì trang dùng ảnh thật thay cho hình minh họa.
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

# ---------------------------------------------------------------- loại hình
PRESETS = {
    "salon": {
        "steps_title": "Đơn giản từ lần đầu ghé tiệm.",
        "label": "Tiệm tóc & làm đẹp", "services_title": "Dịch vụ & bảng giá", "cta": "Đặt lịch",
        "when": "Ngày giờ muốn đến", "dark": True,
        "bg": "#0b0b10", "bg2": "#12121a", "card": "rgba(255,255,255,0.055)", "text": "#f5f1ea",
        "accent": "#d9a441", "accent2": "#f3c969", "ink": "#16110a",
        "icons": ["scissors", "sparkle", "comb", "scissors", "sparkle", "comb"],
        "steps": [("Đặt lịch", "Chọn giờ qua web, Zalo hoặc gọi điện."),
                  ("Tư vấn kiểu", "Trao đổi mong muốn trước khi bắt đầu."),
                  ("Thực hiện", "Làm đúng kiểu đã chốt."),
                  ("Hoàn thiện", "Xem lại, chỉnh nhẹ cho ưng ý.")],
    },
    "clinic": {
        "steps_title": "Đơn giản từ lần đầu đến khám.",
        "label": "Phòng khám & nha khoa", "services_title": "Dịch vụ", "cta": "Đặt lịch khám",
        "when": "Ngày giờ muốn khám", "dark": False,
        "bg": "#f6fbfb", "bg2": "#e9f5f5", "card": "#ffffff", "text": "#0b1f2a",
        "accent": "#0d9488", "accent2": "#38bdf8", "ink": "#ffffff",
        "icons": ["stethoscope", "sparkle", "tooth", "tooth", "crown", "braces", "implant"],
        "steps": [("Đặt lịch", "Chọn giờ qua web, Zalo hoặc gọi điện."),
                  ("Thăm khám", "Bác sĩ kiểm tra và trao đổi tình trạng."),
                  ("Tư vấn phương án", "Trình bày các lựa chọn và chi phí dự kiến."),
                  ("Điều trị", "Thực hiện theo phương án bạn đã đồng ý.")],
    },
    "edu": {
        "steps_title": "Rõ ràng từ buổi đầu tiên.",
        "label": "Trung tâm đào tạo", "services_title": "Khóa học & học phí", "cta": "Đăng ký tư vấn",
        "when": "Khóa học quan tâm", "dark": False,
        "bg": "#f8f7ff", "bg2": "#efedfd", "card": "#ffffff", "text": "#14132b",
        "accent": "#4f46e5", "accent2": "#a855f7", "ink": "#ffffff",
        "icons": ["book", "cap", "book", "cap"],
        "steps": [("Đăng ký tư vấn", "Để lại thông tin hoặc nhắn Zalo."),
                  ("Kiểm tra đầu vào", "Xác định trình độ hiện tại."),
                  ("Xếp lớp & lộ trình", "Chọn lớp và mục tiêu phù hợp."),
                  ("Bắt đầu học", "Theo lộ trình đã thống nhất.")],
    },
    "fnb": {
        "steps_title": "Dễ dàng từ lần đầu ghé quán.",
        "label": "Quán cà phê & nhà hàng", "services_title": "Menu nổi bật", "cta": "Đặt bàn",
        "when": "Ngày giờ & số người", "dark": False,
        "bg": "#fdf8f1", "bg2": "#f6ebdc", "card": "#ffffff", "text": "#2a1d12",
        "accent": "#b4541a", "accent2": "#f59e0b", "ink": "#ffffff",
        "icons": ["cup", "cup", "cup", "cup", "cup"],
        "steps": [("Chọn chỗ", "Đặt bàn qua web, Zalo hoặc gọi điện."),
                  ("Gọi món", "Xem menu và chọn món bạn thích."),
                  ("Thưởng thức", "Ngồi bao lâu cũng được."),
                  ("Quay lại", "Hẹn gặp bạn lần sau.")],
    },
}

# ---------------------------------------------------------------- biểu tượng (24x24, nét)
ICONS = {
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M8 3v4M16 3v4M3.5 10h17"/><path d="m9 15 2 2 4-4"/>',
    "pin": '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/>',
    "phone": '<path d="M5 4.5h3.2l1.6 4-2 1.3a11 11 0 0 0 6.4 6.4l1.3-2 4 1.6V19a1.8 1.8 0 0 1-2 1.8C10.6 20.3 3.7 13.4 3.2 6.5A1.8 1.8 0 0 1 5 4.5z"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "check": '<path d="m5 12.5 4.2 4.2L19 7"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "chat": '<path d="M4 5.5h16v10.5H10l-4.5 4v-4H4z"/>',
    "sparkle": '<path d="M11 3.5 12.9 9l5.6 1.9-5.6 1.9L11 18.5l-1.9-5.7L3.5 10.9 9.1 9z"/><path d="M19 3.5v3.5M17.2 5.2h3.6"/>',
    "tooth": '<path d="M8 3.5c-2.4 0-4 1.8-4 4.2 0 2 1 3.2 1.4 5.2.4 2.2.6 7.6 2.5 7.6 1.6 0 1.4-4 4.1-4s2.5 4 4.1 4c1.9 0 2.1-5.400 2.500-7.600.4-2 1.400-3.200 1.400-5.200 0-2.400-1.600-4.200-4-4.200-1.700 0-2.800.9-4 .9s-2.300-.9-4-.9z"/>',
    "crown": '<path d="m4 8 3.6 3.4L12 5l4.400 6.400L20 8l-1.400 9H5.400z"/><path d="M6.500 20.500h11"/>',
    "braces": '<rect x="3" y="7" width="5" height="10" rx="1.800"/><rect x="9.500" y="7" width="5" height="10" rx="1.800"/><rect x="16" y="7" width="5" height="10" rx="1.800"/><path d="M2 12h20"/>',
    "implant": '<path d="M7.500 3.500h9l-1 5h-7z"/><path d="M9 11h6M9.500 13.500h5M10 16h4M10.800 18.500h2.400M12 21v.5"/>',
    "stethoscope": '<path d="M6 3.500v5.500a4 4 0 0 0 8 0V3.500"/><path d="M10 13v2a4.500 4.500 0 0 0 9 0v-2.200"/><circle cx="19" cy="11" r="2"/>',
    "scissors": '<circle cx="6" cy="6.500" r="2.600"/><circle cx="6" cy="17.500" r="2.600"/><path d="M8 8.200 20 18M8 15.800 20 6"/>',
    "comb": '<rect x="3.500" y="7" width="17" height="6" rx="1.500"/><path d="M6 13v5M9 13v5M12 13v5M15 13v5M18 13v5"/>',
    "book": '<path d="M12 6.500C10 5 7 4.500 4 5v13c3-.5 6 0 8 1.500 2-1.500 5-2 8-1.500V5c-3-.5-6 0-8 1.500z"/><path d="M12 6.500v13"/>',
    "cap": '<path d="m2.500 9.500 9.500-4.500 9.500 4.500-9.500 4.500z"/><path d="M6.500 11.800V16c1.400 1.600 3.400 2.500 5.500 2.500s4.100-.9 5.500-2.500v-4.200"/><path d="M21.500 9.500V15"/>',
    "cup": '<path d="M5 9h11v5a5 5 0 0 1-5 5h-1a5 5 0 0 1-5-5z"/><path d="M16 10.500h1.500a2.500 2.500 0 0 1 0 5H16"/><path d="M8 3.500c-.8 1 .8 1.800 0 3M12 3.500c-.8 1 .8 1.800 0 3"/>',
    "shield": '<path d="M12 3.500 5 6v5.500c0 4.400 2.900 7.600 7 9 4.100-1.400 7-4.600 7-9V6z"/><path d="m9 12 2.200 2.200L15 10"/>',
}


def icon(name, size=24, cls="ic"):
    body = ICONS.get(name, ICONS["sparkle"])
    return (f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')


SPARK = '<path d="M0-9 2.200-2.200 9 0 2.200 2.200 0 9-2.200 2.200-9 0-2.200-2.200z"/>'

# ---------------------------------------------------------------- hình minh họa chính cho từng loại hình
ART = {
    "clinic": f'''<svg class="art" viewBox="0 0 240 270" aria-hidden="true"><defs>
<linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#d7f1f0"/></linearGradient>
<linearGradient id="g2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" style="stop-color:var(--accent2)"/><stop offset="1" style="stop-color:var(--accent)"/></linearGradient>
<filter id="bl"><feGaussianBlur stdDeviation="7"/></filter></defs>
<ellipse cx="120" cy="246" rx="58" ry="9" fill="#04323a" opacity=".22" filter="url(#bl)"/>
<path d="M120 40C98 22 58 25 46 60c-8 25 6 42 10 70 4 31 9 88 30 88 18 0 18-46 34-46s16 46 34 46c21 0 26-57 30-88 4-28 18-45 10-70-12-35-52-38-74-20z" fill="url(#g1)" stroke="#bfe6e2" stroke-width="3"/>
<path d="M76 54c-13 7-17 22-12 38" stroke="#fff" stroke-width="8" stroke-linecap="round" fill="none"/>
<path d="M84 150c2 20 3 44 8 52" stroke="#c9ebe8" stroke-width="4" stroke-linecap="round" fill="none" opacity=".8"/>
<g fill="#fff" opacity=".95"><g transform="translate(196 44) scale(1.1)">{SPARK}</g><g transform="translate(40 120) scale(.7)">{SPARK}</g><g transform="translate(206 140) scale(.6)">{SPARK}</g></g>
<g transform="translate(176 188)"><circle r="27" fill="url(#g2)"/><circle r="27" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="2"/><path d="m-11 1 7.500 7.500L12-8" stroke="#fff" stroke-width="5.500" stroke-linecap="round" stroke-linejoin="round" fill="none"/></g></svg>''',
    "salon": f'''<svg class="art" viewBox="0 0 240 270" aria-hidden="true"><defs>
<linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" style="stop-color:var(--accent2)"/><stop offset="1" style="stop-color:var(--accent)"/></linearGradient>
<linearGradient id="g2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#aab4c4"/></linearGradient>
<filter id="bl"><feGaussianBlur stdDeviation="7"/></filter></defs>
<ellipse cx="120" cy="248" rx="62" ry="8" fill="#000" opacity=".45" filter="url(#bl)"/>
<g fill="none" stroke="url(#g1)" stroke-width="11"><circle cx="76" cy="200" r="24"/><circle cx="164" cy="200" r="24"/></g>
<path d="M92 182 158 36" stroke="url(#g2)" stroke-width="15" stroke-linecap="round"/>
<path d="M148 182 82 36" stroke="url(#g2)" stroke-width="15" stroke-linecap="round" opacity=".96"/>
<path d="M96 168 154 40" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".7"/>
<circle cx="120" cy="124" r="10" fill="url(#g1)" stroke="#fff" stroke-width="3"/>
<g fill="#fff" opacity=".95"><g transform="translate(38 62) scale(.9)">{SPARK}</g><g transform="translate(206 74) scale(.7)">{SPARK}</g><g transform="translate(200 150) scale(.5)">{SPARK}</g></g></svg>''',
    "edu": f'''<svg class="art" viewBox="0 0 240 270" aria-hidden="true"><defs>
<linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" style="stop-color:var(--accent2)"/><stop offset="1" style="stop-color:var(--accent)"/></linearGradient>
<filter id="bl"><feGaussianBlur stdDeviation="7"/></filter></defs>
<ellipse cx="120" cy="240" rx="70" ry="9" fill="#1b1060" opacity=".25" filter="url(#bl)"/>
<path d="M120 112c-22-16-58-20-84-14v108c26-6 62-2 84 14 22-16 58-20 84-14V98c-26-6-62-2-84 14z" fill="#fff" stroke="#d8d4fb" stroke-width="3"/>
<path d="M120 112v108" stroke="#d8d4fb" stroke-width="3"/>
<g stroke="#c9c4f7" stroke-width="3" stroke-linecap="round" fill="none"><path d="M52 126c20-3 40 0 56 8M52 148c20-3 40 0 56 8M52 170c20-3 40 0 56 8M188 126c-20-3-40 0-56 8M188 148c-20-3-40 0-56 8M188 170c-20-3-40 0-56 8"/></g>
<path d="M120 28 40 66l80 38 80-38z" fill="url(#g1)"/><path d="M76 86v26c10 10 28 16 44 16s34-6 44-16V86l-44 20z" fill="url(#g1)" opacity=".85"/>
<path d="M200 66v44" stroke="url(#g1)" stroke-width="5" stroke-linecap="round"/><circle cx="200" cy="116" r="7" fill="url(#g1)"/>
<g fill="#fff" opacity=".95"><g transform="translate(34 40) scale(.8)">{SPARK}</g><g transform="translate(212 150) scale(.7)">{SPARK}</g></g></svg>''',
    "fnb": f'''<svg class="art" viewBox="0 0 240 270" aria-hidden="true"><defs>
<linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" style="stop-color:var(--accent2)"/><stop offset="1" style="stop-color:var(--accent)"/></linearGradient>
<filter id="bl"><feGaussianBlur stdDeviation="7"/></filter></defs>
<ellipse cx="120" cy="238" rx="78" ry="10" fill="#2a1306" opacity=".28" filter="url(#bl)"/>
<ellipse cx="120" cy="222" rx="84" ry="16" fill="#fff" stroke="#ead9c3" stroke-width="3"/>
<path d="M54 100h120v50c0 36-26 64-60 64s-60-28-60-64z" fill="#fff" stroke="#ead9c3" stroke-width="3"/>
<path d="M174 112h12c18 0 18 40 0 40h-12" fill="none" stroke="#ead9c3" stroke-width="10" stroke-linecap="round"/>
<path d="M62 108h104v14c-22 10-82 10-104 0z" fill="url(#g1)"/>
<path d="M70 96c-6-14 8-18 2-32M114 96c-6-14 8-18 2-32M158 96c-6-14 8-18 2-32" stroke="url(#g1)" stroke-width="7" stroke-linecap="round" fill="none" opacity=".75"/>
<g fill="#fff" opacity=".95"><g transform="translate(36 50) scale(.8)">{SPARK}</g><g transform="translate(206 70) scale(.7)">{SPARK}</g></g></svg>''',
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;scroll-padding-top:84px}
body{font-family:'Be Vietnam Pro','Inter',system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.65;-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit;text-decoration:none}
img{max-width:100%;display:block}
.wrap{width:min(1120px,100% - 40px);margin-inline:auto}
section{padding:96px 0;position:relative}
.alt{background:var(--bg2)}
h1{font-size:clamp(2.3rem,5.4vw,4.2rem);line-height:1.17;letter-spacing:-.04em;font-weight:800}
h2{font-size:clamp(1.7rem,3.8vw,2.7rem);line-height:1.22;letter-spacing:-.03em;font-weight:800}
h3{letter-spacing:-.01em}
.gt{background:linear-gradient(120deg,var(--accent),var(--accent2));-webkit-background-clip:text;background-clip:text;color:transparent;padding:.1em 0 .2em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:.78rem;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);font-weight:700;margin-bottom:14px}
.eyebrow::before{content:"";width:22px;height:2px;border-radius:2px;background:var(--accent)}
.dim{color:var(--dim)}
.head{max-width:620px;margin-bottom:48px}
.head p{margin-top:12px}
.ic{flex:none}
.btn{position:relative;overflow:hidden;display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:15px 28px;border-radius:999px;font-weight:700;font-size:.97rem;border:1.5px solid transparent;cursor:pointer;font-family:inherit;transition:transform .25s,box-shadow .25s,background .25s}
.btn:hover{transform:translateY(-3px)}
.btn-main{background:linear-gradient(120deg,var(--accent),var(--accent2));color:var(--ink);box-shadow:0 12px 32px var(--glow)}
.btn-main:hover{box-shadow:0 18px 40px var(--glow)}
.btn-main::after{content:"";position:absolute;top:0;left:-70%;width:45%;height:100%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.45),transparent);transform:skewX(-20deg);animation:shine 4.5s ease-in-out infinite}
@keyframes shine{0%,60%{left:-70%}100%{left:130%}}
.btn-line{border-color:var(--line);background:var(--card);color:var(--text);backdrop-filter:blur(8px)}
.btn-line:hover{border-color:var(--accent)}
.btn-sm{padding:10px 20px;font-size:.88rem;white-space:nowrap}
.btn:focus-visible,summary:focus-visible,a:focus-visible,input:focus-visible,textarea:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.ribbon{background:linear-gradient(120deg,var(--accent),var(--accent2));color:var(--ink);text-align:center;font-size:.8rem;font-weight:700;padding:9px 16px;line-height:1.45}
.top{position:sticky;top:0;z-index:40;background:var(--bar);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border-bottom:1px solid transparent;transition:border-color .3s,box-shadow .3s}
.top.scrolled{border-color:var(--line);box-shadow:0 8px 30px rgba(0,0,0,.06)}
.bar{display:flex;align-items:center;justify-content:space-between;gap:16px;height:68px}
.logo{display:flex;align-items:center;gap:10px;font-weight:800;letter-spacing:-.02em;font-size:1.06rem;min-width:0;white-space:nowrap}
.logo span{overflow:hidden;text-overflow:ellipsis}
.logo i{width:34px;height:34px;border-radius:11px;background:linear-gradient(135deg,var(--accent),var(--accent2));color:var(--ink);display:grid;place-items:center;font-style:normal;font-weight:800}
.links{display:flex;align-items:center;gap:28px;font-size:.92rem;color:var(--dim)}
.links a:hover{color:var(--text)}

/* hero */
.hero{padding:72px 0 96px;overflow:hidden}
.hero::before{content:"";position:absolute;inset:0;background:radial-gradient(60% 55% at 85% 20%,var(--glow),transparent 70%),radial-gradient(40% 40% at 5% 90%,var(--glow2),transparent 70%);pointer-events:none}
.hero::after{content:"";position:absolute;inset:0;background-image:radial-gradient(var(--line) 1.2px,transparent 1.2px);background-size:26px 26px;-webkit-mask-image:linear-gradient(180deg,#000,transparent 75%);mask-image:linear-gradient(180deg,#000,transparent 75%);pointer-events:none;opacity:.8}
.hgrid{position:relative;z-index:1;display:grid;grid-template-columns:1.08fr .92fr;gap:48px;align-items:center}
.pill{display:inline-flex;align-items:center;gap:8px;padding:8px 16px 8px 10px;border-radius:999px;background:var(--card);border:1px solid var(--line);font-size:.84rem;font-weight:600;color:var(--dim);backdrop-filter:blur(10px);margin-bottom:22px}
.pill b{width:24px;height:24px;border-radius:50%;background:linear-gradient(135deg,var(--accent),var(--accent2));color:var(--ink);display:grid;place-items:center}
.lead{font-size:clamp(1.02rem,1.9vw,1.2rem);max-width:540px;margin:22px 0 32px}
.cta-row{display:flex;gap:12px;flex-wrap:wrap}
.mini{display:flex;gap:22px;flex-wrap:wrap;margin-top:34px;font-size:.88rem;color:var(--dim)}
.mini span{display:inline-flex;align-items:center;gap:8px}
.mini .ic{color:var(--accent)}
.stage{position:relative;aspect-ratio:1/1;width:100%;max-width:520px;margin-inline:auto}
.blob{position:absolute;inset:7%;border-radius:44% 56% 52% 48%/50% 44% 56% 50%;background:linear-gradient(145deg,var(--accent),var(--accent2));box-shadow:0 40px 90px var(--glow);animation:morph 14s ease-in-out infinite alternate}
.blob::after{content:"";position:absolute;inset:0;border-radius:inherit;background:radial-gradient(60% 50% at 30% 20%,rgba(255,255,255,.45),transparent 70%)}
@keyframes morph{0%{border-radius:44% 56% 52% 48%/50% 44% 56% 50%;transform:rotate(0)}100%{border-radius:56% 44% 46% 54%/46% 56% 44% 54%;transform:rotate(8deg)}}
.ring{position:absolute;inset:0;border-radius:50%;border:1.5px dashed var(--line);animation:spin 60s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.art{position:absolute;left:50%;top:50%;width:64%;transform:translate(-50%,-50%);filter:drop-shadow(0 18px 24px rgba(0,0,0,.18));animation:bob 6s ease-in-out infinite}
@keyframes bob{0%,100%{transform:translate(-50%,-50%)}50%{transform:translate(-50%,-53%)}}
.photo{position:absolute;inset:4%;border-radius:36px;overflow:hidden;box-shadow:0 40px 90px var(--glow);border:6px solid var(--card)}
.photo img{width:100%;height:100%;object-fit:cover}
.fc{position:absolute;display:flex;align-items:center;gap:12px;padding:12px 16px 12px 12px;border-radius:18px;background:var(--glass);border:1px solid var(--line);box-shadow:0 18px 44px rgba(0,0,0,.14);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);animation:fl 7s ease-in-out infinite}
.fc b{display:block;font-size:.9rem;line-height:1.25}
.fc small{display:block;font-size:.76rem;color:var(--dim);line-height:1.3;margin-top:2px}
.fc .t{width:40px;height:40px;border-radius:12px;background:linear-gradient(135deg,var(--accent),var(--accent2));color:var(--ink);display:grid;place-items:center;flex:none}
.fc.a{top:6%;left:-4%}
.fc.b{bottom:9%;left:-2%;animation-delay:-2.5s}
.fc.c{top:23%;right:-6%;animation-delay:-4.5s}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}

/* feature + service cards */
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.card{background:var(--card);border:1px solid var(--line);border-radius:24px;padding:30px;box-shadow:0 1px 0 rgba(255,255,255,.04),0 18px 40px rgba(0,0,0,.04);transition:transform .3s,box-shadow .3s,border-color .3s}
.card:hover{transform:translateY(-6px);border-color:var(--accent);box-shadow:0 26px 54px var(--glow2)}
.tile{width:54px;height:54px;border-radius:16px;background:linear-gradient(135deg,var(--accent),var(--accent2));color:var(--ink);display:grid;place-items:center;margin-bottom:20px;box-shadow:0 12px 26px var(--glow)}
.card h3{font-size:1.12rem;margin-bottom:6px}
.card p{font-size:.94rem;color:var(--dim)}
.price{margin-top:14px;font-weight:800;color:var(--accent)}
.sgrid{display:flex;flex-wrap:wrap;justify-content:center;gap:20px}
.sgrid .card{flex:0 0 calc((100% - 60px)/4)}
.more{display:inline-flex;align-items:center;gap:6px;margin-top:16px;font-size:.88rem;font-weight:700;color:var(--accent)}
.more .ic{transition:transform .25s}
.card:hover .more .ic{transform:translateX(4px)}

/* steps */
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;position:relative;counter-reset:s}
.steps::before{content:"";position:absolute;left:8%;right:8%;top:27px;height:2px;background:repeating-linear-gradient(90deg,var(--accent) 0 8px,transparent 8px 16px);opacity:.45}
.step{position:relative;text-align:center;padding:0 8px}
.step i{position:relative;z-index:1;width:56px;height:56px;margin:0 auto 18px;border-radius:50%;background:linear-gradient(135deg,var(--accent),var(--accent2));color:var(--ink);display:grid;place-items:center;font-style:normal;font-weight:800;font-size:1.15rem;box-shadow:0 0 0 8px var(--bg2),0 12px 26px var(--glow)}
.step h3{font-size:1.04rem;margin-bottom:6px}
.step p{font-size:.9rem;color:var(--dim)}

/* about + info */
.two{display:grid;grid-template-columns:1.15fr 1fr;gap:32px;align-items:start}
.info{display:grid;gap:18px}
.info div.r{display:flex;gap:14px;align-items:flex-start}
.info .t{width:42px;height:42px;border-radius:13px;background:var(--bg2);color:var(--accent);display:grid;place-items:center;flex:none}
.info dt{font-size:.74rem;letter-spacing:.12em;text-transform:uppercase;color:var(--dim);font-weight:700}
.info dd{font-size:.97rem;font-weight:600}
.shots{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.shots img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:20px}
.shots img:first-child{grid-column:span 2;grid-row:span 2;aspect-ratio:auto;height:100%}

/* reviews / cta band */
.rev{display:flex;align-items:center;justify-content:space-between;gap:28px;flex-wrap:wrap;padding:38px 42px;border-radius:28px;background:var(--card);border:1px solid var(--line);box-shadow:0 22px 50px var(--glow2)}
.rev h2{font-size:clamp(1.4rem,3vw,2rem)}
.quote p{font-size:1rem;margin-bottom:14px}
.quote span{font-size:.88rem;color:var(--dim)}
.band{position:relative;overflow:hidden;border-radius:32px;padding:64px 40px;text-align:center;background:linear-gradient(130deg,var(--accent),var(--accent2));color:var(--ink)}
.band::before{content:"";position:absolute;width:460px;height:460px;border-radius:50%;background:rgba(255,255,255,.18);top:-200px;right:-120px}
.band::after{content:"";position:absolute;width:320px;height:320px;border-radius:50%;background:rgba(255,255,255,.12);bottom:-160px;left:-80px}
.band>*{position:relative;z-index:1}
.band p{opacity:.92;max-width:520px;margin:12px auto 28px}
.band .btn{background:#fff;color:#0b1f2a;box-shadow:0 14px 34px rgba(0,0,0,.18)}
.band .btn::after{display:none}
.faq{display:grid;gap:12px;max-width:780px}
details{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:2px 22px}
summary{cursor:pointer;padding:17px 0;font-weight:600;list-style:none;display:flex;justify-content:space-between;gap:16px}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";color:var(--accent);font-size:1.4rem;line-height:1}
details[open] summary::after{content:"\\2212"}
details p{color:var(--dim);padding:0 0 18px;font-size:.94rem}

/* contact */
form{display:grid;gap:14px}
label{font-size:.85rem;font-weight:600;display:grid;gap:6px}
input,textarea{font:inherit;color:var(--text);background:var(--bg);border:1px solid var(--line);border-radius:14px;padding:14px 15px;width:100%;transition:border-color .2s,box-shadow .2s}
input:focus,textarea:focus{border-color:var(--accent);box-shadow:0 0 0 4px var(--glow2);outline:none}
textarea{min-height:92px;resize:vertical}
.ok,.err{display:none;padding:14px 16px;border-radius:12px;font-size:.92rem}
.ok{background:rgba(16,185,129,.14);border:1px solid rgba(16,185,129,.4)}
.err{background:rgba(239,68,68,.12);border:1px solid rgba(239,68,68,.4)}
.mapbox{position:relative;height:270px;border-radius:22px;overflow:hidden;margin:0 0 14px;background:linear-gradient(135deg,var(--bg2),var(--card));border:1px solid var(--line);display:grid;place-items:center;text-align:center;padding:20px}
.mapbox .t{width:52px;height:52px;border-radius:16px;background:linear-gradient(135deg,var(--accent),var(--accent2));color:var(--ink);display:grid;place-items:center;margin:0 auto 10px;box-shadow:0 12px 26px var(--glow)}
.mapbox b{display:block;font-size:.95rem}
.mapbox small{color:var(--dim);font-size:.84rem}
.mapbox iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.acts{display:flex;gap:10px;flex-wrap:wrap}
footer{padding:36px 0 44px;border-top:1px solid var(--line);color:var(--dim);font-size:.86rem;text-align:center}
.dock{display:none}

/* motion */
.js .rv{opacity:0;transform:translateY(28px);transition:opacity .8s cubic-bezier(.2,.7,.2,1),transform .8s cubic-bezier(.2,.7,.2,1)}
.js .rv.in{opacity:1;transform:none}
.js .rv.d1{transition-delay:.08s}.js .rv.d2{transition-delay:.16s}.js .rv.d3{transition-delay:.24s}

@media (max-width:900px){
 section{padding:68px 0}
 .hgrid{grid-template-columns:1fr;gap:22px}
 .stage{order:-1;max-width:236px}
 .hero{padding:22px 0 56px}
 .links .btn{display:none}
 .sgrid .card{flex:0 0 calc((100% - 14px)/2);padding:20px}
 .sgrid{gap:14px}
 .sgrid .tile{width:46px;height:46px;margin-bottom:14px}
 .sgrid .card h3{font-size:1rem}
 .sgrid .card p{font-size:.86rem}
 .head{margin-bottom:34px}
 .grid3,.two,.steps{grid-template-columns:1fr}
 .steps::before{display:none}
 .step{display:grid;grid-template-columns:56px 1fr;gap:16px;text-align:left;padding:0}
 .step i{margin:0}
 .shots{grid-template-columns:1fr 1fr}
 .shots img:first-child{grid-column:span 2}
 .links a:not(.btn){display:none}
 .fc.c{display:none}
 .fc{padding:7px 12px 7px 7px;gap:9px}
 .fc .t{width:32px;height:32px;border-radius:10px}
 .fc small{display:none}
 .fc b{font-size:.8rem}
 .fc.a{left:-16%;top:6%}
 .fc.b{left:auto;right:-16%;bottom:6%}
 .cta-row .btn{width:100%}
 .rev{padding:28px 24px}
 .band{padding:48px 24px;border-radius:26px}
 body{padding-bottom:78px}
 .dock{display:grid;grid-template-columns:1fr 1fr;gap:10px;position:fixed;left:0;right:0;bottom:0;z-index:50;padding:10px 14px calc(10px + env(safe-area-inset-bottom));background:var(--bar);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-top:1px solid var(--line)}
 .dock .btn{padding:13px 10px}
}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}.blob,.ring,.art,.fc,.btn-main::after{animation:none}.js .rv{opacity:1;transform:none;transition:none}}
"""

JS = """
(function(){
  var top=document.querySelector('.top');
  function sc(){top.classList.toggle('scrolled',window.scrollY>8)}
  sc();addEventListener('scroll',sc,{passive:true});
  var els=document.querySelectorAll('.rv');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});
    els.forEach(function(el){io.observe(el)});
  }else{els.forEach(function(el){el.classList.add('in')})}
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
    if data.get("maps_url") and not str(data["maps_url"]).startswith("https://"):
        fail(f"{path}: 'maps_url' phải bắt đầu bằng https://")
    if data.get("facebook") and not str(data["facebook"]).startswith("https://"):
        fail(f"{path}: 'facebook' phải bắt đầu bằng https://")
    return data


def safe_image(name):
    base = Path(str(name)).name
    if not re.fullmatch(r"[\w.-]+\.(jpe?g|png|webp|avif)", base, re.I):
        fail(f"tên ảnh không hợp lệ: {name}")
    return base


def pick_icon(service, preset, i):
    if service.get("icon") in ICONS:
        return service["icon"]
    n = service["name"].lower()
    rules = [("trám", "shield"), ("khám", "stethoscope"), ("tư vấn", "stethoscope"), ("cao răng", "sparkle"), ("tẩy", "sparkle"),
             ("sứ", "crown"), ("niềng", "braces"), ("implant", "implant"), ("trồng", "implant"),
             ("cắt", "scissors"), ("uốn", "sparkle"), ("nhuộm", "sparkle"), ("ielts", "cap"), ("thi", "cap")]
    for key, name in rules:
        if key in n:
            return name
    icons = preset["icons"]
    return icons[i % len(icons)]


def rgba(hex_color, alpha):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def build_head(c, p):
    name, area = c["name"], c.get("area", "")
    category = c.get("category", p["label"])
    where = f"{area}, Hà Nội" if area else "Hà Nội"
    title = f"{name} — {category} tại {where}"
    desc = c.get("description") or c.get("about_short") or f"{name}: {category} tại {where}."
    ld = {
        "@context": "https://schema.org", "@type": "LocalBusiness", "name": name,
        "telephone": digits(c["phone"]),
        "address": {"@type": "PostalAddress", "streetAddress": c["address"],
                    "addressLocality": "Hà Nội", "addressCountry": "VN"},
    }
    ld_json = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")
    dark = p["dark"]
    accent = c.get("accent") or p["accent"]
    accent2 = c.get("accent2") or p["accent2"]
    for col in (accent, accent2):
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", col):
            fail(f"{c['slug']}: màu phải dạng #rrggbb")
    dim = "rgba(255,255,255,.68)" if dark else "rgba(11,31,42,.66)"
    line = "rgba(255,255,255,.1)" if dark else "rgba(11,31,42,.1)"
    bar = "rgba(11,11,16,.8)" if dark else "rgba(255,255,255,.82)"
    glass = "rgba(24,24,34,.78)" if dark else "rgba(255,255,255,.86)"
    root = (f":root{{--bg:{p['bg']};--bg2:{p['bg2']};--card:{p['card']};--text:{p['text']};--dim:{dim};--line:{line};"
            f"--bar:{bar};--glass:{glass};--accent:{accent};--accent2:{accent2};--ink:{p['ink']};"
            f"--glow:{rgba(accent, .34)};--glow2:{rgba(accent, .13)}}}")
    return f"""<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:type" content="website" />
<meta name="theme-color" content="{esc(p['bg'])}" />
<script>document.documentElement.className='js'</script>
<noscript><style>.rv{{opacity:1!important;transform:none!important}}</style></noscript>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<script type="application/ld+json">{ld_json}</script>
<style>{root}{CSS}</style>"""


def build_body(c, p):
    name = esc(c["name"])
    category = esc(c.get("category", p["label"]))
    cta = esc(c.get("cta", p["cta"]))
    has_zalo = c.get("zalo", True) is not False
    zalo = "https://zalo.me/" + digits(c.get("zalo") or c["phone"])
    tel = "tel:" + digits(c["phone"])
    addr = c["address"]
    street = addr.split(",")[0]
    area = c.get("area") or "Hà Nội"
    maps_dir = "https://www.google.com/maps/search/?api=1&query=" + quote(addr)
    maps_embed = "https://www.google.com/maps?q=" + quote(addr) + "&output=embed"
    images = c.get("images", {})
    hero_img = safe_image(images["hero"]) if images.get("hero") else None
    gallery = [safe_image(g) for g in images.get("gallery", [])]
    sample_tag = " (mẫu)" if c.get("ribbon") else ""
    svc_title = esc(c.get("services_title", p["services_title"]) + sample_tag)
    has_reviews = bool(c.get("maps_url") or c.get("testimonials"))

    out = []
    if c.get("ribbon"):
        out.append(f'<div class="ribbon">{esc(c["ribbon"])}</div>')

    nav = [f'<a href="#dich-vu">{esc(c.get("services_title", p["services_title"]).split(" &")[0])}</a>',
           '<a href="#quy-trinh">Quy trình</a>']
    if has_reviews:
        nav.append('<a href="#danh-gia">Đánh giá</a>')
    nav.append('<a href="#lien-he">Liên hệ</a>')
    out.append(
        f'<header class="top"><div class="wrap bar"><a class="logo" href="#top"><i>{esc(c["name"].strip()[:1].upper())}</i><span>{name}</span></a>'
        f'<nav class="links">{"".join(nav)}<a class="btn btn-main btn-sm" href="#lien-he">{cta}</a></nav></div></header>')

    # ---- hero
    tagline = c.get("tagline") or f"{c['name']} — {c.get('category', p['label'])}"
    accent_part = c.get("tagline_accent")
    if accent_part and accent_part in tagline:
        h1 = esc(tagline).replace(esc(accent_part), f'<span class="gt">{esc(accent_part)}</span>', 1)
    else:
        h1 = esc(tagline)
    lead = esc(c.get("about_short") or c.get("description") or "")
    mini = "".join(f'<span>{icon("check", 18)}{esc(h["title"])}</span>' for h in c.get("highlights", [])[:3])
    if hero_img:
        visual = f'<div class="photo"><img src="images/{esc(hero_img)}" alt="{name}" /></div>'
    else:
        visual = f'<div class="ring"></div><div class="blob"></div>{ART[c["type"]]}'
    out.append(
        f'<main id="top"><section class="hero"><div class="wrap hgrid"><div>'
        f'<span class="pill rv"><b>{icon("pin", 14)}</b>{category} · {esc(area)}</span>'
        f'<h1 class="rv d1">{h1}</h1>'
        + (f'<p class="lead dim rv d2">{lead}</p>' if lead else "")
        + f'<div class="cta-row rv d3"><a class="btn btn-main" href="#lien-he">{cta} {icon("arrow", 18)}</a>'
        f'<a class="btn btn-line" href="{esc(tel)}">{icon("phone", 18)}{esc(c["phone"])}</a></div>'
        + (f'<div class="mini rv d3">{mini}</div>' if mini else "")
        + f'</div><div class="stage rv d2">{visual}'
        f'<div class="fc a"><span class="t">{icon("calendar", 20)}</span><div><b>Gửi yêu cầu đặt lịch</b><small>Bên mình sẽ liên hệ lại</small></div></div>'
        f'<div class="fc b"><span class="t">{icon("pin", 20)}</span><div><b>{esc(area)}</b><small>{esc(street)}</small></div></div>'
        f'<div class="fc c"><span class="t">{icon("phone", 20)}</span><div><b>{esc(c["phone"])}</b><small>Gọi một chạm</small></div></div>'
        f'</div></div></section>')

    # ---- services
    cards = []
    for i, s in enumerate(c["services"]):
        cards.append(
            f'<a class="card rv d{i % 3 + 1}" href="#lien-he"><div class="tile">{icon(pick_icon(s, p, i), 26)}</div>'
            f'<h3>{esc(s["name"])}</h3>' + (f'<p>{esc(s["desc"])}</p>' if s.get("desc") else "")
            + (f'<div class="price">{esc(s["price"])}</div>' if s.get("price") else "")
            + f'<span class="more">{cta} {icon("arrow", 16)}</span></a>')
    out.append(
        f'<section id="dich-vu" class="alt"><div class="wrap"><div class="head rv"><div class="eyebrow">{category}</div>'
        f'<h2>{svc_title}</h2></div><div class="sgrid">{"".join(cards)}</div></div></section>')

    # ---- steps
    steps = c.get("steps")
    steps = [(s["title"], s["text"]) for s in steps] if steps else p["steps"]
    st = "".join(
        f'<div class="step rv d{i % 3 + 1}"><i>{i}</i><div><h3>{esc(t)}</h3><p>{esc(tx)}</p></div></div>'
        for i, (t, tx) in enumerate(steps, 1))
    out.append(
        f'<section id="quy-trinh" class="alt" style="padding-top:0"><div class="wrap"><div class="head rv"><div class="eyebrow">Quy trình</div>'
        f'<h2>{esc(p["steps_title"])}{sample_tag}</h2></div><div class="steps">{st}</div></div></section>')

    # ---- about + info
    hours = "".join(f"<dd>{esc(h)}</dd>" for h in c.get("hours", []))
    about = esc(c.get("about") or c.get("description") or "")
    rows = []
    if hours:
        rows.append(f'<div class="r"><span class="t">{icon("clock", 20)}</span><div><dt>Giờ mở cửa</dt>{hours}</div></div>')
    rows.append(f'<div class="r"><span class="t">{icon("pin", 20)}</span><div><dt>Địa chỉ</dt><dd>{esc(addr)}</dd></div></div>')
    rows.append(f'<div class="r"><span class="t">{icon("phone", 20)}</span><div><dt>Điện thoại</dt><dd><a href="{esc(tel)}">{esc(c["phone"])}</a></dd></div></div>')
    if c.get("facebook"):
        rows.append(f'<div class="r"><span class="t">{icon("chat", 20)}</span><div><dt>Facebook</dt><dd><a href="{esc(c["facebook"])}" rel="noopener" target="_blank">Xem fanpage</a></dd></div></div>')
    out.append(
        '<section id="gioi-thieu"><div class="wrap two"><div class="rv">'
        f'<div class="eyebrow">Giới thiệu</div><h2>{name}</h2>'
        + (f'<p class="dim" style="margin-top:14px">{about}</p>' if about else "")
        + f'</div><div class="card info rv d1">{"".join(rows)}</div></div></section>')

    if gallery:
        shots = "".join(f'<img src="images/{esc(g)}" alt="{name}" loading="lazy" />' for g in gallery)
        out.append(f'<section class="alt"><div class="wrap"><div class="head rv"><div class="eyebrow">Hình ảnh</div><h2>Không gian thực tế</h2></div><div class="shots rv">{shots}</div></div></section>')

    # ---- reviews
    if has_reviews:
        inner = ""
        if c.get("testimonials"):
            qs = "".join(f'<div class="card quote rv d{i}"><p>“{esc(t["text"])}”</p><span>— {esc(t["who"])}</span></div>'
                         for i, t in enumerate(c["testimonials"][:3], 1))
            inner += f'<div class="grid3" style="margin-bottom:24px">{qs}</div>'
        if c.get("maps_url"):
            inner += (f'<div class="rev rv"><div><div class="eyebrow">Đánh giá</div><h2>Khách hàng nói gì về {name}?</h2>'
                      f'<p class="dim" style="margin-top:8px">Xem các đánh giá trực tiếp trên Google Maps.</p></div>'
                      f'<a class="btn btn-main" href="{esc(c["maps_url"])}" target="_blank" rel="noopener">Xem đánh giá {icon("arrow", 18)}</a></div>')
        out.append(f'<section id="danh-gia"><div class="wrap">{inner}</div></section>')

    if c.get("faq"):
        qa = "".join(f'<details class="rv"><summary>{esc(i["q"])}</summary><p>{esc(i["a"])}</p></details>' for i in c["faq"])
        out.append(f'<section id="hoi-dap" class="alt"><div class="wrap"><div class="head rv"><div class="eyebrow">Hỏi đáp</div><h2>Câu hỏi thường gặp</h2></div><div class="faq">{qa}</div></div></section>')

    # ---- cta band
    out.append(
        f'<section style="padding:0 0 96px"><div class="wrap"><div class="band rv"><h2>{cta} ngay hôm nay</h2>'
        f'<p>Để lại thông tin hoặc gọi trực tiếp, bên mình sẽ liên hệ lại sớm nhất.</p>'
        f'<div class="cta-row" style="justify-content:center"><a class="btn" href="#lien-he">{cta} {icon("arrow", 18)}</a>'
        f'<a class="btn" href="{esc(tel)}">{icon("phone", 18)}{esc(c["phone"])}</a></div></div></div></section>')

    # ---- contact
    out.append(
        '<section id="lien-he" class="alt"><div class="wrap two"><div class="rv">'
        f'<div class="eyebrow">Liên hệ</div><h2>{cta}</h2>'
        '<p class="dim" style="margin:10px 0 24px">Để lại thông tin, bên mình liên hệ lại sớm nhất có thể.</p>'
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
        '</form></div><div class="rv d1">'
        f'<div class="mapbox"><div><div class="t">{icon("pin", 24)}</div><b>{esc(area)}</b><small>{esc(addr)}</small></div>'
        f'<iframe src="{esc(maps_embed)}" title="Bản đồ {name}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>'
        f'<div class="acts"><a class="btn btn-line" href="{esc(maps_dir)}" target="_blank" rel="noopener">{icon("pin", 18)}Chỉ đường</a>'
        + (f'<a class="btn btn-line" href="{esc(zalo)}" target="_blank" rel="noopener">{icon("chat", 18)}Nhắn Zalo</a>' if has_zalo else "")
        + '</div></div></div></section></main>')

    credit = f' · Website bởi {esc(MAKER_NAME)} · Zalo {esc(MAKER_ZALO)}' if c.get("credit") else ""
    if c.get("ribbon"):
        foot = f'Bản xem thử do {esc(MAKER_NAME)} dựng, chưa phải website chính thức của {name}, chưa được {name} xác nhận · Zalo {esc(MAKER_ZALO)}'
    else:
        foot = f'© {datetime.date.today().year} {name} · {esc(addr)}{credit}'
    out.append(
        f'<footer><div class="wrap">{foot}</div></footer>'
        f'<div class="dock"><a class="btn btn-line" href="{esc(tel)}">{icon("phone", 18)}Gọi ngay</a>'
        + (f'<a class="btn btn-main" href="{esc(zalo)}" target="_blank" rel="noopener">{icon("chat", 18)}Nhắn Zalo</a>' if has_zalo
           else f'<a class="btn btn-main" href="{esc(maps_dir)}" target="_blank" rel="noopener">{icon("pin", 18)}Chỉ đường</a>')
        + '</div>')
    return "".join(out)


def build_one(path):
    c = load_client(path)
    p = PRESETS[c["type"]]
    page = ('<!DOCTYPE html>\n<html lang="vi">\n<head>\n' + build_head(c, p) + "\n</head>\n<body>\n"
            + build_body(c, p) + f"\n<script>{JS}</script>\n</body>\n</html>\n")
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
