from core.router.callback_router import CallbackRouter

router = CallbackRouter()


def register_routes():

    from handlers.callbacks import (
        buy_plan,
        profile,
        support,
        
    )

    router.register("buy_plan", buy_plan)
    router.register("profile", profile)
    router.register("support", support)


    return router