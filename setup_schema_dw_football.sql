-- ===============================================================================
-- FILE SQL: TẠO LẠI TOÀN BỘ CÁC BẢNG DBO & VIEWS TRONG KHO DỮ LIỆU DW_Football_Transfermarkt & DW_Football_Analytics
-- MÔ HÌNH HÌNH SAO SỬ DỤNG NATURAL KEYS (ID TRỰC TIẾP), BỎ SURROGATE KEYS (*_SK)
-- ===============================================================================

-- 1. XÓA CÁC VIEWS VÀ BẢNG CŨ THEO ĐÚNG THỨ TỰ THAM CHIẾU
IF OBJECT_ID('dbo.v_FACT_Player_Match_Perf', 'V') IS NOT NULL DROP VIEW dbo.v_FACT_Player_Match_Perf;
IF OBJECT_ID('dbo.v_DIM_Competition', 'V') IS NOT NULL DROP VIEW dbo.v_DIM_Competition;
IF OBJECT_ID('dbo.v_DIM_Club', 'V') IS NOT NULL DROP VIEW dbo.v_DIM_Club;
IF OBJECT_ID('dbo.v_DIM_Player', 'V') IS NOT NULL DROP VIEW dbo.v_DIM_Player;
IF OBJECT_ID('dbo.v_DIM_Time', 'V') IS NOT NULL DROP VIEW dbo.v_DIM_Time;

IF OBJECT_ID('dbo.FACT_Player_Match_Perf', 'U') IS NOT NULL DROP TABLE dbo.FACT_Player_Match_Perf;
IF OBJECT_ID('dbo.FACT_Player_Match_Perf_Error', 'U') IS NOT NULL DROP TABLE dbo.FACT_Player_Match_Perf_Error;
IF OBJECT_ID('dbo.STG_Appearances', 'U') IS NOT NULL DROP TABLE dbo.STG_Appearances;
IF OBJECT_ID('dbo.STG_Games', 'U') IS NOT NULL DROP TABLE dbo.STG_Games;
IF OBJECT_ID('dbo.DIM_Player', 'U') IS NOT NULL DROP TABLE dbo.DIM_Player;
IF OBJECT_ID('dbo.DIM_Club', 'U') IS NOT NULL DROP TABLE dbo.DIM_Club;
IF OBJECT_ID('dbo.DIM_Competition', 'U') IS NOT NULL DROP TABLE dbo.DIM_Competition;
IF OBJECT_ID('dbo.DIM_Game', 'U') IS NOT NULL DROP TABLE dbo.DIM_Game;
IF OBJECT_ID('dbo.DIM_Time', 'U') IS NOT NULL DROP TABLE dbo.DIM_Time;
GO

-- 2. TẠO BẢNG DIMENSION (DIM_Competition) - PK: Competition_ID
CREATE TABLE dbo.DIM_Competition (
    Competition_ID NVARCHAR(100) CONSTRAINT PK_DIM_Competition PRIMARY KEY,
    Competition_Name NVARCHAR(200) NULL,
    Country_Name NVARCHAR(200) NULL,
    Competition_Type NVARCHAR(100) NULL
);
GO

-- 3. TẠO BẢNG DIMENSION (DIM_Club) - PK: Club_ID
CREATE TABLE dbo.DIM_Club (
    Club_ID INT CONSTRAINT PK_DIM_Club PRIMARY KEY,
    Club_Name NVARCHAR(200) NULL,
    Stadium_Name NVARCHAR(200) NULL,
    Stadium_Seats INT NULL,
    Coach_Name NVARCHAR(200) NULL,
    Squad_Size INT NULL
);
GO

-- 4. TẠO BẢNG DIMENSION (DIM_Player) - PK: Player_ID
CREATE TABLE dbo.DIM_Player (
    Player_ID INT CONSTRAINT PK_DIM_Player PRIMARY KEY,
    Player_Name NVARCHAR(200) NULL,
    Date_Of_Birth NVARCHAR(100) NULL,
    Age INT NULL,
    Country_Of_Citizenship NVARCHAR(200) NULL,
    Main_Position NVARCHAR(100) NULL,
    Sub_Position NVARCHAR(100) NULL,
    Foot NVARCHAR(100) NULL,
    Height_In_Cm INT NULL
);
GO

-- 5. TẠO BẢNG DIMENSION (DIM_Game) - PK: Game_ID
CREATE TABLE dbo.DIM_Game (
    Game_ID INT CONSTRAINT PK_DIM_Game PRIMARY KEY,
    Round NVARCHAR(100) NULL,
    Home_Club_ID INT NULL,
    Away_Club_ID INT NULL,
    Home_Club_Goals INT NULL,
    Away_Club_Goals INT NULL,
    Stadium NVARCHAR(200) NULL
);
GO

-- 6. TẠO BẢNG DIMENSION (DIM_Time) - PK: Time_ID (YYYYMMDD)
CREATE TABLE dbo.DIM_Time (
    Time_ID INT CONSTRAINT PK_DIM_Time PRIMARY KEY,
    Full_Date NVARCHAR(100) NULL,
    Day_Of_Week NVARCHAR(100) NULL,
    Day INT NULL,
    Month INT NULL,
    Quarter INT NULL,
    Year INT NULL,
    Season NVARCHAR(100) NULL,
    Is_Weekend INT NULL
);
GO

-- 7. TẠO CÁC BẢNG STAGING (STG_Appearances, STG_Games)
CREATE TABLE dbo.STG_Appearances (
    appearance_id VARCHAR(100),
    game_id INT,
    player_id INT,
    player_club_id INT,
    date_str VARCHAR(100),
    competition_id VARCHAR(100),
    goals INT,
    assists INT,
    minutes_played INT,
    yellow_cards INT,
    red_cards INT
);
GO

CREATE TABLE dbo.STG_Games (
    game_id INT,
    competition_id NVARCHAR(100),
    season INT,
    round NVARCHAR(100),
    date_str NVARCHAR(100),
    home_club_id INT,
    away_club_id INT,
    home_club_goals INT,
    away_club_goals INT,
    stadium NVARCHAR(200)
);
GO

-- 8. TẠO BẢNG FACT (FACT_Player_Match_Perf)
CREATE TABLE dbo.FACT_Player_Match_Perf (
    Appearance_ID INT IDENTITY(1,1) CONSTRAINT PK_FACT_Player_Match_Perf PRIMARY KEY,
    Player_ID INT NOT NULL,
    Club_ID INT NOT NULL,
    Opponent_Club_ID INT NULL,
    Competition_ID NVARCHAR(100) NOT NULL,
    Game_ID INT NOT NULL,
    Time_ID INT NOT NULL,
    Minutes_Played INT DEFAULT 0,
    Goals INT DEFAULT 0,
    Assists INT DEFAULT 0,
    Goal_Contributions INT DEFAULT 0,
    Yellow_Cards INT DEFAULT 0,
    Red_Cards INT DEFAULT 0,
    Is_Starter INT DEFAULT 0,
    Is_Home_Game INT DEFAULT 0,

    CONSTRAINT FK_Fact_Player FOREIGN KEY (Player_ID) REFERENCES dbo.DIM_Player(Player_ID),
    CONSTRAINT FK_Fact_Club FOREIGN KEY (Club_ID) REFERENCES dbo.DIM_Club(Club_ID),
    CONSTRAINT FK_Fact_Competition FOREIGN KEY (Competition_ID) REFERENCES dbo.DIM_Competition(Competition_ID),
    CONSTRAINT FK_Fact_Game FOREIGN KEY (Game_ID) REFERENCES dbo.DIM_Game(Game_ID),
    CONSTRAINT FK_Fact_Time FOREIGN KEY (Time_ID) REFERENCES dbo.DIM_Time(Time_ID)
);
GO

CREATE TABLE dbo.FACT_Player_Match_Perf_Error (
    Error_ID INT IDENTITY(1,1) PRIMARY KEY,
    Appearance_ID VARCHAR(100),
    Player_ID INT,
    Club_ID INT,
    Competition_ID NVARCHAR(100),
    Game_ID INT,
    Time_ID INT,
    Error_Reason NVARCHAR(500),
    Error_Timestamp DATETIME DEFAULT GETDATE()
);
GO

-- 9. TẠO VIEWS DBO HỖ TRỢ TRUY VẤN NGHĨA DỄ DÀNG (v_*)
CREATE VIEW dbo.v_DIM_Competition AS 
SELECT Competition_ID, Competition_Name, Country_Name, Competition_Type FROM dbo.DIM_Competition;
GO

CREATE VIEW dbo.v_DIM_Club AS 
SELECT Club_ID, Club_Name, Stadium_Name, Stadium_Seats, Coach_Name, Squad_Size FROM dbo.DIM_Club;
GO

CREATE VIEW dbo.v_DIM_Player AS 
SELECT Player_ID, Player_Name, Date_Of_Birth, Age, Country_Of_Citizenship, Main_Position, Sub_Position, Foot, Height_In_Cm FROM dbo.DIM_Player;
GO

CREATE VIEW dbo.v_DIM_Time AS 
SELECT Time_ID, Full_Date, Day_Of_Week, Day, Month, Quarter, Year, Season, Is_Weekend FROM dbo.DIM_Time;
GO

CREATE VIEW dbo.v_FACT_Player_Match_Perf AS 
SELECT Appearance_ID, Player_ID, Club_ID, Opponent_Club_ID, Competition_ID, Game_ID, Time_ID, Minutes_Played, Goals, Assists, Goal_Contributions, Yellow_Cards, Red_Cards, Is_Starter, Is_Home_Game FROM dbo.FACT_Player_Match_Perf;
GO
