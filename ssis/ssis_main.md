# HƯỚNG DẪN CẤU HÌNH CONTROL FLOW MASTER PACKAGE: SSIS_MAIN

> **Package chính:** `Master_ETL_Pipeline.dtsx` (hoặc `Main.dtsx`)  
> **Mô hình kiến trúc:** **Master Control Flow Architecture**  
> **Database:** `DW_Football_Analytics` (hoặc `DW_Football_Transfermarkt`)  
> **Chuẩn độ dài Chuỗi:** Áp dụng nghiêm ngặt chuẩn **`100`** hoặc **`200`** (`[DT_WSTR, 100]` hoặc `[DT_WSTR, 200]`), bảo đảm **100% SẠCH WARNING (0 tam giác vàng)**.

---

## 1. SƠ ĐỒ TOÀN CẢNH CONTROL FLOW (MASTER ETL PIPELINE FLOWCHART)

```text
               ┌─────────────────────────────────────────┐
               │   Execute SQL Task: Pre-ETL Cleanup     │
               │    (Truncate/Prepare Staging & Fact)    │
               └────────────────────┬────────────────────┘
                                    │ (Success)
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
            ▼                       ▼                       ▼
┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐
│  Data Flow Task:     │ │  Data Flow Task:     │ │  Data Flow Task:     │
│  Load DIM_Competition│ │  Load DIM_Club       │ │  Load DIM_Time       │
└───────────┬──────────┘ └──────────┬───────────┘ └──────────┬───────────┘
            │                       │                        │
            │                       ▼                        │
            │            ┌──────────────────────┐            │
            │            │  Data Flow Task:     │            │
            │            │  Load DIM_Player     │            │
            │            └──────────┬───────────┘            │
            │                       │                        │
            │                       ▼                        │
            │            ┌──────────────────────┐            │
            │            │  Data Flow Task:     │            │
            │            │  Load DIM_Game       │            │
            │            └──────────┬───────────┘            │
            │                       │                        │
            └───────────────────────┼────────────────────────┘
                                    │ (Tất cả 5 DIM hoàn tất Success)
                                    ▼
               ┌─────────────────────────────────────────┐
               │   Data Flow Task: Load FACT_Player_Match│
               │   Perf (Dùng chuỗi Lookup Transformations)│
               └────────────────────┬────────────────────┘
                                    │ (Success)
                                    ▼
               ┌─────────────────────────────────────────┐
               │   Execute SQL Task: Post-ETL Audit Log  │
               │   (Ghi log số dòng & thời gian hoàn tất)│
               └─────────────────────────────────────────┘
```

---

## 2. QUY TRÌNH THỰC THI CHI TIẾT TRONG CONTROL FLOW (STEP-BY-STEP CONTROL FLOW SETUP)

### Bước 1: Khối Khởi tạo Pre-ETL (`Execute SQL Task: Pre-ETL Cleanup`)
* **Loại khối**: `Execute SQL Task`
* **Name**: `Execute SQL Task - Pre ETL Cleanup`
* **Connection**: OLE DB Connection đến `DW_Football_Analytics`.
* **SQLStatement**:
  ```sql
  USE DW_Football_Analytics;
  GO

  -- Xóa sạch dữ liệu cũ tại bảng Fact và các bảng Staging trước khi chạy luồng ETL
  TRUNCATE TABLE dbo.FACT_Player_Match_Perf;
  TRUNCATE TABLE dbo.STG_Appearances;
  TRUNCATE TABLE dbo.STG_Games;
  GO
  ```

---

### Bước 2: Nhóm Nạp Bảng Dữ Liệu Chiều (Parallel Data Flow Tasks - DIM Execution Phase)

Tạo 5 khối **Data Flow Task** thực thi nạp dữ liệu cho 5 bảng Dimension theo thứ tự phụ thuộc:

1. **`DFT - Load DIM_Competition`**:
   - Đọc `cleaned_competitions.csv` $\rightarrow$ Data Conversion $\rightarrow$ Derived Column $\rightarrow$ Conditional Split $\rightarrow$ Sort $\rightarrow$ `dbo.DIM_Competition`.
   - *Tài liệu chi tiết:* [ssis_dim_competition.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_competition.md)

2. **`DFT - Load DIM_Club`**:
   - Đọc `cleaned_clubs.csv` $\rightarrow$ Data Conversion $\rightarrow$ Derived Column $\rightarrow$ Conditional Split $\rightarrow$ Sort $\rightarrow$ `dbo.DIM_Club`.
   - *Tài liệu chi tiết:* [ssis_dim_club.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_club.md)

3. **`DFT - Load DIM_Player`**:
   - Đọc `cleaned_players.csv` $\rightarrow$ Data Conversion $\rightarrow$ Derived Column $\rightarrow$ Conditional Split $\rightarrow$ Sort $\rightarrow$ `dbo.DIM_Player`.
   - *Tài liệu chi tiết:* [ssis_dim_player.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_player.md)

4. **`DFT - Load DIM_Time`**:
   - Đọc `cleaned_time.csv` (hoặc sinh tự động) $\rightarrow$ Data Conversion $\rightarrow$ Derived Column $\rightarrow$ Conditional Split $\rightarrow$ Sort $\rightarrow$ `dbo.DIM_Time`.
   - *Tài liệu chi tiết:* [ssis_dim_time.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_time.md)

5. **`DFT - Load DIM_Game`**:
   - Nối Precedence Constraint (Success) từ `DFT - Load DIM_Club` sang `DFT - Load DIM_Game`.
   - Đọc `cleaned_games.csv` $\rightarrow$ Data Conversion $\rightarrow$ Derived Column $\rightarrow$ Conditional Split $\rightarrow$ Sort $\rightarrow$ `dbo.DIM_Game`.
   - *Tài liệu chi tiết:* [ssis_dim_game.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_game.md)

---

### Bước 3: Nạp Bảng Sự Kiện Chính (`DFT - Load FACT_Player_Match_Perf`)

* **Loại khối**: `Data Flow Task`
* **Name**: `DFT - Load FACT_Player_Match_Perf`
* **Precedence Constraints**: Nối các đường mũi tên xanh (Success) từ **TẤT CẢ 5 khối Data Flow Task Dimension** (`DIM_Competition`, `DIM_Club`, `DIM_Player`, `DIM_Time`, `DIM_Game`) hội tụ về khối này.
* **Cấu hình Precedence Constraint**:
  * Tick chọn **Logical AND** (Tất cả các task DIM trước đó phải chạy hoàn tất `Success` thì mới kích hoạt nạp FACT).
* **Luồng Data Flow bên trong**:
  - Đọc `appearances.csv` $\rightarrow$ Data Conversion $\rightarrow$ Prep Time ID $\rightarrow$ Conditional Split $\rightarrow$ **Chuỗi 5 Lookup Transformations** (`Lookup Player`, `Lookup Club`, `Lookup Competition`, `Lookup Time`, `Lookup Game Info`) $\rightarrow$ Derived Column Fact Measures $\rightarrow$ `OLE DB Destination (dbo.FACT_Player_Match_Perf)`.
  - *Tài liệu chi tiết:* [ssis_fact_player_match_perf.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_fact_player_match_perf.md)

---

### Bước 4: Khối Ghi Log Hậu Xử Lý (`Execute SQL Task: Post-ETL Audit Log`)

* **Loại khối**: `Execute SQL Task`
* **Name**: `Execute SQL Task - Post ETL Audit Log`
* **Precedence Constraint**: Nối từ `DFT - Load FACT_Player_Match_Perf` (Success).
* **SQLStatement**:
  ```sql
  USE DW_Football_Analytics;
  GO

  -- Ghi nhận log hoàn tất tiến trình nạp kho dữ liệu
  INSERT INTO dbo.FACT_Player_Match_Perf_Error (Appearance_ID, Player_ID, Error_Reason, Error_Timestamp)
  VALUES ('AUDIT_LOG', 0, 'MASTER ETL PACKAGE COMPLETED SUCCESSFULLY', GETDATE());
  GO
  ```

---

## 3. CÁC NGUYÊN TẮC VÀNG VỀ HIỆU NĂNG VÀ QUẢN LÝ TIẾN TRÌNH SSIS

### 3.1. Quy tắc triệt tiêu 100% Warning (0 Tam Giác Vàng)
1. **Chuẩn độ dài chuỗi đồng nhất**:
   - Sử dụng duy nhất độ dài **100** hoặc **200** (`[DT_WSTR, 100]` / `[DT_WSTR, 200]`) trên toàn bộ các khối Data Conversion, Derived Column và OLE DB Destination.
2. **Kiểm tra Validation toàn bộ các cột trong Conditional Split**:
   - Mọi khối `Conditional Split` ở tất cả các luồng phải đưa **đầy đủ 100% cột** đầu vào vào danh sách `InputColumns` và tạo biểu thức kiểm tra (`!ISNULL(...)`, `LEN(TRIM(...)) > 0`, `> 0`, `>= 0`).
3. **Lưu toàn bộ Project (`Ctrl + Shift + S`)**:
   - Luôn thực hiện **Save All** để làm mới bộ nhớ tạm Validation Cache của Visual Studio.

### 3.2. Tối ưu hóa tốc độ nạp dữ liệu (Fast Load & Parallel Processing)
* **Maximum Concurrent Executables**: Đặt trong thuộc tính của Package (`-1` để SSIS tự tối ưu theo số lõi CPU của máy tính).
* **Fast Load Mode**: Tất cả các khối `OLE DB Destination` đều bật cấu hình:
  * Data Access Mode: `Table or view - fast load`
  * Rows per batch: `50000`
  * Maximum insert commit size: `50000`
  * Options: Tick chọn `Table lock` và `Check constraints`.

---

## 4. BẢNG TỔNG HỢP DANH MỤC TỆP HƯỚNG DẪN CẤU HÌNH SSIS

| STT | Tên Tệp Hướng Dẫn | Thành Phần | Bảng Đích / Mục Đích |
| :---: | :--- | :--- | :--- |
| 1 | [ssis_main.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_main.md) | **Control Flow** | Tổng quan quy trình Master Pipeline |
| 2 | [ssis_dim_competition.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_competition.md) | Data Flow | `[dbo].[DIM_Competition]` |
| 3 | [ssis_dim_club.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_club.md) | Data Flow | `[dbo].[DIM_Club]` |
| 4 | [ssis_dim_player.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_player.md) | Data Flow | `[dbo].[DIM_Player]` |
| 5 | [ssis_dim_time.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_time.md) | Data Flow | `[dbo].[DIM_Time]` |
| 6 | [ssis_dim_game.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_dim_game.md) | Data Flow | `[dbo].[DIM_Game]` |
| 7 | [ssis_fact_player_match_perf.md](file:///d:/Kho_du_lieu_OLAP/ssis/ssis_fact_player_match_perf.md) | Data Flow | `[dbo].[FACT_Player_Match_Perf]` |
