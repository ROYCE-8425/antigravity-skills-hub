---
name: cinematic-commercial-video-director
description: "Directs and renders Awwwards/Apple/Linear-tier 9:16 and 16:9 commercial, explainer, and product promo videos using a Chromium GPU Frame Engine (HTML5 +..."
---

# Cinematic Commercial & Explainer Video Director (Chromium GPU + Spatial Glass UI)

## When to Use
Use this skill whenever the user asks to create, upgrade, or direct a **commercial video, product promo, explainer video, or social storytelling reel (9:16 or 16:9)** that combines real-world human/lifestyle cinematography with UI/workflow demonstrations, kinetic typography, voiceover, and captions.

---

## 1. The "Absolute Zero" Anti-Patterns (Strictly Forbidden)

1. **NEVER render UI overlays with flat Python `PIL.ImageDraw` (`rounded_rectangle`):**
   - `PIL.ImageDraw` cannot render `backdrop-filter: blur()`, multi-layered ambient shadows, CSS gradients, concentric Double-Bezel (`Doppelrand`) borders, 3D CSS `perspective()` tilts, or crisp vector SVGs.
   - **Mandatory Engine:** Always render frames via **Playwright Headless Chromium GPU (`page.screenshot`)** or **Remotion**, where every frame is a true DOM/CSS3/SVG/Canvas composition driven deterministically by `window.setFrameTime(t)`.
2. **NEVER chop a 9:16 vertical photo in half with an opaque solid rectangle:**
   - Covering the lower 50–60% of a vertical 9:16 scene with an opaque white/gray wall destroys character body language (hands on laptop, handing products to customers, desk environment).
   - **Mandatory Composition:** Keep the **9:16 character/scene photography 100% Full-Bleed (`1080×1920`)** with continuous 3D Ken Burns camera motion (`scale` + `translate3d`), and float **translucent Frosted Glass Cards (`backdrop-filter: blur(22px) saturate(180%)`)** in the lower/middle spatial plane so the environment and character remain visible around and through the glass.
3. **NEVER use raw Unicode emojis (`💬`, `📋`, `⌨`, `⚠`) in rendered frames:**
   - System fonts frequently render missing glyphs as `▯` boxes. Always use **inline vector `<svg>` icons** (Lucide / Phosphor style with `stroke-width="2"` and `stroke-linecap="round"`).

---

## 2. Spatial Architecture: The 4-Layer Z-Axis Stack (9:16 Vertical `1080×1920`)

Every frame at timestamp `t` is composed of 4 depth layers along the Z-axis:

### Layer 0 — Full-Bleed Cinematic Plate (`z-index: 1`)
- Full `1080×1920` high-resolution scene image with continuous Ken Burns drift:
  - Odd scenes: `scale(1.0 -> 1.065)` + pan `(-1.5%, -1.0%)`
  - Even scenes: `scale(1.065 -> 1.01)` + pan `(1.5%, -0.8%)`
- **Cross-Scene Dissolve & Light Leak Overlay:** Smooth `0.45s` optical cross-dissolve + warm radial light bloom (`mix-blend-mode: screen`) across scene cuts.

### Layer 1 — Atmospheric Depth Scrim (`z-index: 2`)
- Subtle multi-stop vertical gradient scrim that preserves the character's face and upper body in crystal clarity (`y = 0..880px`) while gently deepening contrast in the lower interaction zone (`y = 880..1920px`):
  ```css
  background: linear-gradient(
    180deg,
    rgba(9, 13, 24, 0.42) 0%,
    rgba(9, 13, 24, 0.04) 18%,
    rgba(9, 13, 24, 0.08) 46%,
    rgba(9, 13, 24, 0.62) 72%,
    rgba(9, 13, 24, 0.88) 100%
  );
  ```

### Layer 2 — Double-Bezel Spatial Glass UI Cards (`z-index: 10`)
- Apply the **Double-Bezel (`Doppelrand`)** hardware enclosure pattern from `high-end-visual-design`:
  - **Outer Shell:** `padding: 8px`, `border-radius: 34px`, `background: rgba(255, 255, 255, 0.12)`, `border: 1px solid rgba(255, 255, 255, 0.24)`, `backdrop-filter: blur(24px) saturate(180%)`, `box-shadow: 0 28px 64px -12px rgba(2, 6, 23, 0.55)`.
  - **Inner Core:** `border-radius: 26px`, `background: rgba(15, 23, 42, 0.76)` (dark glass mode) or `rgba(255, 255, 255, 0.88)` (daylight frosted mode), `box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.25)`.
- **Micro-Interactions Inside Cards:**
  - **Typewriter Slicing:** Slice strings deterministically by frame progress (`text.slice(0, Math.floor(len * u))`) with a glowing caret `|`.
  - **Animated Vector Cursor:** Smooth cubic-bezier cursor trajectory (`<svg>` pointer) moving from source text (`Ctrl+C` ripple) to target table cell (`Ctrl+V` highlight).
  - **Animated Data Extraction Stream:** Glowing SVG connector lines (`stroke-dasharray`) linking extracted entities (Customer Name, Product, Quantity) into structured table rows and KPI summary cards.

### Layer 3 — Kinetic HUD & Word-Highlighted Karaoke Captions (`z-index: 20`)
- **Top Floating Island Header (`y = 52px`):**
  - Concentric pill badge with glowing status dot + Chapter title (`CẢNH 1 • NGÀY NÀO CŨNG VẬY`).
- **On-Screen Key Takeaway Pill (`y = 820px`):**
  - Floating glass banner displaying the script's exact *"Chữ trên màn hình"*, with progressive step illumination (`Nhận thông tin → Ghi vào bảng → Tổng hợp`).
- **Bottom Karaoke Subtitle Pill (`y = 1640..1830px`):**
  - Frosted dark glass pill (`rgba(9, 13, 24, 0.82)`, `backdrop-filter: blur(20px)`) with 2 balanced lines of Vietnamese text (`38px ExtraBold`), where active keywords scale slightly (`1.04x`) and glow in warm Amber (`#FACC15`) or Sky Emerald (`#38BDF8`).

---

## 3. Deterministic Chromium GPU Render Pipeline

To render 30–60 FPS video rapidly without frame drops:
1. Build a single self-contained HTML5 studio file (`studio_renderer.html`) exposing `window.renderAtTime(t)`.
2. Preload all 6 scene images as local `file:///` or base64 data URLs so Chromium needs zero network requests per frame.
3. Use Python `multiprocessing` (e.g., 4 parallel Playwright Chromium instances rendering disjoint frame chunks `[0..510]`, `[510..1020]`, `[1020..1530]`, `[1530..2040]`) and concatenate/mux with the master WAV soundtrack via FFmpeg `libx264 -crf 15 -pix_fmt yuv420p`.
4. Always inspect rendered preview frames with `read_file` to verify typography, glass contrast, and safe margins before delivering.
