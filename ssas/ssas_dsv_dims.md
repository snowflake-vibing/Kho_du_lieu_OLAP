# HƯỚNG DẪN SSAS - PHẦN 2: THIẾT LẬP DATA SOURCE VIEW (DSV) & 5 DIMENSIONS

---

## 1. MỤC TIÊU HUẤN LUYỆN
Tạo **Data Source View (DSV)** chứa bảng Sự kiện (`FACT_Player_Match_Perf`) và 5 bảng Chiều (`DIM_Player`, `DIM_Club`, `DIM_Competition`, `DIM_Game`, `DIM_Time`), sau đó xây dựng 5 **Dimension Structure** tương ứng trong dự án SSAS.

---

## 2. BƯỚC 1: TẠO DATA SOURCE VIEW (DSV)

1. Trong Solution Explorer, chuột phải vào **Data Source Views** $\rightarrow$ chọn **New Data Source View...**
2. Nhấn **Next >** tại màn hình Welcome.
3. Chọn Data Source **`DS_DW_Football_Analytics`** $\rightarrow$ Nhấn **Next >**.
4. Tại màn hình **Select Tables and Views**:
   - Chọn và chuyển các bảng sau từ cột *Available objects* sang *Included objects*:
     - **`FACT_Player_Match_Perf`** (Fact Table)
     - **`DIM_Player`** (Dimension Table)
     - **`DIM_Club`** (Dimension Table)
     - **`DIM_Competition`** (Dimension Table)
     - **`DIM_Game`** (Dimension Table)
     - **`DIM_Time`** (Dimension Table)
5. Nhấn **Next >**.
6. Đặt tên DSV: **`DSV_DW_Football_Analytics`** $\rightarrow$ Nhấn **Finish**.
7. Kiểm tra sơ đồ DSV hiển thị liên kết chính xác giữa Fact và 5 Dims thông qua các Natural Keys:
   - `FACT_Player_Match_Perf.Player_ID` $\rightarrow$ `DIM_Player.Player_ID`
   - `FACT_Player_Match_Perf.Club_ID` $\rightarrow$ `DIM_Club.Club_ID`
   - `FACT_Player_Match_Perf.Competition_ID` $\rightarrow$ `DIM_Competition.Competition_ID`
   - `FACT_Player_Match_Perf.Game_ID` $\rightarrow$ `DIM_Game.Game_ID`
   - `FACT_Player_Match_Perf.Time_ID` $\rightarrow$ `DIM_Time.Time_ID`

---

## 3. BƯỚC 2: KHỞI TẠO 5 DIMENSIONS

### 1. Dimension: `DIM_Player`
1. Chuột phải vào **Dimensions** $\rightarrow$ chọn **New Dimension...** $\rightarrow$ **Next >**.
2. Chọn **Use an existing table** $\rightarrow$ **Next >**.
3. Chọn Main table là **`DIM_Player`**, Key column là **`Player_ID`**, Name column là **`Player_Name`**.
4. Tick chọn các thuộc tính (Attributes): `Date_Of_Birth`, `Age`, `Country_Of_Citizenship`, `Main_Position`, `Sub_Position`, `Foot`, `Height_In_Cm`.
5. Đặt tên Dimension: **`DIM_Player`** $\rightarrow$ Nhấn **Finish**.

### 2. Dimension: `DIM_Club`
1. Tạo New Dimension $\rightarrow$ chọn **`DIM_Club`**.
2. Key column là **`Club_ID`**, Name column là **`Club_Name`**.
3. Tick chọn các thuộc tính: `Stadium_Name`, `Stadium_Seats`, `Coach_Name`, `Squad_Size`.
4. Đặt tên Dimension: **`DIM_Club`** $\rightarrow$ Nhấn **Finish**.

### 3. Dimension: `DIM_Competition`
1. Tạo New Dimension $\rightarrow$ chọn **`DIM_Competition`**.
2. Key column là **`Competition_ID`**, Name column là **`Competition_Name`**.
3. Tick chọn các thuộc tính: `Country_Name`, `Competition_Type`.
4. Đặt tên Dimension: **`DIM_Competition`** $\rightarrow$ Nhấn **Finish**.

### 4. Dimension: `DIM_Game`
1. Tạo New Dimension $\rightarrow$ chọn **`DIM_Game`**.
2. Key column là **`Game_ID`**, Name column là **`Game_ID`** (hoặc `Round`).
3. Tick chọn các thuộc tính: `Round`, `Home_Club_ID`, `Away_Club_ID`, `Home_Club_Goals`, `Away_Club_Goals`, `Stadium`.
4. Đặt tên Dimension: **`DIM_Game`** $\rightarrow$ Nhấn **Finish**.

### 5. Dimension: `DIM_Time`
1. Tạo New Dimension $\rightarrow$ chọn **`DIM_Time`**.
2. Key column là **`Time_ID`**, Name column là **`Full_Date`**.
3. Tick chọn các thuộc tính: `Day_Of_Week`, `Day`, `Month`, `Quarter`, `Year`, `Season`, `Is_Weekend`.
4. Đặt tên Dimension: **`DIM_Time`** $\rightarrow$ Nhấn **Finish**.

---

## 4. CHECKLIST KIỂM TRA THÀNH CÔNG
- [x] DSV hiển thị đủ 6 bảng và các đường nối khóa ngoại (Relationships) chính xác.
- [x] Đã khởi tạo thành công 5 tệp `.dim` trong thư mục Dimensions.
- [x] Đã thiết lập đúng Key Columns và Name Columns cho từng Dimension.
