# KIẾN TRÚC KHỐI VÀ QUY TẮC VÀNG TRIỆT TIÊU WARNING TRONG SSIS

## 1. CHUẨN KIẾN TRÚC KHỐI TRONG DATA FLOW

Mỗi luồng dữ liệu Dimension (DIM) tuân thủ mô hình 6 khối tuần tự chuẩn hóa:

```
[Flat File Source] 
       │
       ▼
[Data Conversion]  ─── (Ép kiểu chuẩn DT_I4 hoặc DT_WSTR 100/200)
       │
       ▼
[Derived Column]   ─── (Tính toán thuộc tính & xử lý giá trị NULL/mặc định)
       │
       ▼
[Conditional Split] ─── (Validation kiểm tra dữ liệu tất cả các cột)
       │
       ▼ (Nhánh Valid_xxx)
[Sort]             ─── (Sắp xếp theo Business Key & Distinct loại trùng)
       │
       ▼
[OLE DB Destination] ── (Nạp dữ liệu vào SQL Server Fast Load)
```

---

## 2. QUY TẮC VÀNG TRIỆT TIÊU 100% WARNING TRONG SSIS

Để package SSIS hoàn toàn **SẠCH WARNING (0 tam giác vàng)**, luôn tuân thủ 3 nguyên tắc kỹ thuật sau:

1. **Đồng bộ độ dài 100% (Nguồn = Đích = 200 hoặc 100)**:
   * Độ dài chuỗi tại `Data Conversion` và `Sort` phải **bằng chính xác** độ dài cột `NVARCHAR` trong CSDL SQL Server (chỉ dùng duy nhất chuẩn **200** hoặc **100**).
2. **Kiểm tra điều kiện toàn bộ các cột trong Conditional Split**:
   * Khi dùng `Conditional Split` cho các bảng DIM và FACT (Staging), phải tick chọn **tất cả các cột** của luồng dữ liệu vào danh sách `InputColumns` và thiết lập biểu thức điều kiện kiểm tra toàn bộ các cột (`!ISNULL(...)`, `LEN(TRIM(...)) > 0`, `> 0`, `>= 0`) để đảm bảo không bỏ sót cột nào và tránh lỗi đứt đoạn `LineageID`.
3. **Lưu toàn bộ Project (`Ctrl + Shift + S`)**:
   * Sau khi chỉnh sửa UI trên Visual Studio, luôn bấm **Save All** để Visual Studio ghi nhận cấu hình từ RAM xuống đĩa `.dtsx` và làm mới Cache Validation.
