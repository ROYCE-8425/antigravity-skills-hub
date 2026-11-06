---
name: tieuchuanbaocao
description: "Quy chuẩn và ràng buộc bắt buộc khi soạn thảo báo cáo đồ án Quản lý dự án CNTT cho hệ thống CarClean CRM (kích hoạt khi người dùng gọi /tieuchuanbaocao..."
---

# QLDA Report Constraints (`tieuchuanbaocao`): Quy Chuẩn Soạn Thảo Đồ Án CarClean CRM

Skill này đóng gói toàn bộ các quy chuẩn định dạng, phong cách hành văn và ràng buộc nghiệp vụ bắt buộc được thống nhất xuyên suốt quá trình thực hiện đồ án môn học **Quản lý dự án CNTT** (Khoa CNTT - HUTECH, đề tài: **CarClean CRM**, GVHD: ThS. Võ Phạm Thành Luân, Sinh viên: Ngô Nhật Chấn Phong - MSSV: 2380614867).

Mọi chương nội dung từ Chương 1 đến Chương 10 khi sinh mã hoặc xuất bản file Word (`.docx`) đều **bắt buộc tuân thủ 100% các nguyên tắc dưới đây**.

---

## 1. Ràng Buộc Định Dạng Văn Bản (Typography & Page Setup)

Tuân thủ nghiêm ngặt Hướng dẫn viết Đồ án Cơ sở / Đồ án Tổng hợp của Khoa CNTT - HUTECH:

- **Khổ giấy & Căn lề chuẩn A4:**
  - Khổ giấy: A4 (210 mm x 297 mm), in một mặt.
  - Lề trên (Top): `2.0 cm`
  - Lề dưới (Bottom): `2.5 cm`
  - Lề trái (Left): `3.0 cm` (phục vụ đóng gáy bìa)
  - Lề phải (Right): `2.0 cm`
- **Dãn dòng & Phân đoạn:**
  - Dãn dòng (Line spacing): `1.5 lines`.
  - Căn lề đoạn văn bản (Alignment): Căn đều hai bên (`WD_ALIGN_PARAGRAPH.JUSTIFY`).
  - Dãn đoạn (Spacing): `space_before = Pt(0)`, `space_after = Pt(3)` đến `Pt(4)`.
  - Thụt đầu dòng đoạn văn xuôi thông thường (`first_line_indent`): `1.27 cm` (0.5 inch).
- **Phông chữ chuẩn (Times New Roman):**
  - Toàn bộ nội dung thân bài: Times New Roman, cỡ chữ `13pt`, chữ thường.
  - Tiêu đề Chương (Chương 1, Chương 2...): Times New Roman, cỡ chữ `16pt`, **IN ĐẬM**.
  - Tiêu đề Mục (cấp 1, ví dụ 1.1, 1.2, 2.1...): Times New Roman, cỡ chữ `14pt`, **IN ĐẬM**.
  - Tiêu đề Tiểu mục (cấp 2, ví dụ 1.1.1, 1.1.2...): Times New Roman, cỡ chữ `14pt`, *In nghiêng*.
  - Tiêu đề Tiểu mục con (cấp 3, ví dụ 1.1.1.1... nếu có): Times New Roman, cỡ chữ `13pt`, <u>Gạch chân</u>. Không đánh số dưới mức tiểu mục con.
  - Đánh số mục: Chỉ dùng chữ số tự nhiên dạng phân cấp (1.1, 1.1.1), **TUYỆT ĐỐI KHÔNG dùng số La Mã** (I, II, III...).
- **Đánh số trang:**
  - Đánh số trang tự động ở **chính giữa lề dưới** (Footer Center), bắt đầu đánh số từ Chương 1 bằng trường XML `PAGE`.

---

## 2. Quy Tắc Gạch Đầu Dòng & Căn Lề Khi Xuống Dòng

Đây là quy tắc đặc thù người dùng đã hiệu chỉnh trực tiếp trên giao diện văn bản:

- **Ký tự danh sách:**
  - Sử dụng gạch đầu dòng `- ` (gạch ngang kèm khoảng trắng).
  - **Không sử dụng** dấu chấm tròn đen (`•`) hay các ký tự bullet đồ họa khác.
- **TUYỆT ĐỐI KHÔNG IN ĐẬM TRONG DANH SÁCH:**
  - Trong các mục gạch đầu dòng, **toàn bộ văn bản phải là chữ thường** (`bold=False`).
  - **Cấm hoàn toàn** việc in đậm từ khóa đầu câu (như `**Tên phân hệ:**`, `**Chức năng:**`...). Viết liền mạch theo lối văn xuôi học thuật, rõ ràng, gãy gọn.
- **TUYỆT ĐỐI KHÔNG THỤT LỀ KHI XUỐNG DÒNG (Không dùng Hanging Indent):**
  - Khi câu dài rớt xuống dòng thứ 2 trở đi, chữ phải **chạy thẳng hàng sát lề trái với dấu gạch ngang đầu dòng**, không được thụt lùi vào trong.
  - Cấu hình python-docx chuẩn:
    ```python
    p.paragraph_format.left_indent = Inches(0)
    p.paragraph_format.first_line_indent = Inches(0)
    ```
- **QUY TẮC LOẠI TRỪ GIỮA GẠCH ĐẦU DÒNG VÀ ĐÁNH SỐ (1 TRONG 2, KHÔNG CÓ CẢ 2):**
  - Khi trình bày danh sách liệt kê, **chỉ được chọn hoặc dùng gạch đầu dòng (`- `), HOẶC dùng đánh số thứ tự (`1. `, `2. ` hoặc `1.1 `, `1.2 `)**.
  - **TUYỆT ĐỐI KHÔNG ĐƯỢC DÙNG CẢ HAI ĐỒNG THỜI** trên cùng một mục/dòng. Cấm hoàn toàn các cấu trúc lai tạp như:
    - CẤM: `- 1.1 Quản lý dự án...`
    - CẤM: `- 1. Khởi tạo...`
    - CẤM: `- a. Giai đoạn...`
    - CẤM: `• 1.1 ...`
  - Nếu đã sử dụng dấu gạch đầu dòng `- ` ở đầu thì phía sau lập tức là chữ cái hoa bắt đầu câu (ví dụ: `- Quản lý dự án...`, `- Phân tích và thiết kế...`).
  - Ngược lại, nếu chọn đánh số thứ tự phân cấp thì viết trực tiếp số thứ tự đầu dòng mà không gắn thêm ký tự gạch đầu dòng phía trước.

---

## 3. Ràng Buộc Từ Ngữ, Ký Tự Cấm & Đơn Vị Tiền Tệ

- **ĐƠN VỊ TIỀN TỆ THỐNG NHẤT: BẮT BUỘC DÙNG VNĐ (TUYỆT ĐỐI CẤM DÙNG USD):**
  - Trong toàn bộ các chương báo cáo đồ án CarClean CRM (Chương 1 đến Chương 10), bảng biểu, phân tích chi phí, nén lịch (Crashing), ngân sách dự án và chỉ số tài chính, **bắt buộc sử dụng duy nhất đơn vị tiền tệ là VNĐ (Việt Nam Đồng)**.
  - **Tuyệt đối không sử dụng đơn vị tiền tệ USD**.
  - Định dạng hiển thị số tiền: Sử dụng dấu chấm phân cách hàng nghìn (ví dụ: `8.000.000 VNĐ`, `15.000.000 VNĐ`, `1.200.000 VNĐ/ngày`, `4.200.000 VNĐ`).
- **CẤM KÝ TỰ `&`:**
  - **Tuyệt đối không sử dụng ký tự `&`** trong toàn bộ báo cáo (bao gồm cả thân bài, danh sách, tiêu đề và trong các ô bảng biểu).
  - Luôn luôn viết đầy đủ bằng từ tiếng Việt: **`và`** (hoặc `cùng với`).
- **CHUẨN HÓA TÊN VAI TRÒ KỸ THUẬT:**
  - Sử dụng danh xưng: **Kỹ sư** hoặc **Engineer**.
  - **Tuyệt đối không dùng:** `Tech`, `Kỹ thuật viên` hay `KTV`.
- **CHUẨN HÓA DANH XƯNG NHÀ TÀI TRỢ (SPONSOR):**
  - Luôn sử dụng chức danh ngắn gọn: **Giám đốc**.
  - **Tuyệt đối không dùng:** `Ban Giám đốc Trung tâm Dịch vụ Chăm sóc Ô tô CarClean` hay `Ban Giám đốc`.
- **PHONG CÁCH DIỄN ĐẠT:**
  - Ngắn gọn, súc tích, đi thẳng vào ý chính, phản ánh trung thực mã nguồn kỹ thuật.
  - Không tạo sinh nội dung văn mẫu dài dòng, sáo rỗng hoặc lan man.

---

## 4. Quy Tắc Bảng Biểu & Hình Vẽ (Đơn Sắc, Không Màu, Không Tô Xám, Không In Đậm)

- **Vị trí tiêu đề:**
  - **Bảng biểu (Table):** Tiêu đề nằm ở **PHÍA TRÊN** bảng, căn giữa, định dạng *In đậm nghiêng* (ví dụ: *Bảng 1.1: Bảng tổng hợp công nghệ phần mềm và hạ tầng triển khai*).
  - **Hình vẽ / Sơ đồ (Figure):** Tiêu đề nằm ở **PHÍA DƯỚI** hình, căn giữa, định dạng *In đậm nghiêng* (ví dụ: *Hình 2.1: Sơ đồ cấu trúc phân rã công việc (WBS) tổng thể hệ thống CarClean CRM*).
- **Quy tắc đánh số:**
  - Số bảng/hình phải gắn liền với số chương (Chương 1 là Bảng 1.1, Hình 1.1; Chương 2 là Bảng 2.1, Hình 2.1...).
- **QUY CHUẨN CHIỀU RỘNG BẢNG BIỂU ĐỒNG NHẤT 100% (KHÔNG CÓ BẢNG TO BẢNG NHỎ):**
  - Mọi bảng biểu trong toàn bộ các chương báo cáo (Chương 1 đến Chương 10) **bắt buộc phải có tổng chiều rộng bằng nhau tuyệt đối**, vừa khít 100% với bề rộng vùng soạn thảo giữa hai lề trang A4:
    $$\text{Chiều rộng bảng} = \text{Khổ A4 (21.0 cm)} - \text{Lề trái (3.0 cm)} - \text{Lề phải (2.0 cm)} = \mathbf{16.0\text{ cm}} \quad (\approx 6.30\text{ inches} = 9071\text{ dxa})$$
  - **Tuyệt đối không để xảy ra tình trạng bảng to bảng nhỏ** (bảng bị hẹp thụt vào trong để hở lề phải, bảng phình to thò tràn ra ngoài lề trang). Mọi bảng biểu khi cuộn trang phải có cạnh viền bên trái và cạnh viền bên phải **thẳng tắp một hàng** với nhau và thẳng hàng với lề văn bản của trang.
  - Tổng chiều rộng các cột (`sum(col_widths)`) của mọi bảng luôn luôn chuẩn hóa về đúng `16.0 cm` (`Inches(6.30)` hay `9071 dxa`).
  - Trong cấu hình XML của bảng, luôn thiết lập cố định `<w:tblW w:w="9071" w:type="dxa"/>` (thay thế thẻ `auto` mặc định của python-docx), `<w:tblLayout w:type="fixed"/>`, `<w:tblGrid>` chứa đúng tổng các `gridCol` bằng 9071 dxa, và từng ô trong hàng đều có `<w:tcW w:type="dxa"/>` tương ứng.
- **ĐỊNH DẠNG BẢNG BIỂU ĐƠN GIẢN (SIMPLE TABLE - BẮT BUỘC):**
  - **Đơn sắc không màu và không tô xám:** Tuyệt đối không tô bất kỳ màu nền nào, không tô xám (`shading = 0`, không append thẻ `<w:shd>`) cho bất kỳ ô nào trong bảng (cả dòng tiêu đề và dòng dữ liệu). Nền bảng 100% màu trắng nguyên bản.
  - **Không phân màu tiêu đề:** Hàng tiêu đề không được dùng màu nền hay sắc độ xám để phân biệt.
  - **Tiêu đề bảng không in đậm:** Chữ trong toàn bộ bảng bao gồm cả hàng tiêu đề đều sử dụng kiểu chữ thường (`bold=False`), kích thước 9.5pt - 11pt.
  - **Lưới kẻ viền đen đơn giản (Simple Grid):** Toàn bộ các đường viền bao quanh (top, bottom, left, right) và đường kẻ phân cách giữa các ô (insideH, insideV) đều dùng nét kẻ đơn màu đen chuẩn (`#000000`, độ dày `1/2 pt`, tương đương `sz="4"` trong Word XML).
  - Cấu hình python-docx mẫu chuẩn mực (tự động chuẩn hóa mọi bảng về đúng 16.0 cm / 9071 dxa):
    ```python
    TOTAL_TABLE_WIDTH_DXA = 9071 # 16.0 cm (21.0cm - 3.0cm - 2.0cm)

    def style_table(table, col_widths, headers, rows_data):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        tblPr = table._tbl.tblPr

        # Cố định tổng chiều rộng bảng thành 9071 dxa
        tblW = tblPr.find(qn('w:tblW'))
        if tblW is not None:
            tblW.set(qn('w:w'), str(TOTAL_TABLE_WIDTH_DXA))
            tblW.set(qn('w:type'), 'dxa')
        else:
            tblPr.insert(0, parse_xml(f'<w:tblW {nsdecls("w")} w:w="{TOTAL_TABLE_WIDTH_DXA}" w:type="dxa"/>'))

        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            f'<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)
        tblPr.append(parse_xml(f'<w:tblLayout {nsdecls("w")} w:type="fixed"/>'))
        tblPr.append(parse_xml(
            f'<w:tblCellMar {nsdecls("w")}>'
            f'<w:top w:w="50" w:type="dxa"/>'
            f'<w:bottom w:w="50" w:type="dxa"/>'
            f'<w:left w:w="40" w:type="dxa"/>'
            f'<w:right w:w="40" w:type="dxa"/>'
            f'</w:tblCellMar>'
        ))

        # Tự động chuẩn hóa tỷ lệ cột để tổng luôn luôn = 9071 dxa
        raw_widths = [getattr(w, 'inches', float(w)) for w in col_widths]
        total_raw = sum(raw_widths)
        col_dxas = [int(round(TOTAL_TABLE_WIDTH_DXA * (w / total_raw))) for w in raw_widths]
        diff = TOTAL_TABLE_WIDTH_DXA - sum(col_dxas)
        col_dxas[-1] += diff

        # Thiết lập tblGrid
        existing_grid = table._tbl.find(qn('w:tblGrid'))
        if existing_grid is not None:
            table._tbl.remove(existing_grid)
        tblGrid = parse_xml(f'<w:tblGrid {nsdecls("w")}/>')
        for w_dxa in col_dxas:
            tblGrid.append(parse_xml(f'<w:gridCol {nsdecls("w")} w:w="{w_dxa}"/>'))
        table._tbl.insert(table._tbl.index(tblPr) + 1, tblGrid)

        # Cỡ chữ theo số cột: >=10 cột dùng 9.5pt, >=7 cột dùng 10pt, còn lại 11pt
        font_sz = 11
        if len(headers) >= 10:
            font_sz = 9.5
        elif len(headers) >= 7:
            font_sz = 10

        # Áp dụng cho từng ô: cell.width, tcW dxa, không đổ bóng, bold=False
        for r_idx, row in enumerate(table.rows):
            for c_idx, cell in enumerate(row.cells):
                w_dxa = col_dxas[c_idx]
                cell.width = Inches(w_dxa / 1440.0)
                tcPr = cell._tc.get_or_add_tcPr()
                tcW = tcPr.find(qn('w:tcW'))
                if tcW is not None:
                    tcW.set(qn('w:w'), str(w_dxa))
                    tcW.set(qn('w:type'), 'dxa')
                else:
                    tcPr.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{w_dxa}" w:type="dxa"/>'))
    ```
- **HÌNH ẢNH DẠNG BIỂU ĐỒ, SƠ ĐỒ (DIAGRAMS / TREE CHARTS / FLOWCHARTS):**
  - **Hoàn toàn đơn sắc (Monochrome - đen trắng):** Nền hình ảnh màu trắng tinh khiết (`#FFFFFF`), các khối hộp có nền trắng (`fill="#FFFFFF"`), viền đen đơn nét (`outline="#000000"`).
  - **Đường nét liên kết:** Các đường nối, trục ngang/dọc, mũi tên đều dùng nét đen (`fill="#000000"`).
  - **Tuyệt đối không dùng màu sắc:** Không thêm bất kỳ màu nào (không dùng xanh dương, đỏ, vàng...).
  - **Tuyệt đối không tô xám (No Gray Shading / Fills):** Không dùng màu xám làm nền hộp hay nền khối.
  - **Tuyệt đối không in đậm chữ (No bold text):** Toàn bộ chữ trong sơ đồ, tiêu đề sơ đồ và nhãn các khối hộp bắt buộc dùng kiểu chữ thường (Regular weight, không dùng Bold font).
- **KHÔNG LẬP BẢNG CHO YÊU CẦU CHỨC NĂNG VÀ PHI CHỨC NĂNG:**
  - Yêu cầu chức năng và yêu cầu phi chức năng phải được trình bày dưới dạng **danh sách liệt kê gạch đầu dòng (`- `)** chi tiết, không lập bảng biểu tổng hợp cho 2 mục này.

---

## 5. Ranh Giới Nghiệp Vụ & Kỹ Thuật Hệ Thống CarClean CRM

Mọi phân tích yêu cầu, thiết kế kiến trúc và kế hoạch quản lý dự án phải bám sát chính xác hiện trạng mã nguồn thực tế tại `/Users/fongfog/Documents/QLDA_23DTHD3/carclean_studiovs`:

### A. Những gì ĐÃ CÓ trong phạm vi dự án (In-Scope):
1. **Phân hệ Quản lý tài khoản (RBAC):** 4 nhóm vai trò (Admin, Sale, Engineer, Customer); xác thực cookie bảo mật; bắt buộc đổi mật khẩu lần đầu (`MustChangePassword`); vô hiệu hóa phiên tức thì bằng mã `AuthVersion`.
2. **Phân hệ Danh mục và Kho vật tư:** Quản lý sản phẩm, dịch vụ theo loại xe; nhập kho (`StockImport`); biến động tồn kho (`StockMovements`); kiểm soát giao dịch cơ sở dữ liệu (Database Transaction) cập nhật số dư nguyên tử tại `StockService` nhằm **chống âm kho khi nhiều nhân sự xuất bán đồng thời**.
3. **Phân hệ Tiếp nhận và Kiểm tra xe:** Check-in xe vào xưởng (`ServiceVisit`), ghi nhận yêu cầu khách hàng, lập phiếu kiểm tra tình trạng xe (`VehicleInspection`) theo danh mục kiểm tra kỹ thuật (Checklist) và ghi chú thực tế của kỹ sư.
4. **Phân hệ Báo giá và Điều phối thi công:** Kỹ sư lập đề xuất kỹ thuật (`Proposal`), tư vấn viên tạo báo giá chi tiết (`Quote`), chốt đơn hàng (`Order`), phân công kỹ sư và cập nhật tiến độ thi công từng công đoạn theo thời gian thực (`OrderLineProgress`).
5. **Phân hệ Thanh toán và Hóa đơn:** Tạo hóa đơn (`Invoice`), ghi nhận thanh toán trực tiếp tại quầy bằng tiền mặt hoặc chuyển khoản ngân hàng đối soát thủ công, áp dụng mã voucher giảm giá, tích lũy điểm thưởng thành viên, xuất báo cáo doanh thu ra Excel bằng thư viện `ClosedXML`.
6. **Phân hệ Bảo hành điện tử (e-Warranty):** Kích hoạt tự động khi đơn hàng hoàn tất, tạo tem mã QR tra cứu nhanh, quản lý tiếp nhận khiếu nại (`Complaints`).
7. **Phân hệ Cổng thông tin công khai:** Tra cứu lịch sử chăm sóc xe và hạn bảo hành bằng biển số xe hoặc số điện thoại.
8. **Hạ tầng & Bảo mật Internet:** Đã đưa lên mạng Internet thực tế trên máy chủ Cloud VPS Linux (Ubuntu 22.04), đóng gói Docker và Docker Compose, Kestrel chạy sau NGINX Reverse Proxy, mã hóa SSL/TLS qua HTTPS; cài đặt bảo mật Forwarded Headers chống IP spoofing, Rate Limiting phân tầng, Global Antiforgery Token và header `X-CSRF-TOKEN`, mã hóa BCrypt, HTTP Security Headers chuẩn OWASP.

### B. Những gì ĐÃ CHỐT LOẠI BỎ khỏi phạm vi đề tài (Out-of-Scope / Giới hạn đề tài):
1. **KHÔNG CÓ TÍNH NĂNG ĐẶT LỊCH HẸN TRỰC TUYẾN (BOOKING):** Quy trình tiếp nhận xe thống nhất thực hiện trực tiếp tại xưởng khi khách hàng đưa xe đến.
2. **KHÔNG CÓ TÍNH NĂNG CHỤP ẢNH ĐÓNG DẤU MỜ (WATERMARK):** Không đóng dấu mờ thời gian thực hay biển số xe trên ảnh; không dùng khái niệm "kiểm tra ngoại quan", việc khảo sát tình trạng xe chỉ tập trung vào biểu mẫu danh mục kỹ thuật và ghi chú nhận định thực tế của kỹ sư.
3. **CHƯA CHẠY SEO:** Không triển khai tối ưu hóa công cụ tìm kiếm, chưa cấu hình thẻ meta động chi tiết cho từng dịch vụ, chưa tích hợp Schema JSON-LD và chưa xây dựng mạng lưới liên kết ngoài.
4. **KHÔNG TÍCH HỢP CỔNG THANH TOÁN TỰ ĐỘNG BÊN THỨ BA:** Không tích hợp VNPAY, MoMo hay cổng thanh toán thẻ tự động; chỉ ghi nhận thanh toán tại quầy bằng tiền mặt hoặc chuyển khoản qua đối soát thủ công.
5. **KHÔNG PHÁT TRIỂN ỨNG DỤNG DI ĐỘNG (MOBILE APP):** Không có app iOS/Android native, người dùng truy cập qua giao diện web tương thích đa thiết bị (Responsive Web).
6. **CHỈ TẬP TRUNG DETAILING:** Không bao gồm sửa chữa cơ khí nặng, bảo dưỡng đại tu động cơ, khung gầm hay cứu hộ giao thông.

---

## 6. Nội Dung Cố Định Phần "Ý Nghĩa Khoa Học" (Mục 1.1.2)

Khi soạn thảo mục Ý nghĩa khoa học, luôn sử dụng nguyên văn 3 nội dung đã được người dùng phê duyệt:
- Áp dụng lý thuyết vào thực tiễn: Đề tài này giúp sinh viên áp dụng các lý thuyết quản lý dự án đã học, từ lập kế hoạch đến theo dõi và đánh giá, vào một dự án cụ thể. Sinh viên có cơ hội thực hành các khái niệm như phạm vi dự án, thời gian, ngân sách và chất lượng.
- Khám phá công nghệ và phương pháp quản lý hiện đại: Qua việc phát triển website, sinh viên sẽ tiếp cận với các công nghệ mới và các phương pháp quản lý, giúp nâng cao kiến thức và kỹ năng về công nghệ thông tin và quản lý dự án.
- Phân tích và đánh giá hệ thống: Đề tài khuyến khích sinh viên thực hiện các nghiên cứu về nhu cầu người dùng và đánh giá hiệu quả của hệ thống, từ đó rút ra bài học và đề xuất giải pháp cải tiến cho các dự án sau.

---

## 7. Cấu Trúc Toàn Bộ Đồ Án (10 Chương PMBOK)

Đồ án được cơ cấu theo chuẩn 10 lĩnh vực tri thức quản lý dự án:
- **Chương 1: Tổng quan** (Bối cảnh, ý nghĩa, mục tiêu, phạm vi, yêu cầu hệ thống, kiến trúc triển khai).
- **Chương 2: Quản lý phạm vi dự án** (Project Charter, SOW, phân rã WBS, WBS Dictionary cho 7 phân hệ).
- **Chương 3: Quản lý thời gian dự án** (Danh mục hoạt động, mạng CPM, đường găng, sơ đồ tiến độ Gantt).
- **Chương 4: Quản lý chi phí dự án** (Ước tính chi phí theo mô hình COCOMO, ngân sách phần cứng, phần mềm, nhân công, dự phòng rủi ro).
- **Chương 5: Quản lý chất lượng dự án** (Tiêu chuẩn chất lượng, kế hoạch đảm bảo chất lượng QA, kế hoạch kiểm thử QC).
- **Chương 6: Quản lý nhân sự dự án** (Cơ cấu tổ chức nhóm, ma trận RACI, kế hoạch phân bổ và định biên nhân sự).
- **Chương 7: Quản lý truyền thông dự án** (Kế hoạch giao tiếp các bên liên quan, kênh thông tin, lịch họp, mẫu báo cáo).
- **Chương 8: Quản lý rủi ro dự án** (Nhận diện rủi ro, Risk Register, ma trận rủi ro, kế hoạch ứng phó).
- **Chương 9: Quản lý mua sắm dự án** (Kế hoạch mua sắm Cloud VPS, Domain, SSL, hợp đồng mẫu).
- **Chương 10: Quản lý tích hợp dự án** (Tổng kết, nghiệm thu các gói bàn giao, đánh giá và chuyển giao sản phẩm).

---

## 8. Quy Trình Xuất Bản & Kiểm Định File Word

Khi tạo hoặc cập nhật file Word (`.docx`):
1. Dùng Python script với thư viện `python-docx` để kiểm soát chính xác 100% các thuộc tính định dạng XML.
2. Lưu tệp duy nhất tại một vị trí chính thức:
   - Thư mục nộp bài sinh viên: `2380614867-ngonhatchanphong/`
   - Tuyệt đối không nhân đôi, sao chép hay xuất thêm file ra thư mục gốc dự án.
3. Chạy lệnh kiểm tra tự động trước khi bàn giao:
   - Kiểm tra ký tự `&` = 0 lỗi.
   - Kiểm tra `watermark` / `kiểm tra ngoại quan` = không xuất hiện trong mô tả chức năng.
   - Kiểm tra in đậm (`bold=True`) trong các đoạn gạch đầu dòng (`- `) = 0 lỗi.
   - Kiểm tra thụt lề dòng thứ hai (`left_indent = 0`, `first_line_indent = 0`) trong các mục gạch đầu dòng.
   - Kiểm tra gạch đầu dòng kết hợp đánh số: `assert not re.search(r"^-\s*([0-9]+(\.[0-9]+)*|[a-zA-Z]\.)\s+", text)` = 0 lỗi (không tồn tại `- 1.1`, `- 1.`, v.v.).
   - Kiểm tra bảng biểu: không có bất kỳ thẻ `<w:shd>` nào (không màu mờ, không phân màu tiêu đề), viền đen đơn giản `#000000`, toàn bộ chữ trong bảng không in đậm (`bold=False`).
   - Kiểm tra kích thước bảng biểu: toàn bộ các bảng trong tài liệu phải có `<w:tblW w:w="9071" w:type="dxa"/>` và tổng `gridCol` bằng chính xác `9071 dxa` (16.0 cm), mép viền hai bên trái và phải của các bảng thẳng tắp đều nhau tuyệt đối, không có bảng to phình tràn lề hoặc bảng nhỏ thụt lề.
   - Kiểm tra sơ đồ, biểu đồ: hoàn toàn đơn sắc đen trắng, không chứa pixel màu, không tô xám, toàn bộ chữ trong sơ đồ không in đậm.

---

## 9. Tiêu Chuẩn Nội Dung Chuyên Sâu Chương 5 (Quản Lý Chất Lượng Dự Án)

Được chuẩn hóa từ bộ bài tập thực hành quản trị chất lượng của giảng viên (`1211060327-buimanhtoan/BaiTap5`) và ánh xạ trực tiếp vào kiến trúc hệ thống **CarClean CRM**:

### 9.1. Nền tảng QA/QC, Tiêu chuẩn và Chi phí Chất lượng (COQ)
1. **Phân biệt Đảm bảo chất lượng (`QA`) và Kiểm soát chất lượng (`QC`):**
   - `QA (Quality Assurance)`: Hướng vào **quy trình** để phòng ngừa lỗi ngay từ đầu (`Shift-Left`), bao gồm chuẩn hóa cơ sở dữ liệu đạt dạng chuẩn 3NF và BCNF (48 bảng cơ sở, 9 bảng liên kết), thiết kế máy trạng thái đơn hàng (`OrderStateMachine`) và bảo hành (`WarrantyStateMachine`), áp dụng giao dịch cơ sở dữ liệu nguyên tử (`Database Transaction`) tại `StockService`, chuẩn hóa biểu mẫu kịch bản kiểm thử và ma trận truy vết yêu cầu (`RTM`).
   - `QC (Quality Control)`: Hướng vào **sản phẩm bàn giao** để phát hiện sai lệch trước khi giao cho khách hàng, thông qua tính toán kết quả mong đợi (`Test Oracle`), thực thi 53 kịch bản kiểm thử tự động `xUnit` (`CarClean.Tests`), đối chiếu kết quả thực tế và lập phiếu báo lỗi (`Defect Report`).
2. **Hệ thống chỉ số đo lường và tiêu chuẩn chất lượng:**
   - Phải trình bày đầy đủ công thức toán học, mục tiêu định lượng và phương pháp thu thập dữ liệu cho 6 nhóm tiêu chí: Hiệu suất (thời gian phản hồi trung bình $\le 2$ giây cho 90% yêu cầu, $\le 3$ giây cho 95% yêu cầu), Độ ổn định ($\text{Uptime} \ge 99{,}5\%$, $\text{MTBF} \ge 1.000$ giờ), Tính chính xác nghiệp vụ ($100\%$ đúng công thức tiền cọc, chiết khấu, sổ cái tồn kho và hạn bảo hành), Bảo mật (tỷ lệ xác thực hợp lệ $\ge 98\%$, mã hóa `BCrypt`, kiểm tra `AuthVersion`, `Rate Limiting`, `AutoValidateAntiforgeryToken`), Khả năng bảo trì ($\text{MTTR} < 4$ giờ đối với lỗi nghiêm trọng) và Thân thiện người dùng (hoàn thành thao tác cốt lõi $< 3$ phút, độ hài lòng $\ge 85\%$).
   - Áp dụng 4 bộ tiêu chuẩn quốc tế: `ISO/IEC 25010`, `ISO/IEC 27001`, `ISTQB` và `OWASP Top 10`.
3. **Mô hình Chi phí Chất lượng (`Cost of Quality - COQ`):**
   - Phân tích ngân sách chất lượng theo 2 nhóm lớn và 4 loại chi phí (tính 100% bằng đơn vị **VNĐ** trên Ngân sách gốc $B_0$):
     - **Chi phí phù hợp (`Cost of Conformance`)**: Chi phí phòng ngừa (`Prevention Cost`) và Chi phí thẩm định, đánh giá (`Appraisal Cost`).
     - **Chi phí không phù hợp (`Cost of Non-Conformance`)**: Chi phí sai hỏng nội bộ (`Internal Failure Cost`) và Chi phí sai hỏng bên ngoài (`External Failure Cost`).

### 9.2. Chu Trình 4 Bước Kiểm Soát Chất Lượng Nghiệp Vụ Cốt Lõi
1. **Bước 1 - Xác định cỡ mẫu thống kê và Tính kết quả mong đợi (`Test Oracle`):**
   - Công thức cỡ mẫu kiểm thử theo thống kê: $n = 0{,}25 \times (Z / E)^2$ (với mức tin cậy $95\% \Rightarrow Z = 1{,}96, E = 0{,}05 \Rightarrow n = 385$; mức tin cậy $90\% \Rightarrow Z = 1{,}645, E = 0{,}10 \Rightarrow n = 68$; mức tin cậy $80\% \Rightarrow Z = 1{,}281, E = 0{,}20 \Rightarrow n = 11$).
   - Lập bảng tính `Test Oracle` cho đơn hàng mẫu kết hợp dịch vụ và sản phẩm tại xưởng CarClean CRM theo đúng thứ tự quy tắc nghiệp vụ: tính thành tiền từng dòng (`OrderLines`), tính tiền đặt cọc theo quy tắc `NV-07` ($30\%$ đối với hàng sẵn có trong kho `IsStockReady = true`, $50\%$ đối với hàng phải đặt `IsStockReady = false`), áp dụng chiết khấu hạng thành viên hoặc mã `Voucher` hợp lệ, tính số tiền còn lại phải thu (`PaymentReceipts`), trừ tồn kho nguyên tử một lần duy nhất vào sổ cái `StockMovements` và kích hoạt bảo hành điện tử `WarrantyCoverages` theo quy tắc `NV-13` và `NV-27`.
2. **Bước 2 - Thiết kế Kịch bản Kiểm thử (`Test Case`), Đối chiếu và Lập Phiếu Báo Lỗi (`Defect Report`):**
   - Bảng kịch bản kiểm thử phải có đầy đủ **6 cột chuẩn**: Mã kịch bản (`TC01`..`TC08`), Mã yêu cầu liên kết (`US-...`), Điều kiện ban đầu, Dữ liệu đầu vào, Các bước thực hiện và Kết quả mong đợi định lượng.
   - Bảng đối chiếu kết quả ghi nhận phải phân định rõ trạng thái **Khớp** hoặc **Không khớp** kèm giải thích định lượng.
   - Từ các kịch bản **Không khớp**, lập tối thiểu **02 Phiếu báo lỗi (`GL-01`, `GL-02`)** có đầy đủ 6 thông tin: Tiêu đề lỗi, Kịch bản và dữ liệu đầu vào liên quan, Các bước tái hiện, Kết quả mong đợi đối chiếu Kết quả ghi nhận (ghi rõ độ lệch), Tác hại nghiệp vụ và Mức ưu tiên sửa (`Cao / Vừa / Thấp`), Hướng kiểm tra lại sau khi sửa (`Re-test`).
3. **Bước 3 - Ma trận Truy vết Yêu cầu (`Requirements Traceability Matrix - RTM`):**
   - Lập bảng `RTM` liên kết từng mã yêu cầu nghiệp vụ với các mã `Test Case` và bài kiểm thử tự động trong `CarClean.Tests`, đánh giá mức độ bao phủ và chỉ rõ **điều kiện biên chưa được kiểm tra (`Coverage Gaps`)**, đặc biệt là kịch bản đơn hàng hỗn hợp nhiều danh mục và kịch bản kiểm tra tính lũy đẳng (`IdempotencyKey`) chống trừ tồn kho trùng lặp hoặc kích hoạt bảo hành hai lần.
4. **Bước 4 - Công cụ Thống kê Chất lượng (`Pareto 80/20`, `Control Chart`, `DPMO`, `PDCA`):**
   - **Phân tích Pareto (`80/20`) kết hợp Mức độ nghiêm trọng (`Severity`)**: Sắp xếp các nhóm nguyên nhân lỗi giảm dần theo số lượng, tính tỷ lệ phần trăm và tỷ lệ phần trăm cộng dồn để xác định nhóm nguyên nhân chiếm từ $80\%$ tổng số lỗi trở lên; đồng thời giải thích nguyên tắc không được hoãn sửa các lỗi có mức độ nghiêm trọng cao (`High/Critical Severity` về phân quyền `RBAC`, sai lệch tiền tệ hoặc âm kho) dù tần suất xuất hiện thấp.
   - **Biểu đồ kiểm soát (`Control Chart` $\bar{x} \pm 3s$)**: Theo dõi số lỗi qua 12 tuần kiểm thử, tính trung bình $\bar{x}$, độ lệch chuẩn mẫu $s$, giới hạn kiểm soát trên $\text{UCL} = \bar{x} + 3s$, giới hạn kiểm soát dưới $\text{LCL} = \bar{x} - 3s$ và nhận diện tuần có biến động bất thường vượt ngưỡng $\text{UCL}$.
   - **Chỉ số `DPMO` (*Defects Per Million Opportunities*) và Chu trình `PDCA` (*Plan - Do - Check - Act*)**: Tính tổng cơ hội lỗi, chỉ số `DPMO` trước và sau cải tiến (giảm $75\%$ từ $400$ xuống $100$) và trình bày chu trình `PDCA` kết hợp cải tiến liên tục `Kaizen`.

---

## 10. Tiêu Chuẩn Nội Dung Chuyên Sâu Chương 8 (Quản Lý Rủi Ro Dự Án)

Được chuẩn hóa từ bộ bài tập thực hành quản trị rủi ro của giảng viên (`1211060327-buimanhtoan/BaiTap8`) và đồng bộ 100% với quy chuẩn tiền tệ **VNĐ** của dự án **CarClean CRM**:

### 10.1. Sổ Quản Trị RAID, Cấu Trúc RBS và Phát Biểu Rủi Ro Chuẩn
1. **Phân biệt 4 thực thể trong Sổ `RAID` (`Risks - Assumptions - Issues - Dependencies`):**
   - `Risk (Rủi ro)`: Sự kiện chưa xảy ra ($0\% < P < 100\%$), cần kế hoạch phòng ngừa và dự phòng.
   - `Issue (Vấn đề hiện hữu)`: Sự việc đã hoặc đang xảy ra ($P = 100\%$), cần hành động khắc phục ngay (`Workaround / Corrective Action`).
   - `Assumption (Giả định)`: Điều tạm coi là đúng khi lập kế hoạch nhưng cần xác minh; giả định sai sẽ sinh ra rủi ro.
   - `Dependency (Phụ thuộc)`: Mối phụ thuộc vào hạ tầng máy chủ, thư viện hoặc bên liên quan.
2. **Công thức viết phát biểu rủi ro chuẩn doanh nghiệp (`Cause -> Event -> Impact`):**
   - Mọi mô tả rủi ro phải tách bạch 3 thành phần: **Nguyên nhân gốc rễ (`Cause`)** $\rightarrow$ **Sự kiện rủi ro (`Risk Event`)** $\rightarrow$ **Tác động định lượng (`Impact` về tiến độ, chi phí VNĐ, chất lượng hoặc bảo mật)**.

### 10.2. Phân Tích Định Tính (Ma Trận $5 \times 5$) và Định Lượng (`EMV` bằng VNĐ)
1. **Thang đo định tính $1\text{–}5$ và Điểm rủi ro (`Score`):**
   - Thiết lập bảng thang đo 5 mức cho Xác suất (`QualitativeP` từ 1 đến 5) và Tác động (`QualitativeI` từ 1 đến 5).
   - Công thức: $\text{Score} = \text{QualitativeP} \times \text{QualitativeI}$ (nhận giá trị từ $1$ đến $25$, phân thành 4 vùng: `1–3 Thấp`, `4–8 Trung bình`, `9–14 Cao`, `15–25 Rất cao`).
   - **Nguyên tắc bắt buộc:** `Score` là điểm thứ bậc định tính, **tuyệt đối không cộng tổng cột `Score`**.
2. **Phân tích định lượng bằng Giá trị tiền tệ kỳ vọng (`EMV`):**
   - Công thức: $\text{EMV (VNĐ)} = \text{Probability} \times \text{Impact (VNĐ)}$.
   - **Bắt buộc sử dụng đơn vị VNĐ** cho toàn bộ cột mức thiệt hại (`Impact`) và giá trị kỳ vọng (`EMV`).
3. **Đối chiếu thứ hạng đa tiêu chí (`Score` vs. `EMV` vs. `Impact tối đa`):**
   - Lập bảng xếp hạng cạnh tranh (đồng hạng thì cùng thứ hạng và bỏ qua thứ hạng kế tiếp) theo cả 3 góc nhìn: `Score`, `EMV` và `Impact`.
   - Giải thích rõ quy tắc quản trị thực chiến: đối với rủi ro có **tác động cực lớn ($\text{QualitativeI} = 5$)** như tấn công bảo mật hoặc hỏng toàn vẹn cơ sở dữ liệu, dù xác suất thấp làm `Score` và `EMV` ở mức trung bình nhưng tuyệt đối không được xếp ưu tiên thấp mà phải áp dụng biện pháp kiểm soát kỹ thuật bắt buộc và phương án chuyển giao/sao lưu cô lập.

### 10.3. Chiến Lược Ứng Phó, Theo Dõi Top Risk, Quỹ Dự Phòng và Cây Quyết Định
1. **Chiến lược ứng phó và 6 trường thực thi bắt buộc trong Sổ rủi ro:**
   - Mỗi rủi ro gây hại (`Threat`) chỉ được chọn **đúng 01 chiến lược chính** trong 4 chiến lược chuẩn: `Avoid` (Tránh), `Mitigate` (Giảm nhẹ), `Transfer` (Chuyển giao), `Accept` (Chấp nhận).
   - Bảng kế hoạch thực thi và kiểm soát rủi ro phải điền cụ thể **6 trường thực thi bắt buộc** theo ngữ cảnh CarClean CRM: Chủ sở hữu (`ResponseOwner`), Dấu hiệu kích hoạt đo đếm được (`Trigger`), Hành động phòng ngừa trước (`PreventiveResponse`), Kế hoạch dự phòng khi xảy ra (`ContingencyPlan`), Phương án thay thế (`FallbackPlan`), Rủi ro tồn dư (`ResidualRisk`) và Rủi ro thứ cấp (`SecondaryRisk`), kèm Trạng thái (`Status`) và Kỳ rà soát (`NextReview`).
2. **Theo dõi biến động các rủi ro hàng đầu (`Top Risk Item Tracking`):**
   - Lập bảng theo dõi thứ hạng các rủi ro qua các kỳ đánh giá (Hạng kỳ này, Giá trị `EMV`, Hạng kỳ trước, Biến động tăng/giảm bậc) và phân tích nhóm rủi ro dẫn đầu theo nguyên lý Pareto.
3. **Cơ cấu Quỹ dự phòng và Đường cơ sở chi phí (`Reserve & Budget Governance` tính bằng VNĐ):**
   - Áp dụng đúng 4 công thức chuẩn:
     $$\begin{aligned}
     \text{Quỹ dự phòng (Contingency Reserve - CR)} &= \sum \text{EMV của các rủi ro đã nhận diện} \\
     \text{Đường cơ sở chi phí (Cost Baseline)} &= B_0 + \text{CR} \\
     \text{Quỹ dự phòng quản lý (Management Reserve - MR)} &= B_0 \times 5\% \\
     \text{Tổng ngân sách dự án (Total Budget)} &= \text{Cost Baseline} + \text{MR}
     \end{aligned}$$
   - Phân biệt rõ: `Contingency Reserve` dành cho rủi ro đã biết (`Known Unknowns`), nằm **trong** `Cost Baseline` và do Quản lý dự án (`PM`) phê duyệt giải ngân khi xuất hiện `Trigger`; `Management Reserve` dành cho biến cố chưa biết (`Unknown Unknowns`), nằm **ngoài** `Cost Baseline` và phải trình **Giám đốc** (`Sponsor`) phê duyệt qua Phiếu yêu cầu thay đổi (`Change Request`).
4. **Phân tích Cây quyết định (`Decision Tree Analysis`) và Khẩu vị rủi ro (`Risk Appetite`):**
   - Đánh giá 4 phương án triển khai mở rộng dự án CarClean CRM với đầy đủ nhánh Thành công ($P_{\text{TC}}, V_{\text{TC}} > 0$) và nhánh Thất bại ($P_{\text{TB}}, V_{\text{TB}} < 0$), đảm bảo $P_{\text{TC}} + P_{\text{TB}} = 100\%$, giữ nguyên dấu âm cho khoản lỗ, tính $\text{EMV} = P_{\text{TC}} \times V_{\text{TC}} + P_{\text{TB}} \times V_{\text{TB}}$ và tỷ số hiệu suất trên rủi ro $\text{EMV} / |V_{\text{TB}}|$ (đơn vị **VNĐ**).
   - Phân tích quyết định lựa chọn theo 2 kịch bản: **Kịch bản A** (chọn theo $\text{EMV}$ kỳ vọng cao nhất) và **Kịch bản B** (chọn theo ràng buộc thanh khoản thực tế khi áp trần mức lỗ tối đa cho phép).
5. **Khai thác Cơ hội tích cực (`Opportunities`) và Lịch rà soát rủi ro định kỳ (`Risk Review Cadence`):**
   - Bổ sung bảng nhận diện tối thiểu 02 cơ hội tích cực (`OPP-01`, `OPP-02`) áp dụng chiến lược `Exploit`, `Enhance`, `Share`, `Accept` và bảng quy trình rà soát rủi ro định kỳ hàng tuần cùng trước mỗi cột mốc triển khai (`Go-live`).

