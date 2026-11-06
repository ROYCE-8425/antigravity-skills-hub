import math
import os
import subprocess
import time
import wave
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================
W, H = 1920, 1080
FPS = 60
DURATION = 12.0
TOTAL_FRAMES = int(DURATION * FPS)  # 720 frames

WORKSPACE_DIR = r"c:\Users\199X\OneDrive\Máy tính\video_seo"
ARTIFACT_DIR = r"C:\Users\199X\.gemini\antigravity\brain\429274a0-b221-437b-aa2a-f6e6aa99619f"
OUT_MP4 = os.path.join(WORKSPACE_DIR, "antigravity_2_launch_film_60fps.mp4")
OUT_WAV = os.path.join(ARTIFACT_DIR, "scratch", "soundtrack.wav")
FFMPEG_BIN = r"C:\Users\199X\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe"

os.makedirs(os.path.join(ARTIFACT_DIR, "scratch"), exist_ok=True)
os.makedirs(os.path.join(ARTIFACT_DIR, "reconstructed"), exist_ok=True)

FONT_DIR = r"C:\Windows\Fonts"
SERIF_PATH = os.path.join(FONT_DIR, "times.ttf")
SANS_PATH = os.path.join(FONT_DIR, "arial.ttf")
SANS_BOLD_PATH = os.path.join(FONT_DIR, "arialbd.ttf")

_FONT_CACHE = {}
def get_font(path, size):
    size = max(8, int(round(size)))
    key = (path, size)
    if key not in _FONT_CACHE:
        try:
            _FONT_CACHE[key] = ImageFont.truetype(path, size)
        except Exception:
            _FONT_CACHE[key] = ImageFont.load_default()
    return _FONT_CACHE[key]

# ==============================================================================
# EASING & MATH UTILITIES
# ==============================================================================
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))

def prog(t, t0, t1):
    if t1 <= t0:
        return 1.0 if t >= t1 else 0.0
    return clamp((t - t0) / (t1 - t0), 0.0, 1.0)

def ease_out_cubic(x):
    x = clamp(x)
    return 1.0 - (1.0 - x) ** 3

def ease_out_expo(x):
    x = clamp(x)
    return 1.0 if x == 1.0 else 1.0 - math.pow(2.0, -10.0 * x)

def ease_in_out_cubic(x):
    x = clamp(x)
    return 4 * x * x * x if x < 0.5 else 1 - math.pow(-2 * x + 2, 3) / 2

def ease_in_cubic(x):
    x = clamp(x)
    return x * x * x

def cubic_bezier(u, p0, p1, p2, p3):
    om = 1.0 - u
    b0 = om ** 3
    b1 = 3.0 * (om ** 2) * u
    b2 = 3.0 * om * (u ** 2)
    b3 = u ** 3
    x = b0 * p0[0] + b1 * p1[0] + b2 * p2[0] + b3 * p3[0]
    y = b0 * p0[1] + b1 * p1[1] + b2 * p2[1] + b3 * p3[1]
    return (x, y)

# ==============================================================================
# PRE-COMPUTED BACKGROUNDS & LOGO SPRITE
# ==============================================================================
def build_backgrounds():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx = xx / W
    ny = yy / H

    r = np.full((H, W), 4.0, dtype=np.float32)
    g = np.full((H, W), 8.0, dtype=np.float32)
    b = np.full((H, W), 20.0, dtype=np.float32)

    d1_sq = ((nx - 0.44) * 1.15) ** 2 + ((ny - 0.94) * 1.05) ** 2
    g1 = np.exp(-d1_sq * 3.2)
    g1_core = np.exp(-d1_sq * 7.5)

    d2_sq = ((nx - 0.78) * 1.3) ** 2 + ((ny - 0.92) * 1.1) ** 2
    g2 = np.exp(-d2_sq * 4.5)

    bg_std = np.zeros((H, W, 3), dtype=np.float32)
    bg_std[:, :, 0] = r + g1 * 18.0 + g1_core * 35.0 + g2 * 105.0
    bg_std[:, :, 1] = g + g1 * 145.0 + g1_core * 115.0 + g2 * 35.0
    bg_std[:, :, 2] = b + g1 * 225.0 + g1_core * 40.0 + g2 * 185.0
    bg_std_pil = Image.fromarray(np.clip(bg_std, 0, 255).astype(np.uint8))

    d3_sq = ((nx - 0.50) * 1.1) ** 2 + ((ny - 0.16) * 1.5) ** 2
    g3 = np.exp(-d3_sq * 4.2)
    bg_fin = bg_std.copy()
    bg_fin[:, :, 0] += g3 * 78.0
    bg_fin[:, :, 1] += g3 * 22.0
    bg_fin[:, :, 2] += g3 * 125.0
    bg_fin_pil = Image.fromarray(np.clip(bg_fin, 0, 255).astype(np.uint8))

    d0_sq = ((nx - 0.45) * 1.2) ** 2 + ((ny - 0.85) * 1.2) ** 2
    g0 = np.exp(-d0_sq * 4.5)
    bg_intro = np.zeros((H, W, 3), dtype=np.float32)
    bg_intro[:, :, 0] = 2.0 + g0 * 10.0
    bg_intro[:, :, 1] = 5.0 + g0 * 52.0
    bg_intro[:, :, 2] = 14.0 + g0 * 95.0
    bg_intro_pil = Image.fromarray(np.clip(bg_intro, 0, 255).astype(np.uint8))

    return bg_intro_pil, bg_std_pil, bg_fin_pil

def create_antigravity_logo(size=240):
    S = size * 2
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    u = (xx / S) * 2.0 - 1.0
    v = (yy / S) * 2.0 - 1.0

    y_outer = -0.68 + 1.95 * (u ** 2)
    y_inner = 0.02 + 1.15 * (u ** 2)

    in_arch = (v >= y_outer) & (v <= y_inner) & (v <= 0.65)
    tip_l = ((u + 0.58) ** 2 + (v - 0.42) ** 2) <= (0.095 ** 2)
    tip_r = ((u - 0.58) ** 2 + (v - 0.42) ** 2) <= (0.095 ** 2)
    ribbon_mask = (in_arch & (np.abs(u) <= 0.66) & (v <= 0.46)) | tip_l | tip_r

    t_vert = np.clip((v - (-0.68)) / (0.48 - (-0.68)), 0.0, 1.0)
    t_side = np.clip((u + 0.55) / 1.10, 0.0, 1.0)

    leg_r = (1.0 - t_side) * 45.0 + t_side * 35.0
    leg_g = (1.0 - t_side) * 235.0 + t_side * 205.0
    leg_b = (1.0 - t_side) * 140.0 + t_side * 255.0

    col_r = (1.0 - t_vert) * 255.0 + t_vert * leg_r
    col_g = (1.0 - t_vert) * 190.0 + t_vert * leg_g
    col_b = (1.0 - t_vert) * 20.0 + t_vert * leg_b

    rgba = np.zeros((S, S, 4), dtype=np.uint8)
    rgba[:, :, 0] = np.clip(col_r, 0, 255).astype(np.uint8)
    rgba[:, :, 1] = np.clip(col_g, 0, 255).astype(np.uint8)
    rgba[:, :, 2] = np.clip(col_b, 0, 255).astype(np.uint8)
    rgba[:, :, 3] = np.where(ribbon_mask, 255, 0).astype(np.uint8)

    dot_dist = np.sqrt(u ** 2 + (v - 0.20) ** 2)
    dot_mask = dot_dist <= 0.095
    rgba[dot_mask, 0] = 240
    rgba[dot_mask, 1] = 252
    rgba[dot_mask, 2] = 255
    rgba[dot_mask, 3] = 255

    img_hi = Image.fromarray(rgba)
    alpha = img_hi.split()[3]
    edge = alpha.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.GaussianBlur(1.5))
    white_edge = Image.new("RGBA", (S, S), (220, 255, 255, 190))
    img_hi.paste(white_edge, (0, 0), edge)

    glow = img_hi.filter(ImageFilter.GaussianBlur(14))
    out = Image.alpha_composite(glow, img_hi)
    return out.resize((size, size), Image.Resampling.LANCZOS)

LOGO_MASTER = create_antigravity_logo(240)
_LOGO_CACHE = {}
def get_logo(px_size):
    px_size = max(12, int(round(px_size)))
    if px_size not in _LOGO_CACHE:
        _LOGO_CACHE[px_size] = LOGO_MASTER.resize((px_size, px_size), Image.Resampling.LANCZOS)
    return _LOGO_CACHE[px_size]

# ==============================================================================
# SECRET #1: PRE-LOCKED BOUNDING BOXES FOR COMET TARGETS
# ==============================================================================
CHAT_W, CHAT_H = 1140, 226
CHAT_X = (W - CHAT_W) // 2  # 390
CHAT_Y = 415

PROMPT_WORDS = ["Why", "is", "Antigravity", "2.0", "actually", "so", "good?"]
COMET_COLORS = [
    (255, 220, 65),   # 1. Why - Solar Gold
    (60, 155, 255),   # 2. is - Electric Blue
    (0, 240, 255),    # 3. Antigravity - Quantum Cyan
    (35, 235, 150),   # 4. 2.0 - Aurora Emerald
    (50, 255, 165),   # 5. actually - Neon Mint
    (255, 125, 165),  # 6. so - Coral Pink
    (185, 95, 255),   # 7. good? - Electric Violet
]

def precompute_word_locks():
    dummy = Image.new("RGB", (100, 100))
    d = ImageDraw.Draw(dummy)
    f_prompt = get_font(SANS_PATH, 31)
    space_w = d.textlength(" ", font=f_prompt)

    cur_x = float(CHAT_X + 44)
    base_y = float(CHAT_Y + 46)
    locks = []

    title_x0 = 670.0
    title_y0 = 490.0

    arc_offsets = [
        ((-280, -140), (-190, -25)),
        ((-140, -195), (-90, -110)),
        ((40, -260), (-40, -150)),
        ((240, -310), (140, -190)),
        ((310, -275), (95, -135)),
        ((420, -195), (290, -85)),
        ((520, -150), (360, -25)),
    ]

    for idx, word in enumerate(PROMPT_WORDS):
        w_px = d.textlength(word, font=f_prompt)
        h_px = 36.0
        cx = cur_x + w_px * 0.5
        cy = base_y + h_px * 0.5

        sx = title_x0 + idx * 82.0
        sy = title_y0
        c1_off, c2_off = arc_offsets[idx]
        p0 = (sx, sy)
        p1 = (sx + c1_off[0], sy + c1_off[1])
        p2 = (cx + c2_off[0], cy + c2_off[1])
        p3 = (cx, cy)

        t_start = 1.50 + idx * 0.055
        t_land = 2.06 + idx * 0.115

        locks.append({
            "word": word,
            "x": cur_x,
            "y": base_y,
            "w": w_px,
            "h": h_px,
            "cx": cx,
            "cy": cy,
            "p0": p0,
            "p1": p1,
            "p2": p2,
            "p3": p3,
            "t_start": t_start,
            "t_land": t_land,
            "color": COMET_COLORS[idx],
        })
        cur_x += w_px + space_w
    return locks

WORD_LOCKS = precompute_word_locks()

# ==============================================================================
# SECRET #3: SPRING RECOIL & CAMERA RIGGING
# ==============================================================================
def get_chat_spring_offset(t):
    dy = 0.0
    for idx, lk in enumerate(WORD_LOCKS):
        dt = t - lk["t_land"]
        if 0.0 <= dt <= 0.75:
            amp = 9.5 if idx in (0, 2, 4, 6) else 7.0
            dy += amp * math.exp(-6.5 * dt) * math.sin(26.0 * dt)

    if t >= 6.22:
        dt_launch = t - 6.22
        dy += 28.0 * ease_out_cubic(clamp(dt_launch / 0.36))
    return dy

def get_camera_state(t):
    cx, cy, scale = W * 0.5, H * 0.5, 1.0
    if t < 1.5:
        u = ease_out_expo(prog(t, 0.0, 1.15))
        scale = 0.80 + 0.20 * u
    elif 3.92 <= t < 5.95:
        if t < 4.30:
            z = ease_in_out_cubic(prog(t, 3.92, 4.30))
        elif t < 5.55:
            z = 1.0
        else:
            z = 1.0 - ease_in_out_cubic(prog(t, 5.55, 5.95))
        target_cx = 1195.0
        target_cy = 445.0
        drift_y = -14.0 * ease_in_out_cubic(prog(t, 4.48, 4.95)) * z
        cx = (W * 0.5) * (1.0 - z) + target_cx * z
        cy = (H * 0.5) * (1.0 - z) + (target_cy + drift_y) * z
        scale = 1.0 + 1.38 * z
    return cx, cy, scale

def world_to_screen(wx, wy, cam):
    cx, cy, scale = cam
    sx = (wx - cx) * scale + W * 0.5
    sy = (wy - cy) * scale + H * 0.5
    return sx, sy

# ==============================================================================
# FAST C-LEVEL PIL ADDITIVE GLOW & DRAWING HELPERS
# ==============================================================================
def composite_glow_and_sharp(bg_pil, glow_rgba_img, sharp_rgba_img, blur_small=6):
    """Fast PIL C-level glow blur + additive blend + alpha composite."""
    gw, gh = W // 4, H // 4
    small = glow_rgba_img.resize((gw, gh), Image.Resampling.BILINEAR)
    blurred = small.filter(ImageFilter.GaussianBlur(blur_small))
    full_glow = blurred.resize((W, H), Image.Resampling.BILINEAR)

    # Pre-multiply glow RGB by its alpha channel in fast uint16/uint8 C-op
    r, g, b, a = full_glow.split()
    glow_rgb = Image.merge("RGB", (
        ImageChops.multiply(r, a),
        ImageChops.multiply(g, a),
        ImageChops.multiply(b, a),
    ))
    out = ImageChops.add(bg_pil, glow_rgb)
    out.paste(sharp_rgba_img, (0, 0), sharp_rgba_img)
    return out

def draw_comet_head(draw_sharp, draw_glow, x, y, color, radius=11.0):
    r, g, b = color
    R_glow = radius * 3.2
    draw_glow.ellipse([x - R_glow, y - R_glow, x + R_glow, y + R_glow], fill=(r, g, b, 245))
    R_mid = radius * 1.35
    draw_sharp.ellipse([x - R_mid, y - R_mid, x + R_mid, y + R_mid], fill=(r, g, b, 245))
    R_core = radius * 0.72
    draw_sharp.ellipse([x - R_core, y - R_core, x + R_core, y + R_core], fill=(255, 255, 255, 255))
    flare_len = radius * 2.2
    draw_sharp.line([(x - flare_len, y), (x + flare_len, y)], fill=(255, 255, 255, 225), width=2)
    draw_sharp.line([(x, y - flare_len * 0.8), (x, y + flare_len * 0.8)], fill=(255, 255, 255, 225), width=2)

def draw_pill_vector_icon(draw, kind, cx, cy, scale, alpha):
    """Draw crisp vector icons for the 5 bottom agent pills (no missing glyph boxes!)."""
    s = scale
    if kind == "agent":
        f_ag = get_font(SANS_BOLD_PATH, 16 * s)
        draw.text((cx - 14 * s, cy - 9 * s), "</>", font=f_ag, fill=(148, 175, 205, alpha))
    elif kind == "canvas":
        # 4-point sparkle star ✦
        r_out, r_in = 8.0 * s, 2.6 * s
        pts = [
            (cx, cy - r_out), (cx + r_in, cy - r_in),
            (cx + r_out, cy), (cx + r_in, cy + r_in),
            (cx, cy + r_out), (cx - r_in, cy + r_in),
            (cx - r_out, cy), (cx - r_in, cy - r_in),
        ]
        draw.polygon(pts, fill=(225, 238, 255, alpha))
    elif kind == "browser":
        # Yellow lightning bolt ⚡
        pts = [
            (cx + 2 * s, cy - 8.5 * s),
            (cx - 5.5 * s, cy + 1.0 * s),
            (cx - 0.5 * s, cy + 1.0 * s),
            (cx - 2.5 * s, cy + 8.5 * s),
            (cx + 5.5 * s, cy - 1.0 * s),
            (cx + 0.5 * s, cy - 1.0 * s),
        ]
        draw.polygon(pts, fill=(250, 204, 21, alpha))
    elif kind == "sandbox":
        # Command / Grid icon ⌘
        d = 4.2 * s
        w = max(1, int(1.8 * s))
        col = (180, 198, 220, alpha)
        draw.rectangle([cx - d, cy - d, cx + d, cy + d], outline=col, width=w)
        for ox, oy in [(-d, -d), (d, -d), (-d, d), (d, d)]:
            draw.ellipse([cx + ox - 3 * s, cy + oy - 3 * s, cx + ox + 3 * s, cy + oy + 3 * s], outline=col, width=w)
    elif kind == "deploy":
        # Rocket icon 🚀
        pts_body = [
            (cx + 6.5 * s, cy - 6.5 * s),
            (cx + 2.0 * s, cy - 5.5 * s),
            (cx - 4.5 * s, cy + 1.0 * s),
            (cx - 1.0 * s, cy + 4.5 * s),
            (cx + 5.5 * s, cy - 2.0 * s),
        ]
        draw.polygon(pts_body, fill=(248, 113, 113, alpha))
        draw.polygon([(cx - 4.5 * s, cy + 1.0 * s), (cx - 7.5 * s, cy + 7.5 * s), (cx - 1.0 * s, cy + 4.5 * s)],
                     fill=(251, 191, 36, alpha))

# ==============================================================================
# ACT RENDERERS
# ==============================================================================
def render_eclipse_and_title(t, sharp_img, draw_sharp, draw_glow, cam):
    if t > 2.25:
        return

    ring_fade = 1.0 - ease_in_cubic(prog(t, 1.65, 2.22))
    if ring_fade > 0.01:
        rcx, rcy = world_to_screen(995.0, 500.0, cam)
        _, _, scale = cam
        r_inner = 335.0 * scale
        r_outer = 442.0 * scale

        ang_in = -35.0 - t * 28.0
        ang_out = -65.0 + t * 22.0
        a_val = int(255 * ring_fade)
        a_glow = int(245 * ring_fade)

        bbox_in = [rcx - r_inner, rcy - r_inner, rcx + r_inner, rcy + r_inner]
        bbox_out = [rcx - r_outer, rcy - r_outer, rcx + r_outer, rcy + r_outer]

        draw_glow.arc(bbox_in, start=ang_in, end=ang_in + 250, fill=(0, 230, 255, a_glow), width=int(26 * scale))
        draw_glow.arc(bbox_out, start=ang_out, end=ang_out + 215, fill=(175, 75, 255, a_glow), width=int(28 * scale))

        draw_sharp.arc(bbox_in, start=ang_in, end=ang_in + 250, fill=(65, 245, 255, a_val), width=max(2, int(8 * scale)))
        draw_sharp.arc(bbox_in, start=ang_in + 5, end=ang_in + 245, fill=(220, 255, 255, a_val), width=max(1, int(3 * scale)))
        draw_sharp.arc(bbox_out, start=ang_out, end=ang_out + 215, fill=(210, 140, 255, a_val), width=max(2, int(8 * scale)))
        draw_sharp.arc(bbox_out, start=ang_out + 5, end=ang_out + 210, fill=(245, 225, 255, a_val), width=max(1, int(3 * scale)))

    if t < 1.98:
        _, _, scale = cam
        lift_y = -14.0 * math.sin(prog(t, 1.38, 1.65) * math.pi) if t >= 1.38 else 0.0
        peel_u = prog(t, 1.50, 1.92)

        if peel_u < 0.12:
            lx, ly = world_to_screen(582.0, 502.0 + lift_y, cam)
            logo_sz = int(112 * scale)
            lg = get_logo(logo_sz)
            sharp_img.alpha_composite(lg, (int(lx - logo_sz // 2), int(ly - logo_sz // 2)))

        f_title = get_font(SERIF_PATH, 108 * scale)
        word = "Antigravity"
        cur_wx = 668.0
        base_wy = 442.0 + lift_y
        for i, ch in enumerate(word):
            ch_w = draw_sharp.textlength(ch, font=f_title) / scale
            # Fix: use (i + 1) so index 0 ('A') is visible when peel_u == 0.0!
            ch_thresh = ((i + 1) / len(word)) * 0.85
            if peel_u < ch_thresh:
                sx, sy = world_to_screen(cur_wx, base_wy, cam)
                if peel_u > 0.01 and peel_u > ch_thresh - 0.18:
                    col = (245, 205, 75, 245)
                else:
                    col = (255, 255, 255, 255)
                draw_sharp.text((sx, sy), ch, font=f_title, fill=col)
            cur_wx += ch_w

        if peel_u < 0.94:
            f_sup = get_font(SANS_BOLD_PATH, 44 * scale)
            sx, sy = world_to_screen(cur_wx + 12.0, base_wy + 6.0, cam)
            draw_glow.text((sx, sy), "2.0", font=f_sup, fill=(0, 235, 255, 220))
            draw_sharp.text((sx, sy), "2.0", font=f_sup, fill=(45, 235, 255, 255))


def render_chat_and_comets(t, sharp_img, draw_sharp, draw_glow, cam):
    if t < 1.50 or t > 6.65:
        return

    _, _, scale = cam
    chat_alpha = prog(t, 1.65, 2.05) * (1.0 - ease_in_cubic(prog(t, 6.22, 6.62)))
    spring_dy = get_chat_spring_offset(t)

    if chat_alpha > 0.01:
        x0, y0 = world_to_screen(CHAT_X, CHAT_Y + spring_dy, cam)
        x1, y1 = world_to_screen(CHAT_X + CHAT_W, CHAT_Y + CHAT_H + spring_dy, cam)
        rad = int(26 * scale)
        a_card = int(234 * chat_alpha)
        a_bord = int(180 * chat_alpha)

        draw_glow.rounded_rectangle([x0 - 6 * scale, y0 + 6 * scale, x1 + 6 * scale, y1 + 14 * scale],
                                    radius=rad, fill=(0, 150, 235, int(75 * chat_alpha)))
        draw_sharp.rounded_rectangle([x0, y0, x1, y1], radius=rad,
                                     fill=(8, 13, 24, a_card),
                                     outline=(38, 88, 135, a_bord),
                                     width=max(1, int(2 * scale)))

    f_prompt = get_font(SANS_PATH, 31 * scale)
    for lk in WORD_LOCKS:
        if t >= lk["t_land"]:
            dt_hit = t - lk["t_land"]
            wx, wy = world_to_screen(lk["x"], lk["y"] + spring_dy, cam)
            ww, wh = lk["w"] * scale, lk["h"] * scale
            r, g, b = lk["color"]

            if dt_hit < 0.42:
                hl_u = 1.0 - ease_out_cubic(dt_hit / 0.42)
                pad_x, pad_y = 14 * scale, 10 * scale
                bx0, by0 = wx - pad_x, wy - pad_y
                bx1, by1 = wx + ww + pad_x, wy + wh + pad_y
                draw_glow.rounded_rectangle([bx0, by0, bx1, by1], radius=int(8 * scale),
                                            fill=(r, g, b, int(185 * hl_u)))
                draw_sharp.rounded_rectangle([bx0, by0, bx1, by1], radius=int(8 * scale),
                                             fill=(r, g, b, int(80 * hl_u)),
                                             outline=(r, g, b, int(195 * hl_u)), width=1)
                icx, icy = world_to_screen(lk["cx"], lk["cy"] + spring_dy, cam)
                ring_r = (16.0 + 95.0 * ease_out_cubic(dt_hit / 0.42)) * scale
                draw_sharp.ellipse([icx - ring_r, icy - ring_r, icx + ring_r, icy + ring_r],
                                   outline=(r, g, b, int(185 * hl_u)), width=max(1, int(2 * scale)))

            color_cool = clamp(dt_hit / 0.32)
            wr = int(r * (1.0 - color_cool) + 255 * color_cool)
            wg = int(g * (1.0 - color_cool) + 255 * color_cool)
            wb = int(b * (1.0 - color_cool) + 255 * color_cool)
            draw_sharp.text((wx, wy), lk["word"], font=f_prompt, fill=(wr, wg, wb, int(255 * chat_alpha)))

    ui_alpha = prog(t, 2.55, 3.05) * chat_alpha
    if ui_alpha > 0.01:
        a_ui = int(255 * ui_alpha)
        px, py = world_to_screen(CHAT_X + 46, CHAT_Y + 172 + spring_dy, cam)
        plus_r = 11 * scale
        draw_sharp.line([(px - plus_r, py), (px + plus_r, py)], fill=(155, 170, 195, a_ui), width=max(2, int(2.2 * scale)))
        draw_sharp.line([(px, py - plus_r), (px, py + plus_r)], fill=(155, 170, 195, a_ui), width=max(2, int(2.2 * scale)))

        # Clean vertical slot-scroll for Model Trigger (finishes by 4.90s so 5.0s is 100% clean!)
        f_trig = get_font(SANS_PATH, 21 * scale)
        f_trig_b = get_font(SANS_BOLD_PATH, 21 * scale)
        swap_u = ease_in_out_cubic(prog(t, 4.52, 4.90))
        trig_wx = CHAT_X + CHAT_W - 332
        trig_wy = CHAT_Y + 160 + spring_dy

        if swap_u < 0.99:
            old_a = int(a_ui * (1.0 - swap_u))
            ox, oy = world_to_screen(trig_wx, trig_wy - 18.0 * swap_u, cam)
            draw_sharp.text((ox, oy), "Gemini 3.8 Flash ", font=f_trig, fill=(235, 242, 252, old_a))
            w1 = draw_sharp.textlength("Gemini 3.8 Flash ", font=f_trig)
            draw_sharp.text((ox + w1, oy), "High", font=f_trig, fill=(148, 163, 184, old_a))

        if swap_u > 0.01:
            new_a = int(a_ui * swap_u)
            nx, ny = world_to_screen(trig_wx + 6, trig_wy + 18.0 * (1.0 - swap_u), cam)
            draw_glow.text((nx, ny), "Gemini 4 Argon ", font=f_trig_b, fill=(0, 240, 255, int(new_a * 0.85)))
            draw_sharp.text((nx, ny), "Gemini 4 Argon ", font=f_trig_b, fill=(56, 235, 255, new_a))
            w2 = draw_sharp.textlength("Gemini 4 Argon ", font=f_trig_b)
            draw_sharp.text((nx + w2, ny), "High", font=f_trig, fill=(165, 180, 200, new_a))

        chev_x, chev_y = world_to_screen(CHAT_X + CHAT_W - 110, trig_wy + 12, cam)
        menu_open = 3.95 <= t <= 5.92
        cs = 5.5 * scale
        if menu_open:
            draw_sharp.line([(chev_x - cs, chev_y + cs * 0.5), (chev_x, chev_y - cs * 0.5), (chev_x + cs, chev_y + cs * 0.5)],
                            fill=(180, 195, 215, a_ui), width=max(2, int(2.2 * scale)))
        else:
            draw_sharp.line([(chev_x - cs, chev_y - cs * 0.5), (chev_x, chev_y + cs * 0.5), (chev_x + cs, chev_y - cs * 0.5)],
                            fill=(180, 195, 215, a_ui), width=max(2, int(2.2 * scale)))

        # Send Button [↑]
        if t < 6.26:
            sb_cx = CHAT_X + CHAT_W - 56
            sb_cy = CHAT_Y + 171 + spring_dy
            squash = math.sin(prog(t, 5.95, 6.24) * math.pi) if t >= 5.95 else 0.0
            sx_mult = 1.0 + 0.25 * squash
            sy_mult = 1.0 - 0.28 * squash
            bw = 27.0 * sx_mult * scale
            bh = 27.0 * sy_mult * scale
            scx, scy = world_to_screen(sb_cx, sb_cy, cam)

            glow_boost = int(195 + 60 * squash)
            draw_glow.rounded_rectangle([scx - bw * 1.35, scy - bh * 1.35, scx + bw * 1.35, scy + bh * 1.35],
                                        radius=int(18 * scale), fill=(0, 225, 255, int(glow_boost * ui_alpha)))
            btn_col = (int(42 + 130 * squash), int(125 + 128 * squash), 255, a_ui)
            draw_sharp.rounded_rectangle([scx - bw, scy - bh, scx + bw, scy + bh],
                                         radius=int(15 * scale), fill=btn_col,
                                         outline=(110, 235, 255, a_ui), width=max(1, int(1.8 * scale)))
            ar = 10.0 * scale * sy_mult
            aw = 7.5 * scale * sx_mult
            draw_sharp.line([(scx, scy + ar), (scx, scy - ar)], fill=(255, 255, 255, a_ui), width=max(2, int(2.8 * scale)))
            draw_sharp.line([(scx - aw, scy - ar + aw * 0.85), (scx, scy - ar), (scx + aw, scy - ar + aw * 0.85)],
                            fill=(255, 255, 255, a_ui), width=max(2, int(2.8 * scale)))

    if ui_alpha > 0.01:
        slide_y = (1.0 - ease_out_cubic(prog(t, 2.55, 3.15))) * 18.0
        gx, gy = world_to_screen(632.0, 298.0 + slide_y + spring_dy * 0.35, cam)
        logo_g = get_logo(int(64 * scale))
        if ui_alpha > 0.85:
            sharp_img.alpha_composite(logo_g, (int(gx), int(gy + 4 * scale)))
        else:
            lg_copy = logo_g.copy()
            r_c, g_c, b_c, a_c = lg_copy.split()
            a_c = a_c.point(lambda p: int(p * ui_alpha))
            lg_copy.putalpha(a_c)
            sharp_img.alpha_composite(lg_copy, (int(gx), int(gy + 4 * scale)))

        f_greet = get_font(SERIF_PATH, 66 * scale)
        tx1 = gx + 82 * scale
        ty1 = gy
        draw_sharp.text((tx1, ty1), "Good evening, ", font=f_greet, fill=(248, 250, 255, int(255 * ui_alpha)))
        w_ge = draw_sharp.textlength("Good evening, ", font=f_greet)
        draw_glow.text((tx1 + w_ge, ty1), "builder", font=f_greet, fill=(0, 215, 255, int(185 * ui_alpha)))
        draw_sharp.text((tx1 + w_ge, ty1), "builder", font=f_greet, fill=(75, 225, 255, int(255 * ui_alpha)))

        # 5 Bottom Tool Pills with Crisp Vector Icons
        pills = [
            ("agent", "Agent"),
            ("canvas", "Canvas"),
            ("browser", "Browser"),
            ("sandbox", "Sandbox"),
            ("deploy", "Deploy"),
        ]
        f_pill = get_font(SANS_BOLD_PATH, 19 * scale)
        pill_x = 520.0
        pill_y = 668.0 + spring_dy * 0.6
        for idx, (kind, label) in enumerate(pills):
            p_u = ease_out_cubic(prog(t, 2.70 + idx * 0.07, 3.15 + idx * 0.07)) * chat_alpha
            if p_u > 0.01:
                pa = int(242 * p_u)
                pw, ph = 160.0, 48.0
                px0, py0 = world_to_screen(pill_x, pill_y + (1.0 - p_u) * 14.0, cam)
                px1, py1 = world_to_screen(pill_x + pw, pill_y + ph + (1.0 - p_u) * 14.0, cam)
                draw_sharp.rounded_rectangle([px0, py0, px1, py1], radius=int(12 * scale),
                                             fill=(15, 24, 42, pa),
                                             outline=(45, 72, 108, int(185 * p_u)), width=max(1, int(1.5 * scale)))
                ic_x = px0 + 34 * scale
                ic_y = (py0 + py1) * 0.5
                draw_pill_vector_icon(draw_sharp, kind, ic_x, ic_y, scale, pa)
                draw_sharp.text((px0 + 56 * scale, py0 + 13 * scale), label,
                                font=f_pill, fill=(235, 242, 250, pa))
            pill_x += 180.0

    for lk in WORD_LOCKS:
        if lk["t_start"] <= t <= lk["t_land"] + 0.06:
            u = ease_in_out_cubic(prog(t, lk["t_start"], lk["t_land"]))
            p0, p1, p2 = lk["p0"], lk["p1"], lk["p2"]
            p3 = (lk["cx"], lk["cy"] + spring_dy)

            trail_span = 0.34
            u_tail = max(0.0, u - trail_span)
            steps = 28
            pts_screen = []
            for s in range(steps + 1):
                us = u_tail + (u - u_tail) * (s / steps)
                wx, wy = cubic_bezier(us, p0, p1, p2, p3)
                pts_screen.append(world_to_screen(wx, wy, cam))

            r, g, b = lk["color"]
            fade_tail = 1.0 - prog(t, lk["t_land"], lk["t_land"] + 0.06)
            for s in range(steps):
                frac = (s + 1) / steps
                w_seg = max(1, int((2.0 + 10.0 * frac) * scale))
                a_seg = int(245 * (frac ** 1.6) * fade_tail)
                draw_glow.line([pts_screen[s], pts_screen[s + 1]], fill=(r, g, b, a_seg), width=w_seg * 2)
                cr = int(r * (1.0 - 0.6 * frac) + 255 * 0.6 * frac)
                cg = int(g * (1.0 - 0.6 * frac) + 255 * 0.6 * frac)
                cb = int(b * (1.0 - 0.6 * frac) + 255 * 0.6 * frac)
                draw_sharp.line([pts_screen[s], pts_screen[s + 1]], fill=(cr, cg, cb, a_seg), width=w_seg)

            if t <= lk["t_land"]:
                hx, hy = pts_screen[-1]
                draw_comet_head(draw_sharp, draw_glow, hx, hy, lk["color"], radius=11.0 * scale)


def render_model_selector_popup(t, draw_sharp, draw_glow, cam):
    if t < 3.96 or t > 5.92:
        return

    _, _, scale = cam
    pop_in = ease_out_cubic(prog(t, 3.96, 4.22))
    pop_out = 1.0 - ease_in_cubic(prog(t, 5.65, 5.92))
    alpha_f = pop_in * pop_out
    if alpha_f <= 0.01:
        return

    pw, ph = 448.0, 326.0
    px0_w = 972.0
    py0_w = 232.0 + (1.0 - pop_in) * 14.0
    x0, y0 = world_to_screen(px0_w, py0_w, cam)
    x1, y1 = world_to_screen(px0_w + pw, py0_w + ph, cam)

    a_bg = int(248 * alpha_f)
    a_bd = int(195 * alpha_f)
    rad = int(18 * scale)

    draw_glow.rounded_rectangle([x0 - 4 * scale, y0 - 4 * scale, x1 + 4 * scale, y1 + 4 * scale],
                                radius=rad, fill=(0, 195, 235, int(75 * alpha_f)))
    draw_sharp.rounded_rectangle([x0, y0, x1, y1], radius=rad,
                                 fill=(9, 15, 26, a_bg),
                                 outline=(28, 118, 142, a_bd),
                                 width=max(2, int(1.6 * scale)))

    sel_u = ease_in_out_cubic(prog(t, 4.50, 4.90))
    row_h = 61.0
    pad = 11.0
    sel_row_y = py0_w + pad + (1.0 - sel_u) * row_h
    sx0, sy0 = world_to_screen(px0_w + pad, sel_row_y, cam)
    sx1, sy1 = world_to_screen(px0_w + pw - pad, sel_row_y + 56.0, cam)

    fill_r = int(28 * (1.0 - sel_u) + 8 * sel_u)
    fill_g = int(38 * (1.0 - sel_u) + 52 * sel_u)
    fill_b = int(52 * (1.0 - sel_u) + 68 * sel_u)
    bord_r = int(75 * (1.0 - sel_u) + 20 * sel_u)
    bord_g = int(90 * (1.0 - sel_u) + 215 * sel_u)
    bord_b = int(110 * (1.0 - sel_u) + 240 * sel_u)

    if sel_u > 0.2:
        draw_glow.rounded_rectangle([sx0, sy0, sx1, sy1], radius=int(11 * scale),
                                    fill=(0, 210, 245, int(95 * sel_u * alpha_f)))
    draw_sharp.rounded_rectangle([sx0, sy0, sx1, sy1], radius=int(11 * scale),
                                 fill=(fill_r, fill_g, fill_b, int(235 * alpha_f)),
                                 outline=(bord_r, bord_g, bord_b, int(225 * alpha_f)),
                                 width=max(1, int(1.4 * scale)))

    ck_x = sx1 - 28 * scale
    ck_y = (sy0 + sy1) * 0.5
    ck_col = (
        int(240 * (1.0 - sel_u) + 45 * sel_u),
        int(245 * (1.0 - sel_u) + 240 * sel_u),
        255,
        int(255 * alpha_f),
    )
    cs = 6.5 * scale
    draw_sharp.line([(ck_x - cs, ck_y), (ck_x - cs * 0.25, ck_y + cs * 0.75), (ck_x + cs * 1.1, ck_y - cs * 0.75)],
                    fill=ck_col, width=max(2, int(2.4 * scale)))

    models = [
        ("Gemini 4 Argon", "High", "New", (12, 74, 88), (45, 235, 245), "Most capable for ambitious agent work"),
        ("Gemini 3.8 Flash", "High", "Fast", (16, 72, 42), (74, 222, 128), "Ultra-fast multimodal agent execution"),
        ("Claude Opus 5.5", "High", "New", (62, 24, 88), (192, 132, 252), "Deep reasoning & complex architecture"),
        ("Claude Sonnet 5.5", "High", "New", (22, 48, 92), (96, 165, 250), "Balanced speed for everyday engineering"),
        ("GPT-OSS 120B", "Medium", "Notice", (72, 52, 16), (250, 204, 21), "Open-weight reasoning model"),
    ]

    f_name = get_font(SANS_BOLD_PATH, 18.5 * scale)
    f_tier = get_font(SANS_PATH, 17.5 * scale)
    f_badge = get_font(SANS_BOLD_PATH, 11.5 * scale)
    f_desc = get_font(SANS_PATH, 13.5 * scale)

    for idx, (m_name, m_tier, b_txt, b_bg, b_fg, m_desc) in enumerate(models):
        ry_w = py0_w + pad + idx * row_h
        rx, ry = world_to_screen(px0_w + 24.0, ry_w + 7.0, cam)

        if idx == 0 and sel_u > 0.35:
            name_col = (
                int(255 * (1.0 - sel_u) + 56 * sel_u),
                int(255 * (1.0 - sel_u) + 238 * sel_u),
                255,
                int(255 * alpha_f),
            )
        else:
            name_col = (248, 250, 252, int(255 * alpha_f))

        draw_sharp.text((rx, ry), m_name, font=f_name, fill=name_col)
        w_n = draw_sharp.textlength(m_name + "  ", font=f_name)
        draw_sharp.text((rx + w_n, ry + 1 * scale), m_tier, font=f_tier, fill=(148, 163, 184, int(245 * alpha_f)))
        w_t = draw_sharp.textlength(m_tier + "  ", font=f_tier)

        bx0 = rx + w_n + w_t + 2 * scale
        by0 = ry + 1 * scale
        bw_txt = draw_sharp.textlength(b_txt, font=f_badge)
        bx1 = bx0 + bw_txt + 16 * scale
        by1 = by0 + 19 * scale
        draw_sharp.rounded_rectangle([bx0, by0, bx1, by1], radius=int(9.5 * scale),
                                     fill=(*b_bg, int(230 * alpha_f)),
                                     outline=(*b_fg, int(185 * alpha_f)),
                                     width=max(1, int(1.1 * scale)))
        draw_sharp.text((bx0 + 8 * scale, by0 + 3 * scale), b_txt, font=f_badge, fill=(*b_fg, int(255 * alpha_f)))
        draw_sharp.text((rx, ry + 25 * scale), m_desc, font=f_desc, fill=(142, 158, 178, int(235 * alpha_f)))


def render_act4_photon_and_laser_text(t, draw_sharp, draw_glow, cam):
    if t < 5.95 or t > 8.15:
        return

    # 1. Expanding cyan shockwave ring around Send button at launch (5.95s -> 6.45s, visible at 6.00s!)
    if 5.95 <= t <= 6.48:
        u_ring = ease_out_cubic(prog(t, 5.95, 6.48))
        rcx, rcy = CHAT_X + CHAT_W - 56, CHAT_Y + 171
        r_rad = 38.0 + 190.0 * u_ring
        a_ring = int(250 * (1.0 - u_ring * 0.85))
        draw_glow.ellipse([rcx - r_rad, rcy - r_rad, rcx + r_rad, rcy + r_rad],
                          outline=(0, 235, 255, a_ring), width=14)
        draw_sharp.ellipse([rcx - r_rad, rcy - r_rad, rcx + r_rad, rcy + r_rad],
                           outline=(140, 248, 255, a_ring), width=4)

    # 2. S-Curve Photon Launch (6.22s -> 6.76s)
    if 6.22 <= t <= 6.80:
        u_s = ease_in_out_cubic(prog(t, 6.22, 6.75))
        p0 = (1474.0, 610.0)
        p1 = (1615.0, 355.0)
        p2 = (1180.0, 395.0)
        p3 = (492.0, 488.0)

        u_tail = max(0.0, u_s - 0.58)
        steps = 36
        pts = [cubic_bezier(u_tail + (u_s - u_tail) * (i / steps), p0, p1, p2, p3) for i in range(steps + 1)]
        fade_s = 1.0 - prog(t, 6.70, 6.80)
        for i in range(steps):
            frac = (i + 1) / steps
            a_seg = int(250 * (frac ** 1.4) * fade_s)
            w_seg = max(2, int(3 + 11 * frac))
            draw_glow.line([pts[i], pts[i + 1]], fill=(0, 230, 255, a_seg), width=w_seg * 2)
            draw_sharp.line([pts[i], pts[i + 1]], fill=(185, 250, 255, a_seg), width=w_seg)
        if t <= 6.76:
            hx, hy = pts[-1]
            draw_comet_head(draw_sharp, draw_glow, hx, hy, (0, 240, 255), radius=15.0)

    # 3. Laser Text Crystallization (6.68s -> 7.98s, imploding into 8.00s singularity!)
    lines = [
        ("Antigravity 2.0 represents a fundamental shift in how we engineer with autonomous AI.", 250.0),
        ("Built upon a parallel multi-agent architecture, it orchestrates subagents, background tasks,", 288.0),
        ("and live browser instrumentation to prioritize deep execution over simple code autocomplete.", 326.0),
        ("Unlike traditional IDE assistants, it is designed to understand the full topology of your stack.", 392.0),
        ("Every terminal sandbox, MCP tool call, and visual artifact is verified end-to-end, delivering", 430.0),
        ("production-grade accuracy that redefines autonomous software craftsmanship.", 468.0),
    ]

    if 6.68 <= t <= 7.96:
        implode_u = ease_in_cubic(prog(t, 7.68, 7.96))
        scale_txt = 1.0 - 0.82 * implode_u
        alpha_implode = 1.0 - implode_u
        f_body = get_font(SERIF_PATH, max(10, int(26.5 * scale_txt)))
        x_left = 492.0

        for idx, (text_line, ly_base) in enumerate(lines):
            t_l0 = 6.68 + idx * 0.13
            t_l1 = t_l0 + 0.22
            if t < t_l0:
                continue

            scan_u = ease_out_cubic(prog(t, t_l0, t_l1))
            full_w = draw_sharp.textlength(text_line, font=f_body)
            reveal_chars = int(round(len(text_line) * scan_u))
            sub_txt = text_line[:reveal_chars]

            lx = x_left * (1.0 - implode_u) + (W * 0.5 - full_w * 0.5) * implode_u
            ly = ly_base * (1.0 - implode_u) + (H * 0.5) * implode_u

            dt_after = max(0.0, t - t_l1)
            cool_u = clamp(dt_after / 0.28)

            if cool_u < 1.0:
                cur_w = draw_sharp.textlength(sub_txt, font=f_body)
                plasma_a = int(225 * (1.0 - cool_u) * alpha_implode)
                draw_glow.rounded_rectangle([lx - 6, ly + 2, lx + cur_w + 12, ly + 30 * scale_txt],
                                            radius=10, fill=(0, 195, 255, plasma_a))
                draw_glow.text((lx, ly), sub_txt, font=f_body, fill=(60, 235, 255, plasma_a))

            tr = int(155 * (1.0 - cool_u) + 255 * cool_u)
            tg = int(235 * (1.0 - cool_u) + 255 * cool_u)
            tb = 255
            draw_sharp.text((lx, ly), sub_txt, font=f_body, fill=(tr, tg, tb, int(255 * alpha_implode)))

            if 0.01 < scan_u < 0.99:
                cur_w = draw_sharp.textlength(sub_txt, font=f_body)
                orb_x = lx + cur_w
                orb_y = ly + 15 * scale_txt
                trail_w = min(cur_w, 420.0)
                draw_glow.line([(orb_x - trail_w, orb_y), (orb_x, orb_y)], fill=(0, 225, 255, 240), width=14)
                draw_sharp.line([(orb_x - trail_w * 0.7, orb_y), (orb_x, orb_y)], fill=(195, 250, 255, 225), width=4)
                draw_comet_head(draw_sharp, draw_glow, orb_x, orb_y, (0, 240, 255), radius=14.0)


def render_act5_finale(t, sharp_img, draw_sharp, draw_glow):
    if t < 7.82:
        return

    # 1. Singularity Ring Phase (7.82s -> 8.65s, so 00:00:08.000 matches image1.jpg 1:1!)
    if t < 8.68:
        ring_in = ease_out_cubic(prog(t, 7.82, 8.02))
        ring_boom = prog(t, 8.35, 8.68)
        r_sing = 148.0 * ring_in + 380.0 * ease_out_cubic(ring_boom)
        a_sing = int(250 * ring_in * (1.0 - ring_boom))
        cx, cy = W * 0.5, H * 0.5

        draw_glow.ellipse([cx - r_sing, cy - r_sing, cx + r_sing, cy + r_sing],
                          outline=(0, 235, 255, a_sing), width=18)
        draw_sharp.ellipse([cx - r_sing, cy - r_sing, cx + r_sing, cy + r_sing],
                           outline=(135, 248, 255, a_sing), width=5)

        if t < 8.45:
            f_sing = get_font(SERIF_PATH, 62)
            tw = draw_sharp.textlength("Antigravity", font=f_sing)
            ta = int(245 * ring_in * (1.0 - prog(t, 8.30, 8.45)))
            draw_sharp.text((cx - tw * 0.5, cy - 34), "Antigravity", font=f_sing, fill=(225, 245, 255, ta))

    # 2. 3-Beat Brand Lockup (8.45s -> 12.0s: Code -> Build -> 2.0)
    if t >= 8.42:
        u_enter = ease_out_cubic(prog(t, 8.42, 8.75))
        base_x = 432.0
        base_y = 480.0 + (1.0 - u_enter) * 18.0

        logo_sz = 112
        lg = get_logo(logo_sz)
        sharp_img.alpha_composite(lg, (int(base_x), int(base_y + 4)))

        f_brand = get_font(SERIF_PATH, 112)
        tx = base_x + 132.0
        ty = base_y - 4.0
        draw_sharp.text((tx, ty), "Antigravity ", font=f_brand, fill=(238, 248, 255, int(255 * u_enter)))
        w_anti = draw_sharp.textlength("Antigravity ", font=f_brand)
        sx = tx + w_anti

        if t < 9.75:
            b_u = ease_out_cubic(prog(t, 8.45, 8.78)) * (1.0 - prog(t, 9.60, 9.75))
            dy_b = (1.0 - ease_out_cubic(prog(t, 8.45, 8.78))) * 22.0
            draw_glow.text((sx, ty + dy_b), "Code", font=f_brand, fill=(0, 245, 255, int(245 * b_u)))
            draw_sharp.text((sx, ty + dy_b), "Code", font=f_brand, fill=(95, 252, 255, int(255 * b_u)))
        elif t < 10.75:
            b_u = ease_out_cubic(prog(t, 9.75, 10.02)) * (1.0 - prog(t, 10.60, 10.75))
            dy_b = (1.0 - ease_out_cubic(prog(t, 9.75, 10.02))) * 22.0
            draw_glow.text((sx, ty + dy_b), "Build", font=f_brand, fill=(35, 245, 130, int(245 * b_u)))
            draw_sharp.text((sx, ty + dy_b), "Build", font=f_brand, fill=(115, 255, 175, int(255 * b_u)))
        else:
            b_u = ease_out_cubic(prog(t, 10.75, 11.02))
            dy_b = (1.0 - b_u) * 22.0
            draw_glow.text((sx, ty + dy_b), "2.0", font=f_brand, fill=(45, 245, 175, int(245 * b_u)))

            txt_w, txt_h = 220, 140
            mask_img = Image.new("L", (txt_w, txt_h), 0)
            ImageDraw.Draw(mask_img).text((0, 0), "2.0", font=f_brand, fill=int(255 * b_u))

            gy, gx = np.mgrid[0:txt_h, 0:txt_w].astype(np.float32)
            gt = np.clip((gy - 15.0) / 95.0, 0.0, 1.0)
            grad_rgba = np.zeros((txt_h, txt_w, 4), dtype=np.uint8)
            grad_rgba[:, :, 0] = ((1.0 - gt) * 250.0 + gt * 45.0).astype(np.uint8)
            grad_rgba[:, :, 1] = ((1.0 - gt) * 204.0 + gt * 245.0).astype(np.uint8)
            grad_rgba[:, :, 2] = ((1.0 - gt) * 35.0 + gt * 165.0).astype(np.uint8)
            grad_rgba[:, :, 3] = np.asarray(mask_img, dtype=np.uint8)
            sharp_img.alpha_composite(Image.fromarray(grad_rgba), (int(sx), int(ty + dy_b)))


# ==============================================================================
# MASTER FRAME COMPOSITOR
# ==============================================================================
BG_INTRO, BG_STD, BG_FIN = build_backgrounds()

def render_frame(frame_idx):
    t = frame_idx / float(FPS)

    if t < 1.55:
        bg_pil = BG_INTRO.copy()
    elif t < 2.25:
        u = ease_in_out_cubic(prog(t, 1.55, 2.25))
        bg_pil = Image.blend(BG_INTRO, BG_STD, u)
    elif t < 8.20:
        bg_pil = BG_STD.copy()
    elif t < 8.80:
        u = ease_in_out_cubic(prog(t, 8.20, 8.80))
        bg_pil = Image.blend(BG_STD, BG_FIN, u)
    else:
        bg_pil = BG_FIN.copy()

    sharp_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_sharp = ImageDraw.Draw(sharp_img)
    draw_glow = ImageDraw.Draw(glow_img)

    cam = get_camera_state(t)

    render_eclipse_and_title(t, sharp_img, draw_sharp, draw_glow, cam)
    render_chat_and_comets(t, sharp_img, draw_sharp, draw_glow, cam)
    render_model_selector_popup(t, draw_sharp, draw_glow, cam)
    render_act4_photon_and_laser_text(t, draw_sharp, draw_glow, cam)
    render_act5_finale(t, sharp_img, draw_sharp, draw_glow)

    return composite_glow_and_sharp(bg_pil, glow_img, sharp_img, blur_small=6)


# ==============================================================================
# MAIN RENDER PIPELINE
# ==============================================================================
def main():
    t0 = time.time()
    print(f"Rendering {TOTAL_FRAMES} frames (1920x1080 @ {FPS}fps) -> {OUT_MP4}...")
    cmd = [
        FFMPEG_BIN, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W}x{H}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", OUT_WAV,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "15",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        OUT_MP4,
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    contact_frames = {}
    key_timestamps = {
        "hoi_1_eclipse.jpg": int(0.8 * FPS),
        "hoi_2a_comets_peel.jpg": int(1.75 * FPS),
        "hoi_2b_comets_impact.jpg": int(2.45 * FPS),
        "hoi_2c_chat_ui.jpg": int(3.40 * FPS),
        "hoi_3a_macro_flash.jpg": int(4.35 * FPS),
        "hoi_3b_macro_argon.jpg": int(5.20 * FPS),
        "hoi_4a_send_recoil.jpg": int(6.10 * FPS),
        "hoi_4b_scurve_photon.jpg": int(6.52 * FPS),
        "hoi_4c_laser_text.jpg": int(7.35 * FPS),
        "hoi_5a_code.jpg": int(9.10 * FPS),
        "hoi_5b_build.jpg": int(10.20 * FPS),
        "hoi_5c_2_0.jpg": int(11.30 * FPS),
    }

    for f_idx in range(TOTAL_FRAMES):
        img = render_frame(f_idx)
        proc.stdin.write(img.tobytes())

        if f_idx % FPS == 0:
            sec = f_idx // FPS
            contact_frames[sec] = img.copy()

        for k_name, k_frame in key_timestamps.items():
            if f_idx == k_frame:
                img.save(os.path.join(ARTIFACT_DIR, "reconstructed", k_name), quality=94)

        if (f_idx + 1) % 180 == 0 or f_idx == TOTAL_FRAMES - 1:
            el = time.time() - t0
            print(f"  Rendered {f_idx + 1}/{TOTAL_FRAMES} frames ({el:.1f}s elapsed)")

    proc.stdin.close()
    proc.wait()

    cw, ch = 480, 270
    sheet = Image.new("RGB", (cw * 4, ch * 3), (0, 0, 0))
    d_sheet = ImageDraw.Draw(sheet)
    f_ts = get_font(SANS_PATH, 16)
    for sec in range(12):
        col = sec % 4
        row = sec // 4
        thumb = contact_frames[sec].resize((cw, ch), Image.Resampling.LANCZOS)
        x_off, y_off = col * cw, row * ch
        sheet.paste(thumb, (x_off, y_off))
        d_sheet.rectangle([x_off + 10, y_off + ch - 30, x_off + 122, y_off + ch - 8], fill=(8, 12, 20))
        d_sheet.text((x_off + 16, y_off + ch - 28), f"00:00:{sec:02d}.000", font=f_ts, fill=(235, 242, 250))
        d_sheet.rectangle([x_off, y_off, x_off + cw - 1, y_off + ch - 1], outline=(30, 45, 70), width=1)

    sheet_path = os.path.join(ARTIFACT_DIR, "reconstructed", "contact_sheet_4x3.jpg")
    sheet.save(sheet_path, quality=95)
    print(f"Done in {time.time() - t0:.1f}s! Video saved to: {OUT_MP4}")

if __name__ == "__main__":
    main()
