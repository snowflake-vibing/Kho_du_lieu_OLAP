# 5.1–5.2 Mô tả và tiền xử lý dữ liệu

## Dữ liệu đầu vào

Thí nghiệm sử dụng hai CSV ở commit `206cb41`. Bảng [lượt ra sân](../data/cleaned_appearances.csv) có 1.168.508 dòng và bảng [trận đấu](../data/cleaned_games.csv) có 88.958 dòng. Mỗi mẫu là một cầu thủ trong một trận. Lọc theo ngày dương lịch từ 2022 đến hết 2024.

| Trường | Vai trò |
| --- | --- |
| `appearance_id`, `game_id`, `player_id` | Kiểm tra trùng và phân tách trận giữa các tập |
| `competition_id`, tháng của trận | Đặc trưng bối cảnh có trước trận |
| `player_club_id`, `home_club_id`, `away_club_id` | Xác định cầu thủ thuộc CLB sân nhà hay sân khách |
| `minutes_played` | Tạo nhãn dương khi số phút từ 60 trở lên |
| `goals`, `assists`, `yellow_cards`, `red_cards` | Chỉ số quan sát sau trận, loại khỏi đầu vào |

Cách tạo nhãn bám theo [quy tắc ETL](../ssis/ssis_fact_player_match_perf.md). Nhãn âm bao gồm mọi lượt dưới 60 phút, kể cả cầu thủ thực tế xuất phát rồi rời sân sớm. Dữ liệu lượt ra sân chỉ cho phép đánh giá trên các cầu thủ đã được ghi nhận có tham gia trận.

## Chạy tiền xử lý

Chạy từ thư mục gốc của repo. Môi trường thực nghiệm dùng pandas 3.0.2, scikit-learn 1.7.2, XGBoost 3.4.1 và LightGBM 4.7.0 cùng NumPy.

```python
from pathlib import Path

import lightgbm
import numpy as np
import pandas as pd
import sklearn
import xgboost
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, average_precision_score, confusion_matrix, f1_score,
    precision_score, recall_score, roc_auc_score,
)
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

root = Path("data")
appearances = pd.read_csv(root / "cleaned_appearances.csv")
games = pd.read_csv(root / "cleaned_games.csv")
appearances["match_date"] = pd.to_datetime(
    appearances["date"], format="%m/%d/%Y", errors="coerce"
)
data = appearances.loc[appearances["match_date"].dt.year.between(2022, 2024)].copy()
print("source", len(appearances), len(games), "invalid dates", appearances["match_date"].isna().sum())
print("window", len(data), "missing outcomes", data["minutes_played"].isna().sum(),
      "duplicates", data["appearance_id"].duplicated().sum(),
      "duplicate player-game", data.duplicated(["game_id","player_id"]).sum())
assert not data["appearance_id"].duplicated().any()
assert not data.duplicated(["game_id", "player_id"]).any()
assert data["minutes_played"].notna().all() and data["minutes_played"].ge(0).all()
print("minutes > 120", data["minutes_played"].gt(120).sum())

data = data.merge(
    games[["game_id", "home_club_id", "away_club_id"]],
    on="game_id", how="left", validate="many_to_one"
)
on_home = data["player_club_id"].eq(data["home_club_id"])
on_away = data["player_club_id"].eq(data["away_club_id"])
data["venue_role"] = np.select([on_home & ~on_away, on_away & ~on_home], ["home", "away"], "unknown")
data["year"] = data["match_date"].dt.year
data["is_starter_proxy"] = data["minutes_played"].ge(60).astype(int)
data["competition_id"] = data["competition_id"].fillna("unknown")
data["match_month"] = data["match_date"].dt.month.astype(str)

print("EDA", data.groupby("year").agg(rows=("game_id", "size"), games=("game_id", "nunique"),
    positives=("is_starter_proxy","sum"), minutes_mean=("minutes_played","mean")).to_string(), flush=True)
print("unknown roles", data["venue_role"].eq("unknown").sum(), flush=True)
```

## Kết quả kiểm tra dữ liệu

| Năm dương lịch | Lượt ra sân | Trận phân biệt | Lượt từ 60 phút | Số phút trung bình |
| --- | ---: | ---: | ---: | ---: |
| 2022 | 129.335 | 4.824 | 87.116 | 65,33 |
| 2023 | 150.698 | 5.536 | 100.425 | 64,58 |
| 2024 | 145.640 | 5.287 | 96.360 | 64,20 |
| **Tổng** | **425.673** | **15.647** | **283.901** | |

Trong phạm vi phân tích, không có lượt trùng mã hoặc trùng cặp cầu thủ–trận, không thiếu số phút và mọi lượt đều xác định được sân nhà hoặc sân khách. Có một lượt trên 120 phút. Thí nghiệm giữ dòng đó theo giá trị nguồn vì nhãn vẫn thuộc nhóm từ 60 phút trở lên.
