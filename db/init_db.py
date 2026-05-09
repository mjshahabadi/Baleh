
from db.database import db_conn

def init_db():
    with db_conn() as conn:
        cur = conn.cursor()

        cur.execute("""
        IF OBJECT_ID('baleh.users', 'U') IS NULL
        CREATE TABLE baleh.users (
            id INT IDENTITY(1,1) PRIMARY KEY,
            bale_user_id NVARCHAR(100),
            first_name NVARCHAR(100),
            username NVARCHAR(100)
        )
        """)

        cur.execute("""
        IF OBJECT_ID('baleh.Plans', 'U') IS NULL
        CREATE TABLE baleh.Plans (
            Id INT IDENTITY PRIMARY KEY,
            Name NVARCHAR(100),
            Price BIGINT,
            DurationDays INT,
            IsActive BIT DEFAULT 1
        )
        """)

        cur.execute("""
        IF OBJECT_ID('baleh.Subscriptions', 'U') IS NULL
        CREATE TABLE baleh.Subscriptions (
            Id INT IDENTITY PRIMARY KEY,
            UserId INT,
            PlanId INT,
            StartDate DATETIME,
            EndDate DATETIME,
            IsActive BIT
        )
        """)

        conn.commit()
