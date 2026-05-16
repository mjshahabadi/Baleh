/*
    Baleh Bot SQL Server schema and seed data
    ------------------------------------------------------------
    این فایل مرجع ساخت/به‌روزرسانی دیتابیس برنامه است.
    از این به بعد اگر جدول/فیلد/دیتاتایپ جدیدی لازم شد، همین فایل را به‌روزرسانی کنید و روی SQL Server اجرا کنید.

    ویژگی‌ها:
    - اجرای امن و چندباره تا حد امکان (idempotent)
    - ساخت تمام جداول مورد استفاده سورس
    - افزودن ستون‌های لازم در صورت نبودن
    - درج حداقل سه رکورد نمونه برای جداول اصلی/تنظیمی و داده‌های نمونه
*/

IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = N'baleh')
    EXEC(N'CREATE SCHEMA baleh');
GO

/* ============================================================
   USERS
============================================================ */
IF OBJECT_ID(N'baleh.users', N'U') IS NULL
BEGIN
    CREATE TABLE baleh.users (
        id INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_baleh_users PRIMARY KEY CLUSTERED,
        bale_user_id NVARCHAR(3000) NULL,
        first_name NVARCHAR(3000) NULL,
        last_name NVARCHAR(3000) NULL,
        phone_Number NVARCHAR(3000) NULL,
        username NVARCHAR(3000) NULL,
        company_Id BIGINT NULL,
        created_at DATETIME2(7) NOT NULL CONSTRAINT DF_baleh_users_created_at DEFAULT (SYSDATETIME())
    );
END;
GO

IF COL_LENGTH(N'baleh.users', N'last_name') IS NULL ALTER TABLE baleh.users ADD last_name NVARCHAR(3000) NULL;
IF COL_LENGTH(N'baleh.users', N'phone_Number') IS NULL ALTER TABLE baleh.users ADD phone_Number NVARCHAR(3000) NULL;
IF COL_LENGTH(N'baleh.users', N'company_Id') IS NULL ALTER TABLE baleh.users ADD company_Id BIGINT NULL;
IF COL_LENGTH(N'baleh.users', N'created_at') IS NULL ALTER TABLE baleh.users ADD created_at DATETIME2(7) NOT NULL CONSTRAINT DF_baleh_users_created_at DEFAULT (SYSDATETIME());
GO

/* ============================================================
   MENUS
============================================================ */
IF OBJECT_ID(N'baleh.menus', N'U') IS NULL
BEGIN
    CREATE TABLE baleh.menus (
        id INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_baleh_menus PRIMARY KEY CLUSTERED,
        menu_name NVARCHAR(100) NOT NULL,
        keyboard_type NVARCHAR(20) NOT NULL,
        title NVARCHAR(300) NULL,
        parent_menu NVARCHAR(100) NULL,
        sort_order INT NULL,
        is_active BIT NOT NULL CONSTRAINT DF_baleh_menus_is_active DEFAULT ((1)),
        created_at DATETIME2(7) NOT NULL CONSTRAINT DF_baleh_menus_created_at DEFAULT (SYSDATETIME()),
        updated_at DATETIME2(7) NULL,
        CONSTRAINT UQ_baleh_menus_menu_name UNIQUE NONCLUSTERED (menu_name)
    );
END;
GO

IF COL_LENGTH(N'baleh.menus', N'parent_menu') IS NULL ALTER TABLE baleh.menus ADD parent_menu NVARCHAR(100) NULL;
IF COL_LENGTH(N'baleh.menus', N'sort_order') IS NULL ALTER TABLE baleh.menus ADD sort_order INT NULL;
IF COL_LENGTH(N'baleh.menus', N'updated_at') IS NULL ALTER TABLE baleh.menus ADD updated_at DATETIME2(7) NULL;
GO

/* ============================================================
   BOT BUTTONS
============================================================ */
IF OBJECT_ID(N'baleh.bot_buttons', N'U') IS NULL
BEGIN
    CREATE TABLE baleh.bot_buttons (
        id INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_baleh_bot_buttons PRIMARY KEY CLUSTERED,
        menu_name NVARCHAR(100) NULL,
        button_text NVARCHAR(200) NULL,
        icon NVARCHAR(50) NULL,
        callback_data NVARCHAR(100) NULL,
        row_index INT NULL,
        col_index INT NULL,
        row_align NVARCHAR(50) NULL,
        is_active BIT NOT NULL CONSTRAINT DF_baleh_bot_buttons_is_active DEFAULT ((1)),
        created_at DATETIME2(7) NOT NULL CONSTRAINT DF_baleh_bot_buttons_created_at DEFAULT (SYSDATETIME()),
        updated_at DATETIME2(7) NULL
    );
END;
GO

IF COL_LENGTH(N'baleh.bot_buttons', N'created_at') IS NULL ALTER TABLE baleh.bot_buttons ADD created_at DATETIME2(7) NOT NULL CONSTRAINT DF_baleh_bot_buttons_created_at DEFAULT (SYSDATETIME());
IF COL_LENGTH(N'baleh.bot_buttons', N'updated_at') IS NULL ALTER TABLE baleh.bot_buttons ADD updated_at DATETIME2(7) NULL;
ALTER TABLE baleh.bot_buttons ALTER COLUMN callback_data NVARCHAR(100) NULL;
ALTER TABLE baleh.bot_buttons ALTER COLUMN row_align NVARCHAR(50) NULL;
GO

/* ============================================================
   ROUTES
============================================================ */
IF OBJECT_ID(N'baleh.routes', N'U') IS NULL
BEGIN
    CREATE TABLE baleh.routes (
        id INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_baleh_routes PRIMARY KEY CLUSTERED,
        callback_data NVARCHAR(100) NULL,
        route_type NVARCHAR(50) NULL,
        route_value NVARCHAR(500) NULL,
        is_active BIT NOT NULL CONSTRAINT DF_baleh_routes_is_active DEFAULT ((1)),
        route_config NVARCHAR(MAX) NULL,
        created_at DATETIME2(7) NOT NULL CONSTRAINT DF_baleh_routes_created_at DEFAULT (SYSDATETIME()),
        updated_at DATETIME2(7) NULL,
        CONSTRAINT UQ_baleh_routes_callback_data UNIQUE NONCLUSTERED (callback_data)
    ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY];
END;
GO

IF COL_LENGTH(N'baleh.routes', N'route_config') IS NULL ALTER TABLE baleh.routes ADD route_config NVARCHAR(MAX) NULL;
IF COL_LENGTH(N'baleh.routes', N'created_at') IS NULL ALTER TABLE baleh.routes ADD created_at DATETIME2(7) NOT NULL CONSTRAINT DF_baleh_routes_created_at DEFAULT (SYSDATETIME());
IF COL_LENGTH(N'baleh.routes', N'updated_at') IS NULL ALTER TABLE baleh.routes ADD updated_at DATETIME2(7) NULL;
ALTER TABLE baleh.routes ALTER COLUMN route_value NVARCHAR(500) NULL;
GO

/* ============================================================
   PLANS
============================================================ */
IF OBJECT_ID(N'baleh.Plans', N'U') IS NULL
BEGIN
    CREATE TABLE baleh.Plans (
        Id INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_baleh_Plans PRIMARY KEY CLUSTERED,
        title NVARCHAR(100) NOT NULL,
        Price BIGINT NOT NULL,
        duration_days INT NOT NULL,
        Features NVARCHAR(MAX) NULL,
        IsActive BIT NULL CONSTRAINT DF_baleh_Plans_IsActive DEFAULT ((1))
    ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY];
END;
GO

IF COL_LENGTH(N'baleh.Plans', N'title') IS NULL ALTER TABLE baleh.Plans ADD title NVARCHAR(100) NULL;
IF COL_LENGTH(N'baleh.Plans', N'duration_days') IS NULL ALTER TABLE baleh.Plans ADD duration_days INT NULL;
IF COL_LENGTH(N'baleh.Plans', N'Features') IS NULL ALTER TABLE baleh.Plans ADD Features NVARCHAR(MAX) NULL;
IF COL_LENGTH(N'baleh.Plans', N'Name') IS NOT NULL EXEC(N'UPDATE baleh.Plans SET title = ISNULL(title, Name)');
IF COL_LENGTH(N'baleh.Plans', N'DurationDays') IS NOT NULL EXEC(N'UPDATE baleh.Plans SET duration_days = ISNULL(duration_days, DurationDays)');
GO

/* ============================================================
   SUBSCRIPTIONS
============================================================ */
IF OBJECT_ID(N'baleh.Subscriptions', N'U') IS NULL
BEGIN
    CREATE TABLE baleh.Subscriptions (
        Id INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_baleh_Subscriptions PRIMARY KEY CLUSTERED,
        user_id INT NOT NULL,
        plan_id INT NOT NULL,
        start_date DATETIME2(7) NOT NULL,
        end_date DATETIME2(7) NOT NULL,
        is_active BIT NULL CONSTRAINT DF_baleh_Subscriptions_is_active DEFAULT ((1)),
        CreatedAt DATETIME2(7) NULL CONSTRAINT DF_baleh_Subscriptions_CreatedAt DEFAULT (SYSDATETIME())
    );
END;
GO

IF COL_LENGTH(N'baleh.Subscriptions', N'user_id') IS NULL ALTER TABLE baleh.Subscriptions ADD user_id INT NULL;
IF COL_LENGTH(N'baleh.Subscriptions', N'plan_id') IS NULL ALTER TABLE baleh.Subscriptions ADD plan_id INT NULL;
IF COL_LENGTH(N'baleh.Subscriptions', N'start_date') IS NULL ALTER TABLE baleh.Subscriptions ADD start_date DATETIME2(7) NULL;
IF COL_LENGTH(N'baleh.Subscriptions', N'end_date') IS NULL ALTER TABLE baleh.Subscriptions ADD end_date DATETIME2(7) NULL;
IF COL_LENGTH(N'baleh.Subscriptions', N'CreatedAt') IS NULL ALTER TABLE baleh.Subscriptions ADD CreatedAt DATETIME2(7) NULL CONSTRAINT DF_baleh_Subscriptions_CreatedAt DEFAULT (SYSDATETIME());
GO

/* ============================================================
   PAYMENTS
============================================================ */
IF OBJECT_ID(N'baleh.Payments', N'U') IS NULL
BEGIN
    CREATE TABLE baleh.Payments (
        Id INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_baleh_Payments PRIMARY KEY CLUSTERED,
        UserId INT NULL,
        Amount BIGINT NULL,
        Status NVARCHAR(50) NULL,
        CreatedAt DATETIME2(7) NULL CONSTRAINT DF_baleh_Payments_CreatedAt DEFAULT (SYSDATETIME())
    );
END;
GO

/* ============================================================
   WORKFLOWS
============================================================ */
IF OBJECT_ID(N'baleh.workflows', N'U') IS NULL
BEGIN
    CREATE TABLE baleh.workflows (
        id INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_baleh_workflows PRIMARY KEY CLUSTERED,
        name NVARCHAR(100) NULL,
        code NVARCHAR(50) NULL,
        CONSTRAINT UQ_baleh_workflows_code UNIQUE NONCLUSTERED (code)
    );
END;
GO

IF OBJECT_ID(N'baleh.workflow_steps', N'U') IS NULL
BEGIN
    CREATE TABLE baleh.workflow_steps (
        id INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_baleh_workflow_steps PRIMARY KEY CLUSTERED,
        workflow_id INT NULL,
        step_code NVARCHAR(50) NULL,
        step_type NVARCHAR(20) NULL,
        message NVARCHAR(MAX) NULL,
        next_step NVARCHAR(50) NULL,
        field_name NVARCHAR(50) NULL,
        is_start BIT NULL CONSTRAINT DF_baleh_workflow_steps_is_start DEFAULT ((0))
    ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY];
END;
GO

/* ============================================================
   USER STATE
============================================================ */
IF OBJECT_ID(N'baleh.user_state', N'U') IS NULL
BEGIN
    CREATE TABLE baleh.user_state (
        id BIGINT IDENTITY(1,1) NOT NULL CONSTRAINT PK_baleh_user_state PRIMARY KEY CLUSTERED,
        user_id BIGINT NOT NULL,
        workflow_code NVARCHAR(100) NOT NULL,
        current_step NVARCHAR(100) NOT NULL,
        state_data NVARCHAR(MAX) NULL,
        is_completed BIT NOT NULL CONSTRAINT DF_baleh_user_state_is_completed DEFAULT ((0)),
        created_at DATETIME2(7) NOT NULL CONSTRAINT DF_baleh_user_state_created_at DEFAULT (SYSDATETIME()),
        updated_at DATETIME2(7) NOT NULL CONSTRAINT DF_baleh_user_state_updated_at DEFAULT (SYSDATETIME())
    ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY];
END;
GO

/* ============================================================
   SEED DATA: MENUS (>= 3)
============================================================ */
IF NOT EXISTS (SELECT 1 FROM baleh.menus WHERE menu_name = N'main_menu')
    INSERT INTO baleh.menus (menu_name, keyboard_type, title, parent_menu, sort_order, is_active)
    VALUES (N'main_menu', N'inline', N'👋 منوی اصلی:', NULL, 1, 1);

IF NOT EXISTS (SELECT 1 FROM baleh.menus WHERE menu_name = N'subscription_menu')
    INSERT INTO baleh.menus (menu_name, keyboard_type, title, parent_menu, sort_order, is_active)
    VALUES (N'subscription_menu', N'inline', N'💳 منوی اشتراک', N'main_menu', 2, 1);

IF NOT EXISTS (SELECT 1 FROM baleh.menus WHERE menu_name = N'leave_menu')
    INSERT INTO baleh.menus (menu_name, keyboard_type, title, parent_menu, sort_order, is_active)
    VALUES (N'leave_menu', N'inline', N'📅 منوی مرخصی', N'main_menu', 3, 1);
GO

/* ============================================================
   SEED DATA: BOT BUTTONS (>= 3)
============================================================ */
IF NOT EXISTS (SELECT 1 FROM baleh.bot_buttons WHERE callback_data = N'buy_plan')
    INSERT INTO baleh.bot_buttons (menu_name, button_text, icon, callback_data, row_index, col_index, row_align, is_active)
    VALUES (N'main_menu', N'خرید اشتراک', N'💳', N'buy_plan', 0, 0, N'right', 1);

IF NOT EXISTS (SELECT 1 FROM baleh.bot_buttons WHERE callback_data = N'profile')
    INSERT INTO baleh.bot_buttons (menu_name, button_text, icon, callback_data, row_index, col_index, row_align, is_active)
    VALUES (N'main_menu', N'پروفایل', N'👤', N'profile', 0, 1, N'right', 1);

IF NOT EXISTS (SELECT 1 FROM baleh.bot_buttons WHERE callback_data = N'support')
    INSERT INTO baleh.bot_buttons (menu_name, button_text, icon, callback_data, row_index, col_index, row_align, is_active)
    VALUES (N'main_menu', N'پشتیبانی', N'📞', N'support', 1, 0, N'right', 1);

IF NOT EXISTS (SELECT 1 FROM baleh.bot_buttons WHERE callback_data = N'leave_daily_calendar')
    INSERT INTO baleh.bot_buttons (menu_name, button_text, icon, callback_data, row_index, col_index, row_align, is_active)
    VALUES (N'main_menu', N'ثبت مرخصی روزانه', N'📅', N'leave_daily_calendar', 1, 1, N'right', 1);
GO

/* ============================================================
   SEED DATA: ROUTES (>= 3)
============================================================ */
IF NOT EXISTS (SELECT 1 FROM baleh.routes WHERE callback_data = N'buy_plan')
    INSERT INTO baleh.routes (callback_data, route_type, route_value, route_config, is_active)
    VALUES (N'buy_plan', N'message', N'💳 خرید اشتراک', NULL, 1);

IF NOT EXISTS (SELECT 1 FROM baleh.routes WHERE callback_data = N'profile')
    INSERT INTO baleh.routes (callback_data, route_type, route_value, route_config, is_active)
    VALUES (N'profile', N'message', N'👤 پروفایل', NULL, 1);

IF NOT EXISTS (SELECT 1 FROM baleh.routes WHERE callback_data = N'support')
    INSERT INTO baleh.routes (callback_data, route_type, route_value, route_config, is_active)
    VALUES (N'support', N'message', N'📞 پشتیبانی', NULL, 1);

IF NOT EXISTS (SELECT 1 FROM baleh.routes WHERE callback_data = N'leave_daily_calendar')
    INSERT INTO baleh.routes (callback_data, route_type, route_value, route_config, is_active)
    VALUES (
        N'leave_daily_calendar',
        N'calendar',
        N'📅 تاریخ مرخصی روزانه را انتخاب کنید:',
        N'{"calendar":"jalali","year":1405,"month":1,"min_year":1405,"max_year":1405,"week_start":"sat","selected_message":"✅ تاریخ مرخصی روزانه انتخاب شد: {date}"}',
        1
    );
GO

/* ============================================================
   SEED DATA: PLANS (>= 3)
============================================================ */
IF NOT EXISTS (SELECT 1 FROM baleh.Plans WHERE title = N'اشتراک یک ماهه')
    INSERT INTO baleh.Plans (title, Price, duration_days, Features, IsActive)
    VALUES (N'اشتراک یک ماهه', 99000, 30, N'دسترسی پایه', 1);

IF NOT EXISTS (SELECT 1 FROM baleh.Plans WHERE title = N'اشتراک سه ماهه')
    INSERT INTO baleh.Plans (title, Price, duration_days, Features, IsActive)
    VALUES (N'اشتراک سه ماهه', 249000, 90, N'دسترسی استاندارد', 1);

IF NOT EXISTS (SELECT 1 FROM baleh.Plans WHERE title = N'اشتراک سالانه')
    INSERT INTO baleh.Plans (title, Price, duration_days, Features, IsActive)
    VALUES (N'اشتراک سالانه', 899000, 365, N'دسترسی کامل', 1);
GO

/* ============================================================
   SEED DATA: USERS / PAYMENTS / SUBSCRIPTIONS (>= 3 sample rows)
============================================================ */
IF NOT EXISTS (SELECT 1 FROM baleh.users WHERE bale_user_id = N'1001')
    INSERT INTO baleh.users (bale_user_id, first_name, last_name, phone_Number, username, company_Id)
    VALUES (N'1001', N'کاربر', N'نمونه یک', N'09120000001', N'sample_user_1', 1);

IF NOT EXISTS (SELECT 1 FROM baleh.users WHERE bale_user_id = N'1002')
    INSERT INTO baleh.users (bale_user_id, first_name, last_name, phone_Number, username, company_Id)
    VALUES (N'1002', N'کاربر', N'نمونه دو', N'09120000002', N'sample_user_2', 1);

IF NOT EXISTS (SELECT 1 FROM baleh.users WHERE bale_user_id = N'1003')
    INSERT INTO baleh.users (bale_user_id, first_name, last_name, phone_Number, username, company_Id)
    VALUES (N'1003', N'کاربر', N'نمونه سه', N'09120000003', N'sample_user_3', 1);
GO

DECLARE @plan1 INT = (SELECT TOP 1 Id FROM baleh.Plans WHERE title = N'اشتراک یک ماهه');
DECLARE @plan2 INT = (SELECT TOP 1 Id FROM baleh.Plans WHERE title = N'اشتراک سه ماهه');
DECLARE @plan3 INT = (SELECT TOP 1 Id FROM baleh.Plans WHERE title = N'اشتراک سالانه');
DECLARE @user1 INT = (SELECT TOP 1 id FROM baleh.users WHERE bale_user_id = N'1001');
DECLARE @user2 INT = (SELECT TOP 1 id FROM baleh.users WHERE bale_user_id = N'1002');
DECLARE @user3 INT = (SELECT TOP 1 id FROM baleh.users WHERE bale_user_id = N'1003');

IF NOT EXISTS (SELECT 1 FROM baleh.Subscriptions WHERE user_id = @user1 AND plan_id = @plan1)
    INSERT INTO baleh.Subscriptions (user_id, plan_id, start_date, end_date, is_active)
    VALUES (@user1, @plan1, SYSDATETIME(), DATEADD(DAY, 30, SYSDATETIME()), 1);

IF NOT EXISTS (SELECT 1 FROM baleh.Subscriptions WHERE user_id = @user2 AND plan_id = @plan2)
    INSERT INTO baleh.Subscriptions (user_id, plan_id, start_date, end_date, is_active)
    VALUES (@user2, @plan2, SYSDATETIME(), DATEADD(DAY, 90, SYSDATETIME()), 1);

IF NOT EXISTS (SELECT 1 FROM baleh.Subscriptions WHERE user_id = @user3 AND plan_id = @plan3)
    INSERT INTO baleh.Subscriptions (user_id, plan_id, start_date, end_date, is_active)
    VALUES (@user3, @plan3, SYSDATETIME(), DATEADD(DAY, 365, SYSDATETIME()), 1);

IF NOT EXISTS (SELECT 1 FROM baleh.Payments WHERE UserId = @user1 AND Amount = 99000)
    INSERT INTO baleh.Payments (UserId, Amount, Status) VALUES (@user1, 99000, N'paid');

IF NOT EXISTS (SELECT 1 FROM baleh.Payments WHERE UserId = @user2 AND Amount = 249000)
    INSERT INTO baleh.Payments (UserId, Amount, Status) VALUES (@user2, 249000, N'paid');

IF NOT EXISTS (SELECT 1 FROM baleh.Payments WHERE UserId = @user3 AND Amount = 899000)
    INSERT INTO baleh.Payments (UserId, Amount, Status) VALUES (@user3, 899000, N'paid');
GO

/* ============================================================
   SEED DATA: WORKFLOWS / WORKFLOW_STEPS (>= 3 steps)
============================================================ */
IF NOT EXISTS (SELECT 1 FROM baleh.workflows WHERE code = N'leave_request')
    INSERT INTO baleh.workflows (name, code) VALUES (N'ثبت مرخصی', N'leave_request');

IF NOT EXISTS (SELECT 1 FROM baleh.workflows WHERE code = N'support_request')
    INSERT INTO baleh.workflows (name, code) VALUES (N'درخواست پشتیبانی', N'support_request');

IF NOT EXISTS (SELECT 1 FROM baleh.workflows WHERE code = N'profile_update')
    INSERT INTO baleh.workflows (name, code) VALUES (N'تکمیل پروفایل', N'profile_update');
GO

DECLARE @leave_workflow_id INT = (SELECT TOP 1 id FROM baleh.workflows WHERE code = N'leave_request');

IF NOT EXISTS (SELECT 1 FROM baleh.workflow_steps WHERE workflow_id = @leave_workflow_id AND step_code = N'start_date')
    INSERT INTO baleh.workflow_steps (workflow_id, step_code, step_type, message, next_step, field_name, is_start)
    VALUES (@leave_workflow_id, N'start_date', N'input', N'📅 تاریخ شروع مرخصی را وارد کنید:', N'end_date', N'start_date', 1);

IF NOT EXISTS (SELECT 1 FROM baleh.workflow_steps WHERE workflow_id = @leave_workflow_id AND step_code = N'end_date')
    INSERT INTO baleh.workflow_steps (workflow_id, step_code, step_type, message, next_step, field_name, is_start)
    VALUES (@leave_workflow_id, N'end_date', N'input', N'📅 تاریخ پایان مرخصی را وارد کنید:', N'reason', N'end_date', 0);

IF NOT EXISTS (SELECT 1 FROM baleh.workflow_steps WHERE workflow_id = @leave_workflow_id AND step_code = N'reason')
    INSERT INTO baleh.workflow_steps (workflow_id, step_code, step_type, message, next_step, field_name, is_start)
    VALUES (@leave_workflow_id, N'reason', N'input', N'📝 علت مرخصی را وارد کنید:', N'END', N'reason', 0);
GO

/* ============================================================
   SEED DATA: USER_STATE (>= 3 sample rows, optional sample states)
============================================================ */
IF NOT EXISTS (SELECT 1 FROM baleh.user_state WHERE user_id = 1001)
    INSERT INTO baleh.user_state (user_id, workflow_code, current_step, state_data, is_completed)
    VALUES (1001, N'leave_request', N'start_date', N'{}', 0);

IF NOT EXISTS (SELECT 1 FROM baleh.user_state WHERE user_id = 1002)
    INSERT INTO baleh.user_state (user_id, workflow_code, current_step, state_data, is_completed)
    VALUES (1002, N'support_request', N'description', N'{}', 0);

IF NOT EXISTS (SELECT 1 FROM baleh.user_state WHERE user_id = 1003)
    INSERT INTO baleh.user_state (user_id, workflow_code, current_step, state_data, is_completed)
    VALUES (1003, N'profile_update', N'phone', N'{}', 0);
GO
