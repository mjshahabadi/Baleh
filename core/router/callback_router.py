from services.menu_service import MenuService


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

        # MENU NAVIGATION
        if action.startswith("MENU:"):
            value = action.split(":", 1)[1]

            self._handle_menu(value, ctx)
            return

        # WORKFLOW
        if action.startswith("WF:"):
            value = action.split(":", 1)[1]

            self._handle_workflow(value, ctx)
            return

        # NORMAL ROUTE
        self._handle_action(action, ctx)

    # ==========================================
    # MENU HANDLER (FIXED)
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
    # NORMAL ACTION ROUTER
    # ==========================================
    def _handle_action(self, action, ctx):

        if action == "profile":

            self.bot.send_message(
                ctx.chat_id,
                "👤 پروفایل"
            )

            return

        # ⚠️ fix: keyboard undefined bug
        self.bot.send_message(
            ctx.chat_id,
            f"Unknown action: {action}"
        )