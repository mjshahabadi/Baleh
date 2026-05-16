from db.database import db_conn


ROUTE_CONFIG_LEAVE_DAILY = (
    '{"calendar":"jalali","year":1405,"month":1,"min_year":1405,'
    '"max_year":1405,"week_start":"sat",'
    '"selected_message":"✅ تاریخ مرخصی روزانه انتخاب شد: {date}"}'
)


def _execute(cur, sql, params=None):
    cur.execute(sql, params or ())


def init_db():
    """Create/migrate the minimum SQL Server schema needed by the app.

    The full manually-runnable database script is maintained in
    ``db/schema.sql``. Keep that file updated whenever tables, columns, or seed
    data change.
    """

    with db_conn() as conn:
        cur = conn.cursor()

        _execute(cur, """
        cur.execute("""
        IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'baleh')
            EXEC('CREATE SCHEMA baleh')
        """)

        _execute(cur, """
        cur.execute("""
        IF OBJECT_ID('baleh.users', 'U') IS NULL
        CREATE TABLE baleh.users (
            id INT IDENTITY(1,1) PRIMARY KEY,
            bale_user_id NVARCHAR(3000) NULL,
            first_name NVARCHAR(3000) NULL,
            last_name NVARCHAR(3000) NULL,
            phone_Number NVARCHAR(3000) NULL,
            username NVARCHAR(3000) NULL,
            company_Id BIGINT NULL,
            created_at DATETIME2(7) NOT NULL DEFAULT SYSDATETIME()
        )
        """)

        _execute(cur, """
        IF OBJECT_ID('baleh.menus', 'U') IS NULL
        CREATE TABLE baleh.menus (
            id INT IDENTITY(1,1) PRIMARY KEY,
            menu_name NVARCHAR(100) NOT NULL UNIQUE,
            keyboard_type NVARCHAR(20) NOT NULL DEFAULT 'inline',
            title NVARCHAR(300) NULL,
            parent_menu NVARCHAR(100) NULL,
            sort_order INT NULL,
            is_active BIT NOT NULL DEFAULT 1,
            created_at DATETIME2(7) NOT NULL DEFAULT SYSDATETIME(),
            updated_at DATETIME2(7) NULL
        )
        """)

        _execute(cur, """
        IF OBJECT_ID('baleh.bot_buttons', 'U') IS NULL
        CREATE TABLE baleh.bot_buttons (
            id INT IDENTITY(1,1) PRIMARY KEY,
            menu_name NVARCHAR(100) NULL,
            button_text NVARCHAR(200) NULL,
            icon NVARCHAR(50) NULL,
            callback_data NVARCHAR(100) NULL,
            row_index INT NULL,
            col_index INT NULL,
            row_align NVARCHAR(50) NULL,
            is_active BIT NOT NULL DEFAULT 1,
            created_at DATETIME2(7) NOT NULL DEFAULT SYSDATETIME(),
            updated_at DATETIME2(7) NULL
        )
        """)

        _execute(cur, """
        IF OBJECT_ID('baleh.routes', 'U') IS NULL
        CREATE TABLE baleh.routes (
            id INT IDENTITY(1,1) PRIMARY KEY,
            callback_data NVARCHAR(100) NULL UNIQUE,
            route_type NVARCHAR(50) NULL,
            route_value NVARCHAR(500) NULL,
            is_active BIT NOT NULL DEFAULT 1,
            route_config NVARCHAR(MAX) NULL,
            created_at DATETIME2(7) NOT NULL DEFAULT SYSDATETIME(),
            updated_at DATETIME2(7) NULL
        )
        """)

        _execute(cur, """
        IF OBJECT_ID('baleh.Plans', 'U') IS NULL
        CREATE TABLE baleh.Plans (
            Id INT IDENTITY(1,1) PRIMARY KEY,
            title NVARCHAR(100) NOT NULL,
            Price BIGINT NOT NULL,
            duration_days INT NOT NULL,
            Features NVARCHAR(MAX) NULL,
            IsActive BIT NULL DEFAULT 1
        )
        """)

        _execute(cur, """
        IF OBJECT_ID('baleh.Subscriptions', 'U') IS NULL
        CREATE TABLE baleh.Subscriptions (
            Id INT IDENTITY(1,1) PRIMARY KEY,
            user_id INT NOT NULL,
            plan_id INT NOT NULL,
            start_date DATETIME2(7) NOT NULL,
            end_date DATETIME2(7) NOT NULL,
            is_active BIT NULL DEFAULT 1,
            CreatedAt DATETIME2(7) NULL DEFAULT SYSDATETIME()
        )
        """)

        _execute(cur, """
        IF OBJECT_ID('baleh.Payments', 'U') IS NULL
        CREATE TABLE baleh.Payments (
            Id INT IDENTITY(1,1) PRIMARY KEY,
            UserId INT NULL,
            Amount BIGINT NULL,
            Status NVARCHAR(50) NULL,
            CreatedAt DATETIME2(7) NULL DEFAULT SYSDATETIME()
        )
        """)

        _execute(cur, """
        IF OBJECT_ID('baleh.workflows', 'U') IS NULL
        CREATE TABLE baleh.workflows (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(100) NULL,
            code NVARCHAR(50) NULL UNIQUE
        )
        """)

        _execute(cur, """
        IF OBJECT_ID('baleh.workflow_steps', 'U') IS NULL
        CREATE TABLE baleh.workflow_steps (
            id INT IDENTITY(1,1) PRIMARY KEY,
            workflow_id INT NULL,
            step_code NVARCHAR(50) NULL,
            step_type NVARCHAR(20) NULL,
            message NVARCHAR(MAX) NULL,
            next_step NVARCHAR(50) NULL,
            field_name NVARCHAR(50) NULL,
            is_start BIT NULL DEFAULT 0
        )
        """)

        _execute(cur, """
        IF OBJECT_ID('baleh.user_state', 'U') IS NULL
        CREATE TABLE baleh.user_state (
            id BIGINT IDENTITY(1,1) PRIMARY KEY,
            user_id BIGINT NOT NULL,
            workflow_code NVARCHAR(100) NOT NULL,
            current_step NVARCHAR(100) NOT NULL,
            state_data NVARCHAR(MAX) NULL,
            is_completed BIT NOT NULL DEFAULT 0,
            created_at DATETIME2(7) NOT NULL DEFAULT SYSDATETIME(),
            updated_at DATETIME2(7) NOT NULL DEFAULT SYSDATETIME()
        )
        """)

        # Lightweight migrations for databases created by earlier versions.
        migrations = [
            "IF COL_LENGTH('baleh.menus', 'parent_menu') IS NULL ALTER TABLE baleh.menus ADD parent_menu NVARCHAR(100) NULL",
            "IF COL_LENGTH('baleh.menus', 'sort_order') IS NULL ALTER TABLE baleh.menus ADD sort_order INT NULL",
            "IF COL_LENGTH('baleh.routes', 'route_config') IS NULL ALTER TABLE baleh.routes ADD route_config NVARCHAR(MAX) NULL",
            "IF COL_LENGTH('baleh.Plans', 'title') IS NULL ALTER TABLE baleh.Plans ADD title NVARCHAR(100) NULL",
            "IF COL_LENGTH('baleh.Plans', 'duration_days') IS NULL ALTER TABLE baleh.Plans ADD duration_days INT NULL",
            "IF COL_LENGTH('baleh.Plans', 'Features') IS NULL ALTER TABLE baleh.Plans ADD Features NVARCHAR(MAX) NULL",
            "IF COL_LENGTH('baleh.Subscriptions', 'user_id') IS NULL ALTER TABLE baleh.Subscriptions ADD user_id INT NULL",
            "IF COL_LENGTH('baleh.Subscriptions', 'plan_id') IS NULL ALTER TABLE baleh.Subscriptions ADD plan_id INT NULL",
            "IF COL_LENGTH('baleh.Subscriptions', 'start_date') IS NULL ALTER TABLE baleh.Subscriptions ADD start_date DATETIME2(7) NULL",
            "IF COL_LENGTH('baleh.Subscriptions', 'end_date') IS NULL ALTER TABLE baleh.Subscriptions ADD end_date DATETIME2(7) NULL",
        ]
        for statement in migrations:
            _execute(cur, statement)

        # Backfill canonical plan columns from legacy names when present.
        _execute(cur, """
        IF COL_LENGTH('baleh.Plans', 'Name') IS NOT NULL
            EXEC('UPDATE baleh.Plans SET title = ISNULL(title, Name)')
        """)
        _execute(cur, """
        IF COL_LENGTH('baleh.Plans', 'DurationDays') IS NOT NULL
            EXEC('UPDATE baleh.Plans SET duration_days = ISNULL(duration_days, DurationDays)')
        """)

        seed_statements = [
            ("""
            IF NOT EXISTS (SELECT 1 FROM baleh.menus WHERE menu_name = 'main_menu')
                INSERT INTO baleh.menus (menu_name, keyboard_type, title, parent_menu, sort_order, is_active)
                VALUES ('main_menu', 'inline', N'👋 منوی اصلی:', NULL, 1, 1)
            """, None),
            ("""
            IF NOT EXISTS (SELECT 1 FROM baleh.menus WHERE menu_name = 'subscription_menu')
                INSERT INTO baleh.menus (menu_name, keyboard_type, title, parent_menu, sort_order, is_active)
                VALUES ('subscription_menu', 'inline', N'💳 منوی اشتراک', 'main_menu', 2, 1)
            """, None),
            ("""
            IF NOT EXISTS (SELECT 1 FROM baleh.menus WHERE menu_name = 'leave_menu')
                INSERT INTO baleh.menus (menu_name, keyboard_type, title, parent_menu, sort_order, is_active)
                VALUES ('leave_menu', 'inline', N'📅 منوی مرخصی', 'main_menu', 3, 1)
            """, None),
            ("""
            IF NOT EXISTS (SELECT 1 FROM baleh.bot_buttons WHERE callback_data = 'buy_plan')
                INSERT INTO baleh.bot_buttons (menu_name, button_text, icon, callback_data, row_index, col_index, row_align, is_active)
                VALUES ('main_menu', N'خرید اشتراک', N'💳', 'buy_plan', 0, 0, 'right', 1)
            """, None),
            ("""
            IF NOT EXISTS (SELECT 1 FROM baleh.bot_buttons WHERE callback_data = 'profile')
                INSERT INTO baleh.bot_buttons (menu_name, button_text, icon, callback_data, row_index, col_index, row_align, is_active)
                VALUES ('main_menu', N'پروفایل', N'👤', 'profile', 0, 1, 'right', 1)
            """, None),
            ("""
            IF NOT EXISTS (SELECT 1 FROM baleh.bot_buttons WHERE callback_data = 'support')
                INSERT INTO baleh.bot_buttons (menu_name, button_text, icon, callback_data, row_index, col_index, row_align, is_active)
                VALUES ('main_menu', N'پشتیبانی', N'📞', 'support', 1, 0, 'right', 1)
            """, None),
            ("""
            IF NOT EXISTS (SELECT 1 FROM baleh.bot_buttons WHERE callback_data = 'leave_daily_calendar')
                INSERT INTO baleh.bot_buttons (menu_name, button_text, icon, callback_data, row_index, col_index, row_align, is_active)
                VALUES ('main_menu', N'ثبت مرخصی روزانه', N'📅', 'leave_daily_calendar', 1, 1, 'right', 1)
            """, None),
            ("""
            IF NOT EXISTS (SELECT 1 FROM baleh.routes WHERE callback_data = 'buy_plan')
                INSERT INTO baleh.routes (callback_data, route_type, route_value, route_config, is_active)
                VALUES ('buy_plan', 'message', N'💳 خرید اشتراک', NULL, 1)
            """, None),
            ("""
            IF NOT EXISTS (SELECT 1 FROM baleh.routes WHERE callback_data = 'profile')
                INSERT INTO baleh.routes (callback_data, route_type, route_value, route_config, is_active)
                VALUES ('profile', 'message', N'👤 پروفایل', NULL, 1)
            """, None),
            ("""
            IF NOT EXISTS (SELECT 1 FROM baleh.routes WHERE callback_data = 'support')
                INSERT INTO baleh.routes (callback_data, route_type, route_value, route_config, is_active)
                VALUES ('support', 'message', N'📞 پشتیبانی', NULL, 1)
            """, None),
            ("""
            IF NOT EXISTS (SELECT 1 FROM baleh.routes WHERE callback_data = 'leave_daily_calendar')
                INSERT INTO baleh.routes (callback_data, route_type, route_value, route_config, is_active)
                VALUES ('leave_daily_calendar', 'calendar', N'📅 تاریخ مرخصی روزانه را انتخاب کنید:', ?, 1)
            """, (ROUTE_CONFIG_LEAVE_DAILY,)),
            ("""
            IF NOT EXISTS (SELECT 1 FROM baleh.Plans WHERE title = N'اشتراک یک ماهه')
                INSERT INTO baleh.Plans (title, Price, duration_days, Features, IsActive)
                VALUES (N'اشتراک یک ماهه', 99000, 30, N'دسترسی پایه', 1)
            """, None),
            ("""
            IF NOT EXISTS (SELECT 1 FROM baleh.Plans WHERE title = N'اشتراک سه ماهه')
                INSERT INTO baleh.Plans (title, Price, duration_days, Features, IsActive)
                VALUES (N'اشتراک سه ماهه', 249000, 90, N'دسترسی استاندارد', 1)
            """, None),
            ("""
            IF NOT EXISTS (SELECT 1 FROM baleh.Plans WHERE title = N'اشتراک سالانه')
                INSERT INTO baleh.Plans (title, Price, duration_days, Features, IsActive)
                VALUES (N'اشتراک سالانه', 899000, 365, N'دسترسی کامل', 1)
            """, None),
        ]

        for statement, params in seed_statements:
            _execute(cur, statement, params)
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
            route_config NVARCHAR(MAX) NULL,
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
        IF COL_LENGTH('baleh.routes', 'route_config') IS NULL
            ALTER TABLE baleh.routes ADD route_config NVARCHAR(MAX) NULL
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
        IF NOT EXISTS (
            SELECT 1 FROM baleh.bot_buttons
            WHERE menu_name = 'main_menu' AND callback_data = 'leave_daily_calendar'
        )
            INSERT INTO baleh.bot_buttons
                (menu_name, button_text, icon, callback_data, row_index, col_index, row_align, is_active)
            VALUES
                ('main_menu', N'ثبت مرخصی روزانه', N'📅', 'leave_daily_calendar', 1, 1, 'right', 1)
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

        cur.execute("""
        IF NOT EXISTS (SELECT 1 FROM baleh.routes WHERE callback_data = 'leave_daily_calendar')
            INSERT INTO baleh.routes (callback_data, route_type, route_value, route_config, is_active)
            VALUES (
                'leave_daily_calendar',
                'calendar',
                N'📅 تاریخ مرخصی روزانه را انتخاب کنید:',
                N'{"calendar":"jalali","year":1405,"month":1,"min_year":1405,"max_year":1405,"week_start":"sat","selected_message":"✅ تاریخ مرخصی روزانه انتخاب شد: {date}"}',
                1
            )
        """)

        conn.commit()
