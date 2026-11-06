# Từ Điển Thông Số Chuyển Động, Bảng Màu & Mẫu Code (`world_class_kinetic_patterns.md`)

Tài liệu tham chiếu chuyên sâu dành cho skill `kinetic-ui-launch-director`, tổng hợp các thông số chuẩn từ 5 trường phái Motion Design hàng đầu: **Nexo, Antigravity 2.0, Linear, Raycast, Apple Don't Blink**.

---

## 1. Bảng Màu Quang Phổ Thương Hiệu (Brand Light Spectrums)

### 1.1. Bảng màu `Antigravity / Nexo Quantum Spectrum` (Mặc định)
| Thành phần | Mã HEX | RGB Tuple | Vai trò trong khung hình |
| :--- | :--- | :--- | :--- |
| **Obsidian Deep Space** | `#040711` | `(4, 7, 17)` | Nền không gian sâu giúp ánh sáng Additive Glow nổi khối tối đa |
| **Nebula Core Blue** | `#0E5CAD` | `(14, 92, 173)` | Quầng sáng radial trung tâm phía đáy khung hình |
| **Quantum Cyan** | `#00F0FF` | `(0, 240, 255)` | Tia năng lượng, sóng xung kích, viền chọn chính và chữ `Code` |
| **Aurora Emerald** | `#34D399` | `(52, 211, 153)` | Luồng sao chổi tốc độ, huy hiệu `[Fast]` và chữ `Build` |
| **Solar Gold** | `#FACC15` | `(250, 204, 21)` | Đỉnh vòm logo, sao chổi mở đầu và nửa trên chữ `2.0` |
| **Electric Violet** | `#A855F7` | `(168, 85, 247)` | Vành nhật thực ngoài, sao chổi số 7 và quầng sáng kết màn |

### 1.2. Bảng màu `Linear Midnight Titanium`
- **Background:** `#08090A` $\rightarrow$ `#121417`
- **Card Surface:** `rgba(18, 20, 24, 0.88)` với viền `1px` `#272A30`
- **Primary Glow:** Indigo-Violet `#5E6AD2` kết hợp Ice White `#F4F5F8`

### 1.3. Bảng màu `Raycast Crimson-Sunset`
- **Background:** `#09060C` $\rightarrow$ `#1E0B18`
- **Primary Glow:** Coral Red `#FF6363` $\rightarrow$ Amber Gold `#FFAF40`

---

## 2. Thông Số Toán Học Cho Đường Cong & Vật Lý

### 2.1. Hằng số Easing Chuẩn 60FPS
- **`ease_out_expo` (Hãm phanh camera gấp ở Hồi 1):**
  $$f(x) = 1 - 2^{-10x}$$
- **`ease_in_out_cubic` (Quỹ đạo bay sao chổi & Whip-Pan Camera ở Hồi 2–3):**
  $$f(x) = \begin{cases} 4x^3 & \text{nếu } x < 0.5 \\ 1 - \frac{(-2x + 2)^3}{2} & \text{nếu } x \ge 0.5 \end{cases}$$
- **Dao động lò xo tắt dần (Underdamped Spring cho mặt kính):**
  $$\Delta y(t) = A \cdot e^{-6.5 t} \sin(26.0 t)$$

### 2.2. Cấu hình `spring()` tương đương trong Remotion (React/TypeScript)
```tsx
// 1. Snappy UI Card / Command Palette Pop (Apple / Raycast style)
const snappySpring = {
  damping: 14,
  mass: 0.55,
  stiffness: 190,
};

// 2. Heavy Glass Impact Recoil (Nexo / Antigravity style)
const glassImpactSpring = {
  damping: 9,
  mass: 0.9,
  stiffness: 160,
};

// 3. Smooth Camera Macro Whip-Pan (2.4x Zoom)
const cameraWhipSpring = {
  damping: 18,
  mass: 0.8,
  stiffness: 140,
};
```

---

## 3. Khung Kịch Bản Chuẩn Theo Thời Lượng

### 3.1. Cấu trúc 12 Giây (`720 frames` — Chuẩn Launch Teaser / Social Hero)
- `0.0s – 1.5s` (`Frames 0–90`): **Quantum Hook & Brand Reveal** (Vành ánh sáng + Dolly-in tiêu đề).
- `1.5s – 3.9s` (`Frames 90–234`): **Particle/Comet Morphing & Pre-Locked Prompt** (Tiêu đề tách thành $N$ sao chổi đúc thành câu lệnh + mở thanh công cụ).
- `4.0s – 6.0s` (`Frames 240–360`): **Macro Camera Inspection** (Phóng đại `2.4x` vào bảng cấu hình, lướt chọn tính năng cao cấp nhất).
- `6.0s – 8.0s` (`Frames 360–480`): **Action Launch & Laser Crystallization** (Nén nút gửi $\rightarrow$ phóng tên lửa ánh sáng $\rightarrow$ quét tia laser khắc văn bản).
- `8.0s – 12.0s` (`Frames 480–720`): **Singularity Implosion & 3-Beat Finale** (Thu xoáy vào vòng tròn tâm điểm $\rightarrow$ nổ bung 3 nhịp từ khóa thương hiệu).

### 3.2. Cấu trúc 30–45 Giây (Chuẩn Full Product Launch Film)
- `00s – 05s`: **Pattern Interrupt Kinetic Burst** (Câu hỏi hoặc nỗi đau lớn nhất phóng từ không gian sâu, tách chữ đàn hồi).
- `05s – 15s`: **Text-to-UI Origami Morph** (Khung chữ giãn rộng biến thành cửa sổ ứng dụng chính).
- `15s – 30s`: **Continuous One-Take Camera Tour** (Camera lướt liên hoàn qua 3 tính năng trụ cột bằng Match-Cut và đường dẫn ánh sáng).
- `30s – 40s`: **Speed & Scale Payoff** (Góc nhìn toàn cảnh hệ sinh thái + hiệu ứng thác dữ liệu thành công).
- `40s – 45s`: **Singularity Collapse & 3-Beat Sign-off** (Hội tụ về biểu tượng và thông điệp kết).
