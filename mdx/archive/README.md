# KHO LƯU TRỮ PHIÊN BẢN CŨ (`mdx/archive/`)

Thư mục này chỉ lưu trữ các tệp nháp và phiên bản truy vấn cũ (`legacy_v1/`) được viết cho lược đồ kho dữ liệu trước đây (`DW_Football_Analytics` với khóa `*_SK`, `DIM_Time.Season`, `DIM_Player.Age`, `DIM_Club.Coach_Name`, `FACT.Is_Starter`).

Kể từ bản chuẩn hóa theo Chương 1 ([Bao_cao_OLAP.docx](../../bao-cao-olap/Bao_cao_OLAP.docx)) và Chương 3 ([Chuong_3_SSAS.docx](../../bao-cao-olap/Chuong_3_SSAS.docx)), **toàn bộ 15 câu truy vấn** (từ `query_01` đến `query_15`, mỗi câu gồm cả `.md` và `.mdx`) đã được cập nhật và đặt trực tiếp tại thư mục chính [`mdx/`](../README.md) — không còn để 5 câu trong `archive/`.

Các tệp được chuyển vào [`legacy_v1/`](./legacy_v1/) gồm:
- `doc_query_01.md` – `doc_query_12.md`: Bản nháp hướng dẫn cũ phục vụ ghép báo cáo trước khi chuẩn hóa Chương 3.
- `query_02.md`, `query_08.md`, `query_13.md`, `query_14.md`, `query_15.md`: Bản lưu cũ của 5 câu trước khi đưa ra thư mục chính `mdx/` và cập nhật theo `schema_warehouse.sql`.
- `test.md` và `Bao_Cao_Double_Check_Query_10_11.xlsx`: Tài liệu kiểm tra chéo gắn với phiên bản Câu 10–11 cũ.
