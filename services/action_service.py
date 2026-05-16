import json

from services.jalali_calendar import JalaliCalendar


class ActionService:
    """Execute database-configured actions without per-button code changes."""

    @staticmethod
    def handle(bot, ctx, action_code, route_type, route_value=None, route_config=None):
        route_type = str(route_type or "action").lower()
        config = ActionService._parse_config(route_config)

        if route_type == "calendar":
            ActionService._send_jalali_calendar(bot, ctx, action_code, route_value, config)
            return True

        if route_type == "noop":
            return True

        return False

    @staticmethod
    def handle_calendar_navigation(bot, ctx):
        callback_data = str(ctx.callback_data or "")

        if callback_data.startswith("CALSELECT:"):
            return ActionService._handle_calendar_select(bot, ctx, callback_data)

        if callback_data == "CAL:NOOP":
            return True

        if callback_data == "CAL:CLOSE":
            bot.edit_message(ctx.chat_id, ctx.message_id, "تقویم بسته شد.")
            return True

        parts = callback_data.split(":")
        if len(parts) != 4 or parts[0] != "CAL":
            return False

        action_code = parts[1]
        year = int(parts[2])
        month = int(parts[3])

        from services.route_service import RouteService

        route = RouteService.resolve_details(action_code)
        if not route or str(route.get("route_type") or "").lower() != "calendar":
            bot.send_message(ctx.chat_id, "❌ تنظیمات تقویم پیدا نشد.")
            return True

        config = ActionService._parse_config(route.get("route_config"))
        config["year"] = year
        config["month"] = month

        title = route.get("route_value") or "📅 انتخاب تاریخ"
        keyboard = ActionService._build_calendar_keyboard(action_code, config)

        bot.edit_message(
            ctx.chat_id,
            ctx.message_id,
            title,
            reply_markup=keyboard,
        )
        return True

    @staticmethod
    def _handle_calendar_select(bot, ctx, callback_data):
        parts = callback_data.split(":", 2)
        if len(parts) != 3:
            return False

        action_code = parts[1]
        selected_date = parts[2]

        from services.route_service import RouteService

        route = RouteService.resolve_details(action_code)
        config = ActionService._parse_config(route.get("route_config") if route else None)
        message_template = config.get("selected_message") or "✅ تاریخ انتخاب شد: {date}"

        bot.send_message(
            ctx.chat_id,
            message_template.format(date=selected_date),
        )
        return True

    @staticmethod
    def _send_jalali_calendar(bot, ctx, action_code, route_value, config):
        title = route_value or config.get("title") or "📅 انتخاب تاریخ"
        keyboard = ActionService._build_calendar_keyboard(action_code, config)

        bot.send_message(
            ctx.chat_id,
            title,
            reply_markup=keyboard,
        )

    @staticmethod
    def _build_calendar_keyboard(action_code, config):
        year = int(config.get("year", 1405))
        month = int(config.get("month", 1))
        min_year = int(config.get("min_year", year))
        max_year = int(config.get("max_year", year))

        return JalaliCalendar.build_month_keyboard(
            year=year,
            month=month,
            action_code=action_code,
            week_start=config.get("week_start", "sat"),
            select_callback_prefix=config.get("select_callback_prefix"),
            min_year=min_year,
            max_year=max_year,
        )

    @staticmethod
    def _parse_config(route_config):
        if not route_config:
            return {}

        if isinstance(route_config, dict):
            return route_config

        try:
            data = json.loads(route_config)
        except (TypeError, ValueError):
            return {}

        return data if isinstance(data, dict) else {}
