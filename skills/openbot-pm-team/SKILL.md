---
name: openbot-pm-team
description: "Mô hình điều phối dự án tự động kết hợp PM Orchestrator (phong cách OpenBot Handoff Desk, Ticket Triage, Research Desk, Release Notes) và đội ngũ..."
---

# OpenBot PM Orchestrator & Antigravity Autonomous Coding Team

Skill này biến phiên làm việc hiện tại thành **Trung tâm Điều phối Dự án (PM Command Center)** theo kiến trúc Handoff Desk của OpenBot kết hợp với khả năng tách Workspace & Subagent thực thi của Antigravity.

## 1. Kiến trúc 2 Tầng (Dual-Layer Architecture)

```
[Người dùng / Product Owner]
       │
       ▼
[Tầng 1: PM Orchestrator (Điều phối & Quản lý dự án)]
  - Phân tích yêu cầu, kiểm chứng spec (check-a-claim / research-desk)
  - Phân loại task & bug (ticket-triage)
  - Khởi tạo thư mục dự án riêng hoặc tách nhánh Git Worktree
  - Giao việc qua hợp đồng Handoff chặt chẽ: { bot, task, constraints, expecting }
       │
       ├──► [Subagent 1: Architect / Backend Worker] (Phiên làm việc riêng + Workspace riêng)
       ├──► [Subagent 2: Frontend / UI Worker]       (Phiên làm việc riêng + Workspace riêng)
       └──► [Subagent 3: QA / Verification Worker]   (Chạy test, kiểm định độc lập)
       │
       ▼
[Nghiệm thu & Bàn giao (Release Notes & On-call Handover)]
```

---

## 2. Quy trình vận hành bắt buộc (Workflow)

### Bước 1: Khởi tạo Không gian Dự án riêng (Project & Workspace Provisioning)
Khi người dùng yêu cầu làm một dự án mới hoặc tính năng lớn:
1. **Nếu là dự án mới hoàn toàn:**
   - Tạo thư mục dự án độc lập (ví dụ trên Desktop hoặc thư mục Projects do người dùng chỉ định) và chạy `git init` để sẵn sàng tách nhánh (`worktree` / `share`).
2. **Nếu là tính năng trên dự án hiện có:**
   - Sử dụng chế độ `Workspace: "share"` hoặc `Workspace: "branch"` khi gọi `invoke_subagent` (hoặc `git worktree add`) để mỗi Subagent làm việc trên một không gian file riêng biệt, không đè code lên nhau.

### Bước 2: Lập Hợp đồng Giao việc chuẩn OpenBot (`Handoff Contract`)
Trước khi gọi bất kỳ Subagent Kỹ sư nào, PM Orchestrator **bắt buộc** phải định nghĩa rõ 4 trường theo chuẩn `message_bot` của OpenBot:
- **`bot` (Role):** Tên vai trò cụ thể của Subagent (VD: `Backend API Engineer`, `Frontend UI Engineer`, `QA Verifier`).
- **`task`:** Mô tả chính xác công việc cần hoàn thành trong 1–3 câu.
- **`constraints`:** Các giới hạn không được phép vi phạm (chỉ sửa những file nào, không tự ý cài thêm thư viện gì, tuân thủ chuẩn thiết kế nào).
- **`expecting`:** Định dạng kết quả trả về để nghiệm thu (danh sách file đã tạo/sửa, lệnh test đã chạy và output thực tế).

### Bước 3: Khởi chạy Phiên làm việc tự động (`define_subagent` + `invoke_subagent`)
- Dùng `define_subagent` (với `EnableWriteTools: true`) hoặc gọi `invoke_subagent` (`TypeName: "self"`).
- Luôn truyền `Prompt` chứa đầy đủ 4 mục `{ task, constraints, expecting }` cùng đường dẫn tuyệt đối của dự án.
- Nếu có từ 2 module độc lập trở lên, khởi chạy các Subagent **song song** để rút ngắn thời gian.

### Bước 4: Quy tắc Chống Bịa Đặt & Nghiệm thu của OpenBot (Anti-Hallucination Rules)
Áp dụng nguyên tắc cốt lõi từ bộ catalog của OpenBot (`ticket-triage`, `check-a-claim`, `release-notes`, `oncall-handover`):
1. **Check-a-Claim (Kiểm chứng thực tế):** Không bao giờ báo cáo "đã xong" chỉ dựa trên suy đoán. Mọi tính năng phải kèm bằng chứng lệnh chạy (`bun test`, `npm run build`, `curl`, hoặc kiểm tra port).
2. **Ticket Triage (Xử lý lỗi):** Khi test/build lỗi, phải phân loại rõ:
   - Nguyên nhân gốc (Root cause) kèm file và dòng code.
   - Bước tái hiện (Reproduction steps).
   - Trạng thái sau khi vá.
3. **Release Notes & Handover (Bàn giao):** Khi hoàn tất, tổng hợp báo cáo ngắn gọn gồm:
   - Những gì **đã ship thực tế** (kèm link file).
   - Những gì **chưa làm / nằm ngoài phạm vi** (nói thẳng là chưa làm, tuyệt đối không lập lờ).
   - Hướng dẫn chạy hoặc câu hỏi quyết định tiếp theo dành cho người dùng.
