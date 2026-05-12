from services.menu_service import MenuService
from services.action_service import ActionService
from services.route_service import RouteService


class CallbackRouter:

    def __init__(self, bot):
        self.bot = bot

    # ==========================================
    # MAIN HANDLER
    # ==========================================
    def handle(self, ctx):

        action = ctx.callback_data

        if not action:
            return

        # CALENDAR NAVIGATION
        if action.startswith("CAL:") or action.startswith("CALSELECT:"):
            if ActionService.handle_calendar_navigation(self.bot, ctx):
                return

        # MENU NAVIGATION (prefix mode)
        if action.startswith("MENU:"):
            value = action.split(":", 1)[1]

            self._handle_menu(value, ctx)
            return

        # WORKFLOW (prefix mode)
        if action.startswith("WF:"):
            value = action.split(":", 1)[1]

            self._handle_workflow(value, ctx)
            return

        # DATABASE ROUTE
        route = RouteService.resolve_details(action)
        if not route:
            self._handle_action(action, ctx)
            return

        self._handle_route(route, action, ctx)
        route_type, route_value = RouteService.resolve(action)
        self._handle_route(route_type, route_value, action, ctx)

    # ==========================================
    # MENU HANDLER
    # ==========================================
    def _handle_menu(self, value, ctx):

        MenuService.open_menu(
            self.bot,
            ctx.chat_id,
            value
        )

    # ==========================================
    # WORKFLOW HANDLER
    # ==========================================
    def _handle_workflow(self, value, ctx):

        from services.workflow_service import start_workflow

        start_workflow(
            self.bot,
            ctx.message,
            value
        )

    # ==========================================
    # DB ROUTE HANDLER
    # ==========================================
    def _handle_route(self, route, action, ctx):

        route_type = str(route.get("route_type") or "action").lower()
        route_value = str(route.get("route_value") or "")
        route_config = route.get("route_config")

        if ActionService.handle(
            self.bot,
            ctx,
            action,
            route_type,
            route_value,
            route_config,
        ):
            return
    def _handle_route(self, route_type, route_value, action, ctx):

        route_type = str(route_type or "action").lower()
        route_value = str(route_value or "")

        if route_type == "menu":
            self._handle_menu(route_value, ctx)
            return

        if route_type == "workflow":
            self._handle_workflow(route_value, ctx)
            return

        if route_type == "message":
            self.bot.send_message(ctx.chat_id, route_value)
            return

        self._handle_action(route_value or action, ctx)

    # ==========================================
    # NORMAL ACTION ROUTER
    # ==========================================
    def _handle_action(self, action, ctx):

        if action == "profile":

            self.bot.send_message(
                ctx.chat_id,
                "👤 پروفایل"
            )

            return

        if action == "buy_plan":

            self.bot.send_message(
                ctx.chat_id,
                "💳 خرید اشتراک"
            )

            return

        if action == "support":

            self.bot.send_message(
                ctx.chat_id,
                "📞 پشتیبانی"
            )

            return

        self.bot.send_message(
            ctx.chat_id,
            f"Unknown action: {action}"
        )
