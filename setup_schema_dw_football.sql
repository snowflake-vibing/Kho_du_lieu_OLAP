-- ===============================================================================
-- FILE SQL: DROP VÀ TẠO LẠI TOÀN BỘ CÁC BẢNG DBO TRONG KHO DỮ LIỆU DW_Football_Transfermarkt
-- ===============================================================================

USE DW_Football_Transfermarkt;
GO

-- 1. XÓA CÁC BẢNG CŨ THEO ĐÚNG THỨ TỰ (FACT TRƯỚC, STAGING VÀ DIM SAU)
IF OBJECT_ID('dbo.FACT_Player_Match_Perf', 'U') IS NOT NULL DROP TABLE dbo.FACT_Player_Match_Perf;
IF OBJECT_ID('dbo.STG_Appearances', 'U') IS NOT NULL DROP TABLE dbo.STG_Appearances;
IF OBJECT_ID('dbo.DIM_Player', 'U') IS NOT NULL DROP TABLE dbo.DIM_Player;
IF OBJECT_ID('dbo.DIM_Club', 'U') IS NOT NULL DROP TABLE dbo.DIM_Club;
IF OBJECT_ID('dbo.DIM_Competition', 'U') IS NOT NULL DROP TABLE dbo.DIM_Competition;
IF OBJECT_ID('dbo.DIM_Game', 'U') IS NOT NULL DROP TABLE dbo.DIM_Game;
IF OBJECT_ID('dbo.DIM_Time', 'U') IS NOT NULL DROP TABLE dbo.DIM_Time;
GO

-- 2. TẠO BẢNG DIMENSION (DIM_Competition)
CREATE TABLE dbo.DIM_Competition (
    Competition_SK INT IDENTITY(1,1) CONSTRAINT PK_DIM_Competition PRIMARY KEY,
    Competition_ID NVARCHAR(100) NOT NULL CONSTRAINT UQ_DIM_Competition_ID UNIQUE,
    Competition_Name NVARCHAR(200) NULL,
    Country_Name NVARCHAR(200) NULL,
    Competition_Type NVARCHAR(100) NULL
);
GO

-- 3. TẠO BẢNG DIMENSION (DIM_Club)
CREATE TABLE dbo.DIM_Club (
    Club_SK INT IDENTITY(1,1) CONSTRAINT PK_DIM_Club PRIMARY KEY,
    Club_ID INT NOT NULL CONSTRAINT UQ_DIM_Club_ID UNIQUE,
    Club_Name NVARCHAR(200) NULL,
    Stadium_Name NVARCHAR(200) NULL,
    Stadium_Seats INT NULL,
    Coach_Name NVARCHAR(200) NULL,
    Squad_Size INT NULL
);
GO

-- 4. TẠO BẢNG DIMENSION (DIM_Player)
CREATE TABLE dbo.DIM_Player (
    Player_SK INT IDENTITY(1,1) CONSTRAINT PK_DIM_Player PRIMARY KEY,
    Player_ID INT NOT NULL CONSTRAINT UQ_DIM_Player_ID UNIQUE,
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

-- 5. TẠO BẢNG DIMENSION (DIM_Game)
CREATE TABLE dbo.DIM_Game (
    Game_SK INT IDENTITY(1,1) CONSTRAINT PK_DIM_Game PRIMARY KEY,
    Game_ID INT NOT NULL CONSTRAINT UQ_DIM_Game_ID UNIQUE,
    Season INT NULL,
    Round NVARCHAR(100) NULL,
    Home_Club_ID INT NULL,
    Away_Club_ID INT NULL,
    Home_Club_Goals INT NULL,
    Away_Club_Goals INT NULL,
    Stadium NVARCHAR(200) NULL
);
GO

-- 6. TẠO BẢNG DIMENSION (DIM_Time)
CREATE TABLE dbo.DIM_Time (
    Time_SK INT IDENTITY(1,1) CONSTRAINT PK_DIM_Time PRIMARY KEY,
    Time_ID INT NOT NULL CONSTRAINT UQ_DIM_Time_ID UNIQUE,
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

-- 7. TẠO BẢNG STAGING (STG_Appearances)
CREATE TABLE dbo.STG_Appearances (
    appearance_id VARCHAR(100),
    game_id INT,
    player_id INT,
    player_club_id INT,
    player_current_club_id INT,
    date_str VARCHAR(100),
    player_name NVARCHAR(200),
    competition_id VARCHAR(100),
    yellow_cards INT,
    red_cards INT,
    goals INT,
    assists INT,
    minutes_played INT
);
GO

-- 8. TẠO BẢNG FACT (FACT_Player_Match_Perf)
CREATE TABLE dbo.FACT_Player_Match_Perf (
    Appearance_ID INT IDENTITY(1,1) CONSTRAINT PK_FACT_Player_Match_Perf PRIMARY KEY,
    Player_SK INT NULL,
    Club_SK INT NULL,
    Opponent_Club_SK INT NULL,
    Competition_SK INT NULL,
    Game_SK INT NULL,
    Time_SK INT NULL,
    Game_ID INT NOT NULL,
    Minutes_Played INT DEFAULT 0,
    Goals INT DEFAULT 0,
    Assists INT DEFAULT 0,
    Goal_Contributions INT DEFAULT 0,
    Yellow_Cards INT DEFAULT 0,
    Red_Cards INT DEFAULT 0,
    Is_Starter INT DEFAULT 0,
    Is_Home_Game INT DEFAULT 0,

    CONSTRAINT FK_Fact_Player FOREIGN KEY (Player_SK) REFERENCES dbo.DIM_Player(Player_SK),
    CONSTRAINT FK_Fact_Club FOREIGN KEY (Club_SK) REFERENCES dbo.DIM_Club(Club_SK),
    CONSTRAINT FK_Fact_Opponent_Club FOREIGN KEY (Opponent_Club_SK) REFERENCES dbo.DIM_Club(Club_SK),
    CONSTRAINT FK_Fact_Competition FOREIGN KEY (Competition_SK) REFERENCES dbo.DIM_Competition(Competition_SK),
    CONSTRAINT FK_Fact_Game FOREIGN KEY (Game_SK) REFERENCES dbo.DIM_Game(Game_SK),
    CONSTRAINT FK_Fact_Time FOREIGN KEY (Time_SK) REFERENCES dbo.DIM_Time(Time_SK)
);
GO
