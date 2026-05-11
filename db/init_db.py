from db.database import db_conn


def init_db():
    with db_conn() as conn:
        cur = conn.cursor()

        cur.execute("""
        IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'baleh')
            EXEC('CREATE SCHEMA baleh')
        """)

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

        cur.execute("""
        IF OBJECT_ID('baleh.menus', 'U') IS NULL
        CREATE TABLE baleh.menus (
            id INT IDENTITY(1,1) PRIMARY KEY,
            menu_name NVARCHAR(100) NOT NULL UNIQUE,
            keyboard_type NVARCHAR(20) NOT NULL DEFAULT 'inline',
            title NVARCHAR(500) NOT NULL,
            is_active BIT NOT NULL DEFAULT 1,
            created_at DATETIME NOT NULL DEFAULT GETDATE(),
            updated_at DATETIME NULL
        )
        """)

        cur.execute("""
        IF OBJECT_ID('baleh.bot_buttons', 'U') IS NULL
        CREATE TABLE baleh.bot_buttons (
            id INT IDENTITY(1,1) PRIMARY KEY,
            menu_name NVARCHAR(100) NOT NULL,
            button_text NVARCHAR(200) NOT NULL,
            icon NVARCHAR(50) NULL,
            callback_data NVARCHAR(300) NOT NULL,
            row_index INT NOT NULL DEFAULT 0,
            col_index INT NOT NULL DEFAULT 0,
            row_align NVARCHAR(20) NOT NULL DEFAULT 'right',
            is_active BIT NOT NULL DEFAULT 1,
            created_at DATETIME NOT NULL DEFAULT GETDATE(),
            updated_at DATETIME NULL
        )
        """)

        cur.execute("""
        IF OBJECT_ID('baleh.routes', 'U') IS NULL
        CREATE TABLE baleh.routes (
            id INT IDENTITY(1,1) PRIMARY KEY,
            callback_data NVARCHAR(300) NOT NULL UNIQUE,
            route_type NVARCHAR(50) NOT NULL,
            route_value NVARCHAR(500) NOT NULL,
            is_active BIT NOT NULL DEFAULT 1,
            created_at DATETIME NOT NULL DEFAULT GETDATE(),
            updated_at DATETIME NULL
        )
        """)

        cur.execute("""
        IF COL_LENGTH('baleh.menus', 'is_active') IS NULL
            ALTER TABLE baleh.menus ADD is_active BIT NOT NULL CONSTRAINT DF_baleh_menus_is_active DEFAULT 1
        """)

        cur.execute("""
        IF COL_LENGTH('baleh.bot_buttons', 'is_active') IS NULL
            ALTER TABLE baleh.bot_buttons ADD is_active BIT NOT NULL CONSTRAINT DF_baleh_bot_buttons_is_active DEFAULT 1
        """)

        cur.execute("""
        IF COL_LENGTH('baleh.routes', 'is_active') IS NULL
            ALTER TABLE baleh.routes ADD is_active BIT NOT NULL CONSTRAINT DF_baleh_routes_is_active DEFAULT 1
        """)

        cur.execute("""
        IF NOT EXISTS (SELECT 1 FROM baleh.menus WHERE menu_name = 'main_menu')
        INSERT INTO baleh.menus (menu_name, keyboard_type, title, is_active)
        VALUES ('main_menu', 'inline', N'👋 منوی اصلی:', 1)
        """)

        cur.execute("""
        IF NOT EXISTS (SELECT 1 FROM baleh.bot_buttons WHERE menu_name = 'main_menu')
        BEGIN
            INSERT INTO baleh.bot_buttons
                (menu_name, button_text, icon, callback_data, row_index, col_index, row_align, is_active)
            VALUES
                ('main_menu', N'خرید اشتراک', N'💳', 'buy_plan', 0, 0, 'right', 1),
                ('main_menu', N'پروفایل', N'👤', 'profile', 0, 1, 'right', 1),
                ('main_menu', N'پشتیبانی', N'📞', 'support', 1, 0, 'right', 1)
        END
        """)

        cur.execute("""
        IF NOT EXISTS (SELECT 1 FROM baleh.routes WHERE callback_data = 'buy_plan')
            INSERT INTO baleh.routes (callback_data, route_type, route_value, is_active)
            VALUES ('buy_plan', 'message', N'💳 خرید اشتراک', 1)
        """)

        cur.execute("""
        IF NOT EXISTS (SELECT 1 FROM baleh.routes WHERE callback_data = 'profile')
            INSERT INTO baleh.routes (callback_data, route_type, route_value, is_active)
            VALUES ('profile', 'message', N'👤 پروفایل', 1)
        """)

        cur.execute("""
        IF NOT EXISTS (SELECT 1 FROM baleh.routes WHERE callback_data = 'support')
            INSERT INTO baleh.routes (callback_data, route_type, route_value, is_active)
            VALUES ('support', 'message', N'📞 پشتیبانی', 1)
        """)

        conn.commit()
