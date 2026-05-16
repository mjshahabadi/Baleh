# Dynamic bot actions from database

The bot UI stays dynamic by separating each button into two database records:

1. `baleh.bot_buttons` controls where the button appears, its caption, icon, row, and column.
2. `baleh.routes` controls what the button does through `route_type`, `route_value`, and optional JSON in `route_config`.

This means adding, removing, or moving buttons only requires database changes. New action families can be reused by configuration without writing one Python handler per button.

## Supported route types

| `route_type` | Meaning |
| --- | --- |
| `menu` | Open another menu named in `route_value`. |
| `workflow` | Start a database-defined workflow named in `route_value`. |
| `message` | Send `route_value` as a message. |
| `calendar` | Render a configured Jalali inline calendar. |
| `noop` | Do nothing; useful for labels or disabled actions. |

## Example: daily leave button with a Jalali 1405 calendar

Insert a button:

```sql
INSERT INTO baleh.bot_buttons
    (menu_name, button_text, icon, callback_data, row_index, col_index, row_align, is_active)
VALUES
    ('main_menu', N'ثبت مرخصی روزانه', N'📅', 'leave_daily_calendar', 1, 1, 'right', 1);
```

Configure what the button does:

```sql
INSERT INTO baleh.routes
    (callback_data, route_type, route_value, route_config, is_active)
VALUES
(
    'leave_daily_calendar',
    'calendar',
    N'📅 تاریخ مرخصی روزانه را انتخاب کنید:',
    N'{
        "calendar": "jalali",
        "year": 1405,
        "month": 1,
        "min_year": 1405,
        "max_year": 1405,
        "week_start": "sat",
        "selected_message": "✅ تاریخ مرخصی روزانه انتخاب شد: {date}"
    }',
    1
);
```

With this configuration, pressing **ثبت مرخصی روزانه** shows a Jalali calendar for year 1405, starts each week on Saturday, and lets the user move between months inside the configured year. Selecting a day sends the configured `selected_message` with `{date}` replaced by the selected Jalali date.

## Calendar configuration keys

| Key | Example | Description |
| --- | --- | --- |
| `year` | `1405` | Initial Jalali year to display. |
| `month` | `1` | Initial Jalali month to display. |
| `min_year` | `1405` | First year allowed by navigation. |
| `max_year` | `1405` | Last year allowed by navigation. |
| `week_start` | `sat` | First day of the week. Use `sat` for Saturday. |
| `selected_message` | `✅ تاریخ انتخاب شد: {date}` | Message sent after date selection. |

## Database schema source of truth

The SQL Server schema and seed script is maintained in `db/schema.sql`. If a table is added/removed, a field is added/removed, or a datatype changes, update `db/schema.sql` in the same code change and run it against the target SQL Server database.
