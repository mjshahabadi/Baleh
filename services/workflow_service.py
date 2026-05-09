from core.workflow.executor import WorkflowExecutor


def start_workflow(bot, message, code):

    user_id = message["from"]["id"]
    chat_id = message["chat"]["id"]

    executor = WorkflowExecutor(bot, user_id, chat_id)
    executor.start(code)


def handle_workflow(bot, message):

    user_id = message["from"]["id"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    executor = WorkflowExecutor(bot, user_id, chat_id)

    return executor.handle(text)