class RuleEngine:

    @staticmethod
    def check(button, user):

        # role check
        if button.get("role_required"):
            if button["role_required"] != user.data.get("role"):
                return False

        # condition check
        expr = button.get("condition_expr")

        if expr:
            try:
                return eval(expr, {}, {"user": user.data})
            except:
                return False

        return True