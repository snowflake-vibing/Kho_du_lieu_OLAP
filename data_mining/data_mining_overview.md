# HƯỚNG DẪN DATA MINING - PHẦN 1: TỔNG QUAN & PHÁT BIỂU BÀI TOÁN

---

## 1. MỤC TIÊU BÀI TOÁN KHAI THÁC DỮ LIỆU
Khai thác dữ liệu trong dự án bóng đá hướng tới việc phát hiện các tri thức ẩn sâu (Hidden Patterns) trong lịch sử thi đấu của cầu thủ để hỗ trợ ban huấn luyện đưa ra quyết định chiến thuật tối ưu.

---

## 2. ĐỊNH NGHĨA BÀI TOÁN DỰ BÁO CẦU THỦ ĐÁ CHÍNH (`STARTER PREDICTION`)

### 2.1. Biến Mục tiêu (Target Variable)
- **`Is_Starter`**: Biến nhị phân:
  - `1`: Cầu thủ ra sân trong đội hình xuất phát ($\ge 60$ phút thi đấu).
  - `0`: Cầu thủ vào sân từ băng ghế dự bị hoặc thi đấu ít hơn 60 phút.

### 2.2. Tập Thuộc tính Đầu vào (Feature Vector)
- **Thông tin Cầu thủ (`DIM_Player`)**: `Age` (Tuổi), `Height_In_Cm` (Chiều cao), `Main_Position` (Vị trí chính), `Foot` (Chân thuận), `Country_Of_Citizenship`.
- **Thông tin Câu lạc bộ (`DIM_Club`)**: `Squad_Size` (Quy mô đội hình), `Stadium_Seats`.
- **Bối cảnh Trận đấu (`DIM_Game` & `DIM_Time`)**: `Is_Home_Game` (Sân nhà/khách), `Season` (Mùa giải), `Is_Weekend`.
- **Lịch sử Kỷ luật (`FACT_Player_Match_Perf`)**: `Yellow_Cards`, `Red_Cards`.

---

## 3. CÁC TIÊU CHÍ ĐÁNH GIÁ MÔ HÌNH (EVALUATION METRICS)

1. **Accuracy (Độ chính xác)**: Tỷ lệ tổng số mẫu dự đoán đúng trên toàn bộ tập test.
2. **Precision (Độ chính xác tích cực)**: Tỷ lệ dự đoán đúng đá chính trên tổng số cầu thủ mô hình báo đá chính.
3. **Recall (Độ nhạy)**: Tỷ lệ mô hình phát hiện được cầu thủ thực sự đá chính.
4. **F1-Score**: Trung bình điều hòa giữa Precision và Recall.
5. **ROC-AUC Score**: Diện tích dưới đường cong ROC đo lường khả năng phân tách giữa hai lớp 0 và 1.

---

## 4. CHECKLIST KIỂM TRA THÀNH CÔNG
- [x] Định nghĩa rõ ràng bài toán dự báo nhị phân `Is_Starter`.
- [x] Xác định đầy đủ danh mục biến mục tiêu và tập thuộc tính tính toán.
- [x] Thống nhất các độ đo đánh giá tiêu chuẩn trong học máy.
