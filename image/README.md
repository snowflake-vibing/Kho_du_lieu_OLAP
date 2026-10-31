# DANH MỤC HÌNH ẢNH MINH HỌA CÁC CÂU TRUY VẤN TỪ QUERY 6 ĐẾN QUERY 10 (48 HÌNH ẢNH CHUẨN)

Tài liệu này tổng hợp toàn bộ các hình ảnh minh chứng thực nghiệm được trích xuất trực tiếp theo từng khung hình từ video gốc [`MDX_Final.mp4`](file:///C:/Users/GIGA/Downloads/MDX_Final.mp4), đảm bảo tính chính xác, đồng bộ 100% giữa ba môi trường: **Visual Studio (Tab Calculations & Cube Browser)**, **Microsoft Excel (PivotTable Report)** và **SQL Server Management Studio (SSMS MDX Query)**.

---

## 1. CÂU TRUY VẤN 6: PHÂN TÍCH PARETO 80% BÀN THẮNG TẠI NƯỚC ANH (11 ảnh)

| STT | Tên file hình ảnh | Mốc thời gian | Môi trường giao diện | Giải thích chi tiết nội dung hiển thị trong ảnh |
|:---:|:---|:---:|:---|:---|
| 1 | `query_6_step_1-calculations_tao_pct_of_england_goals.png` | **43:05** | Visual Studio - Calculations | Tạo thước đo tính toán `Pct_Of_England_Goals`, thiết lập công thức tính tỷ lệ phần trăm số bàn thắng độc lập tự chủ và định dạng chuỗi `0.00%`. |
| 2 | `query_6_step_2-deploy_solution_ssas.png` | **43:20** | Visual Studio - Deployment Progress | Cửa sổ tiến trình Deploy Solution hiển thị trạng thái `Deploy: 1 succeeded, 0 failed` xác nhận thước đo đã được nạp thành công vào khối Cube SSAS. |
| 3 | `query_6_step_3-cube_browser_loc_country_england.png` | **43:40** | Visual Studio - Cube Browser (Filter Pane) | Cấu hình dòng bộ lọc thứ nhất trên Filter Pane: Chiều `DIM Competition`, Hierarchy `Country Name`, toán tử `Equal`, giá trị lọc `England`. |
| 4 | `query_6_step_4-cube_browser_loc_toppercent_80.png` | **44:05** | Visual Studio - Cube Browser (Filter Pane) | Cấu hình dòng bộ lọc thứ hai: Chiều `DIM Player`, Hierarchy `Player Name`, toán tử `Custom`, mở Expression Builder hiển thị hàm `TOPPERCENT` lấy ngưỡng tích lũy 80% bàn thắng. |
| 5 | `query_6_step_5-cube_browser_keo_tha_data_grid.png` | **44:20** | Visual Studio - Cube Browser (Data Grid Drag) | Kéo thả trường phân cấp `Citizenship` vào trục Rows và các thước đo `Goals`, `Pct_Of_England_Goals` vào vùng Data trước khi chạy truy vấn. |
| 6 | `query_6_step_6-cube_browser_ket_qua_18_quoc_gia.png` | **44:35** | Visual Studio - Cube Browser (Data Grid Executed) | Bảng kết quả thực thi trong Cube Browser hiển thị đúng danh sách 18 quốc gia chiếm 80% tổng số bàn thắng tại giải bóng đá nước Anh. |
| 7 | `query_6_step_7-excel_keo_tha_pivottable_fields.png` | **45:10** | Microsoft Excel - PivotTable Fields | Khung PivotTable Fields hiển thị các trường đã kéo: `Citizenship` vào Rows; `Goals` và `Pct_Of_England_Goals` vào Values; Report Filter chọn `Country Name = England`. |
| 8 | `query_6_step_8-excel_thiet_lap_loc_top_80_percent.png` | **45:30** | Microsoft Excel - Top 10 Filter Dialog | Hộp thoại `Top 10 Filter (Citizenship)` cấu hình lọc lấy `Top` `80` `Percent` theo chỉ số `Sum of Goals` để áp dụng nguyên lý Pareto trong Excel. |
| 9 | `query_6_step_9-excel_sap_xep_giam_dan_ban_thang.png` | **45:45** | Microsoft Excel - Thao tác Sort | Thao tác nhấp chuột phải vào cột số bàn thắng, chọn `Sort` $
ightarrow$ `Sort Largest to Smallest` để danh sách sắp xếp ưu tiên từ quốc gia ghi nhiều bàn nhất xuống. |
| 10 | `query_6_step_10-excel_ket_qua_pivottable_hoan_chinh.png` | **46:00** | Microsoft Excel - PivotTable Worksheet | Bảng kết quả PivotTable Excel hoàn chỉnh hiển thị đúng 18 quốc gia dẫn đầu theo Pareto 80%, định dạng Tabular rõ ràng, khớp tuyệt đối MDX. |
| 11 | `query_6_step_11-ssms_thuc_thi_mdx_va_ket_qua.png` | **46:30** | SSMS - MDX Editor & Results Grid | Cửa sổ SSMS hiển thị toàn bộ câu truy vấn MDX tối ưu và lưới kết quả thực thi thành công (`Query executed successfully`) với đúng 18 dòng dữ liệu. |

---

## 2. CÂU TRUY VẤN 7: TẬP HỢP GIAO GIỮA 2 TIÊU CHÍ (INTERSECT) (8 ảnh)

| STT | Tên file hình ảnh | Mốc thời gian | Môi trường giao diện | Giải thích chi tiết nội dung hiển thị trong ảnh |
|:---:|:---|:---:|:---|:---|
| 1 | `query_7_step_1-cube_browser_thiet_lap_bo_loc_custom.png` | **46:40** | Visual Studio - Cube Browser (Filter Pane) | Cấu hình bộ lọc trên Filter Pane: Chiều `DIM Club`, Hierarchy `Club Name`, cột Operator chọn toán tử `Custom` và mở hộp thoại Expression Builder. |
| 2 | `query_7_step_2-cube_browser_loc_bieu_thuc_intersect.png` | **47:05** | Visual Studio - Cube Browser (Expression Builder) | Hộp thoại `Expression Builder` hiển thị nguyên văn biểu thức đại số tập hợp hàm `INTERSECT` giao giữa Top 30 CLB nhiều bàn thắng Cuối tuần (Is Weekend = 1) và Top 30 CLB nhiều bàn thắng Ngày thường (Is Weekend = 0). |
| 3 | `query_7_step_3-cube_browser_keo_tha_data_grid.png` | **47:30** | Visual Studio - Cube Browser (Data Grid Drag) | Lưới Data Grid sau khi kéo thả trường `Club Name` vào trục Rows, trường `Is Weekend` vào Columns và các thước đo vào Data; sẵn sàng với thông báo `"Click to execute the query."`. |
| 4 | `query_7_step_4-cube_browser_ket_qua_9_clb.png` | **47:45** | Visual Studio - Cube Browser (Data Grid Executed) | Bảng kết quả thực thi trong Cube Browser hiển thị đúng 9 câu lạc bộ toàn diện nhất lọt vào Top 30 cả Cuối tuần và Ngày thường, phân rã theo số bàn thắng (Goals) và thẻ phạt (Yellow Cards). |
| 5 | `query_7_step_5-excel_keo_tha_pivottable_fields.png` | **48:30** | Microsoft Excel - PivotTable Fields | Khung danh sách trường PivotTable Fields hiển thị kéo thả trường `Is Weekend` vào Columns, các thước đo vào Values. |
| 6 | `query_7_step_6-excel_create_set_using_mdx.png` | **49:10** | Microsoft Excel - MDX Set Builder | Hộp thoại `New Set` sử dụng tính năng `Create Set Using MDX...` dán biểu thức `INTERSECT` chuẩn đại số tập hợp OLAP theo đúng Quy tắc Rule 3. |
| 7 | `query_7_step_7-excel_ket_qua_pivottable_hoan_chinh.png` | **49:40** | Microsoft Excel - PivotTable Worksheet | Bảng PivotTable hoàn chỉnh trong Excel hiển thị đúng 9 câu lạc bộ giao thoa với đầy đủ các cột số liệu ngày thường và cuối tuần. |
| 8 | `query_7_step_8-ssms_thuc_thi_mdx_va_ket_qua.png` | **50:20** | SSMS - MDX Editor & Results Grid | Cửa sổ SSMS hiển thị câu truy vấn MDX tối ưu mệnh đề `INTERSECT` và lưới kết quả thực thi thành công trả về đúng 9 dòng tương ứng. |

---

## 3. CÂU TRUY VẤN 8: TĂNG TRƯỞNG BÀN THẮNG THEO QUÝ (QOQ) CỦA TOP 10 CLB NĂM 2023 (10 ảnh)

| STT | Tên file hình ảnh | Mốc thời gian | Môi trường giao diện | Giải thích chi tiết nội dung hiển thị trong ảnh |
|:---:|:---|:---:|:---|:---|
| 1 | `query_8_step_1-calculations_tao_qoq_goals_growth.png` | **51:40** | Visual Studio - Calculations | Tạo Calculated Member `[QoQ_Goals_Growth]` sử dụng hàm chuỗi thời gian `PARALLELPERIOD` kết hợp hàm `IIF` kiểm tra mẫu số khác 0 và định dạng `0.00%`. |
| 2 | `query_8_step_2-calculations_tao_named_set_top_10_clubs.png` | **52:18** | Visual Studio - Calculations | Tạo Named Set `[Top_10_Clubs_2023]` sử dụng hàm `TOPCOUNT` lấy 10 câu lạc bộ có tổng số bàn thắng cao nhất trong năm 2023. |
| 3 | `query_8_step_3-deploy_solution_ssas.png` | **52:25** | Visual Studio - Deployment Progress | Cửa sổ Deployment Progress hiển thị trạng thái `Deploy: 1 succeeded, 0 failed` xác nhận thước đo và Named Set đã được nạp hoàn tất. |
| 4 | `query_8_step_4-cube_browser_loc_nam_2023.png` | **52:32** | Visual Studio - Cube Browser (Filter Pane) | Cấu hình dòng bộ lọc thứ nhất trên Filter Pane: Chiều `DIM Time`, Hierarchy `Year`, toán tử `Equal`, giá trị lọc `2023`. |
| 5 | `query_8_step_5-cube_browser_loc_top_10_clubs.png` | **52:51** | Visual Studio - Cube Browser (Filter Pane) | Cấu hình dòng bộ lọc thứ hai: Kéo Named Set `Top_10_Clubs_2023` vào Filter Pane để giới hạn tập hợp 10 CLB hàng đầu. |
| 6 | `query_8_step_6-cube_browser_ket_qua_10_clb_qua_4_quy.png` | **53:22** | Visual Studio - Cube Browser (Data Grid Executed) | Bảng kết quả thực thi trong Cube Browser hiển thị 10 câu lạc bộ hàng đầu châu Âu cùng chỉ số tăng trưởng QoQ qua 4 quý của năm 2023. |
| 7 | `query_8_step_7-excel_keo_tha_pivottable_fields.png` | **54:20** | Microsoft Excel - PivotTable Fields | Khung PivotTable Fields kéo thả Named Set `Top_10_Clubs_2023` vào Rows, trường `Quarter` vào Columns, các thước đo Goals và QoQ Growth vào Values; Filter chọn năm 2023. |
| 8 | `query_8_step_8-excel_an_cot_quy_1_rong.png` | **54:30** | Microsoft Excel - Thao tác Hide cột | Thao tác nhấp chuột phải vào tiêu đề cột `QoQ_Goals_Growth` của Quý 1 chọn `Hide` để ẩn cột mang giá trị NULL, đồng bộ 100% với trục COLUMNS của MDX. |
| 9 | `query_8_step_9-excel_ket_qua_pivottable_hoan_chinh.png` | **54:46** | Microsoft Excel - PivotTable Worksheet | Bảng PivotTable hoàn chỉnh sạch đẹp gồm đúng 10 CLB và 7 cột số liệu qua 4 quý, khớp chính xác từng ô dữ liệu với MDX. |
| 10 | `query_8_step_10-ssms_thuc_thi_mdx_va_ket_qua.png` | **55:25** | SSMS - MDX Editor & Results Grid | Cửa sổ SSMS hiển thị câu truy vấn MDX phân tích chuỗi thời gian QoQ và lưới kết quả thực thi thành công trả về ma trận dữ liệu 10 dòng x 7 cột. |

---

## 4. CÂU TRUY VẤN 9: THỐNG KÊ SÂN VẬN ĐỘNG SỨC CHỨA TỪ 60.000 CHỖ TRỞ LÊN (10 ảnh)

| STT | Tên file hình ảnh | Mốc thời gian | Môi trường giao diện | Giải thích chi tiết nội dung hiển thị trong ảnh |
|:---:|:---|:---:|:---|:---|
| 1 | `query_9_step_1-calculations_tao_stadium_capacity_cleaned.png` | **56:45** | Visual Studio - Calculations | Tạo Calculated Member `Stadium_Capacity_Cleaned` với cú pháp chuẩn `MAX(EXISTING [DIM Club].[Stadium Seats].[Stadium Seats].MEMBERS, ...)` theo Quy tắc GEMINI.md Rule 5. |
| 2 | `query_9_step_2-calculations_tao_distinct_matches_played.png` | **57:30** | Visual Studio - Calculations | Tạo Calculated Member `Distinct_Matches_Played` tính số trận đấu thực tế độc lập tại từng sân vận động sử dụng hàm `DISTINCTCOUNT`. |
| 3 | `query_9_step_3-cube_browser_loc_custom_suc_chua_60000.png` | **58:10** | Visual Studio - Cube Browser (Filter Pane) | Cấu hình bộ lọc trên Filter Pane: Chiều `DIM Club`, Hierarchy `Stadium Name`, toán tử `Custom`, mở Expression Builder dán biểu thức `FILTER` sức chứa $\ge 60.000$. |
| 4 | `query_9_step_4-cube_browser_keo_tha_truong_du_lieu.png` | **58:31** | Visual Studio - Cube Browser (Data Grid Drag) | Lưới Data Grid sau khi kéo thả đầy đủ 5 cột thông tin (`Stadium Name`, `Club Name`, `Stadium Seats`, `Stadium_Capacity_Cleaned`, `Distinct_Matches_Played`) và thông báo `"Click to execute the query."`. |
| 5 | `query_9_step_5-cube_browser_ket_qua_23_san_van_dong.png` | **58:34** | Visual Studio - Cube Browser (Data Grid Executed) | Bảng kết quả thực thi trong Cube Browser hiển thị đúng danh sách 23 sân vận động quy mô lớn có sức chứa từ 60.000 chỗ ngồi trở lên. |
| 6 | `query_9_step_6-excel_keo_tha_pivottable_fields.png` | **59:42** | Microsoft Excel - PivotTable Fields | Khung PivotTable Fields hiển thị các trường đã kéo vào đầy đủ: `Stadium Name`, `Club Name` ở Rows; `Stadium Seats`, `Stadium_Capacity_Cleaned`, `Distinct_Matches_Played` ở Values. |
| 7 | `query_9_step_7-excel_value_filter_lon_hon_bang_60000.png` | **59:55** | Microsoft Excel - Value Filter Dialog | Hộp thoại `Value Filter (Stadium Name)` thiết lập điều kiện lọc `is greater than or equal to 60000` trên thước đo `Stadium_Capacity_Cleaned`. |
| 8 | `query_9_step_8-excel_sap_xep_giam_dan_suc_chua.png` | **60:06** | Microsoft Excel - Thao tác Sort | Thao tác nhấp chuột phải vào một ô số trong cột `Stadium_Capacity_Cleaned`, di chuột vào menu `Sort` $
ightarrow$ chọn `Sort Largest to Smallest` để sắp xếp giảm dần theo sức chứa. |
| 9 | `query_9_step_9-excel_ket_qua_pivottable_hoan_chinh.png` | **60:17** | Microsoft Excel - PivotTable Worksheet | Bảng PivotTable hoàn chỉnh hiển thị đúng 23 sân vận động dẫn đầu bởi Camp Nou (99.354 chỗ), Wembley Stadium (90.000 chỗ)... định dạng phẳng Tabular chuẩn mực. |
| 10 | `query_9_step_10-ssms_thuc_thi_mdx_va_ket_qua.png` | **60:50** | SSMS - MDX Editor & Results Grid | Cửa sổ SSMS hiển thị toàn bộ câu lệnh MDX tối ưu và lưới kết quả thực thi hoàn tất thành công (`Query executed successfully`), trả về đúng 23 dòng dữ liệu. |

---

## 5. CÂU TRUY VẤN 10: THỐNG KÊ THÁNG GHI NHẬN SỐ LƯỢNG THẺ PHẠT NHIỀU NHẤT TRONG NĂM CỦA TỪNG HUẤN LUYỆN VIÊN TRƯỞNG (8 ảnh chuẩn + 1 ảnh thao tác lọc)

| STT | Tên file hình ảnh | Mốc thời gian | Môi trường giao diện | Giải thích chi tiết nội dung hiển thị trong ảnh |
|:---:|:---|:---:|:---|:---|
| 1 | `query_10_step_1-cube_browser_bieu_thuc_generate.png` | **61:55** | Visual Studio - Cube Browser (Expression Builder) | Mở hộp thoại `Expression Builder` tại điều kiện lọc Custom của thuộc tính `Coach Name` thuộc chiều `DIM Club`, dán và hiển thị đầy đủ biểu thức MDX lặp tập hợp `GENERATE` kết hợp `FILTER(NONEMPTY(...))` và `TOPCOUNT(..., 1, [Measures].[Yellow Cards])` để trích xuất duy nhất 1 tháng đỉnh điểm thẻ phạt cho từng HLV trưởng. |
| 2 | `query_10_step_2-cube_browser_keo_tha_data_grid.png` | **62:30** | Visual Studio - Cube Browser (Data Grid Drag) | Lưới thiết kế Data Grid sau khi kéo thả các trường dữ liệu: thuộc tính `Coach Name` (DIM Club) và `Month` (DIM Time) vào trục Rows, cùng 2 thước đo `Yellow Cards` và `Red Cards` vào vùng dữ liệu. Trạng thái hiển thị thông báo sẵn sàng `"Click to execute the query."` trước khi bấm chạy truy vấn. |
| 3 | `query_10_step_3-cube_browser_ket_qua_thang_the_phat_hlv.png` | **62:45** | Visual Studio - Cube Browser (Data Grid Executed) | Bảng kết quả thực thi thành công trong Cube Browser hiển thị danh sách các HLV trưởng cùng duy nhất 1 tháng cao điểm thẻ phạt và số thẻ vàng, thẻ đỏ chi tiết. |
| 4 | `query_10_step_4-excel_keo_tha_pivottable_fields.png` | **63:42** | Microsoft Excel - PivotTable Fields | Khung thao tác `PivotTable Fields` ở cạnh phải màn hình hiển thị trực quan và đầy đủ 100% các trường: `Coach Name` và `Month` trong ô Rows; cả hai thước đo `Yellow Cards` và `Red Cards` trong ô Values. Trang tính hiển thị bố cục dạng phẳng Tabular sạch đẹp. |
| 5 | `query_10_step_5-excel_value_filter_top_1_month_the_vang.png` | **63:50** | Microsoft Excel - Top 10 Filter Dialog | Hộp thoại `Top 10 Filter (Month)` đang mở ở vị trí trung tâm, cấu hình lọc lấy `Top` `1` `Items` theo chỉ số `Sum of Yellow Cards` để giới hạn mỗi vị huấn luyện viên chỉ hiển thị duy nhất 1 tháng đỉnh điểm thẻ vàng. |
| 6 | `query_10_step_6-excel_sap_xep_giam_dan_the_vang.png` | **64:39** | Microsoft Excel - Sort Dialog | Hộp thoại `Sort (Coach Name)` hiển thị thao tác thiết lập sắp xếp giảm dần toàn cục `Descending (Z to A) by:` theo thước đo `Sum of Yellow Cards` nhằm ưu tiên đưa các HLV nhận nhiều thẻ vàng nhất lên đầu danh sách. |
| 6b | `query_10_step_6b-excel_loc_bo_unknown_coach.png` | **64:55** | Microsoft Excel - Dropdown Filter Menu | Menu lọc tại cột `Coach Name` gõ tìm kiếm `unkn` và thao tác bỏ tích chọn `Unknown Coach` để loại bỏ vị huấn luyện viên không xác định, đồng bộ 100% với điều kiện MDX. |
| 7 | `query_10_step_7-excel_ket_qua_pivottable_hoan_chinh.png` | **65:28** | Microsoft Excel - PivotTable Worksheet | Bảng PivotTable hoàn chỉnh, sạch đẹp, các menu lọc đã đóng kín; hiển thị chính xác từng huấn luyện viên trưởng, tháng kỷ lục và số lượng thẻ phạt, dẫn đầu là HLV Matías Almeyda (Tháng 10: 32 thẻ vàng, 14 thẻ đỏ), Diego Simeone (Tháng 10: 27 thẻ vàng, 6 thẻ đỏ)... loại bỏ hoàn toàn Unknown Coach. |
| 8 | `query_10_step_8-ssms_thuc_thi_mdx_va_ket_qua.png` | **65:45** | SSMS - MDX Editor & Results Grid | Cửa sổ SSMS hiển thị toàn bộ câu truy vấn MDX tối ưu và lưới kết quả thực thi đã hoàn tất thành công (`Query executed successfully`, 178 dòng), trả về số liệu đồng quy 100% với Cube Browser và Excel PivotTable. |
