from core.state.state_manager import StateManager
from core.workflow.engine import WorkflowEngine


class WorkflowExecutor:

    def __init__(self, bot, user_id, chat_id):

        self.bot = bot
        self.user_id = user_id
        self.chat_id = chat_id

        self.state_mgr = StateManager(user_id)

    # ==========================================
    # START WORKFLOW
    # ==========================================
    def start(self, workflow_code):

        wf_id = WorkflowEngine.get_workflow(workflow_code)

        if not wf_id:
            self.bot.send_message(
                self.chat_id,
                "❌ workflow پیدا نشد"
            )
            return False

        start_step = WorkflowEngine.get_start_step(wf_id)

        if not start_step:
            self.bot.send_message(
                self.chat_id,
                "❌ start step تعریف نشده"
            )
            return False

        # ✅ ذخیره state
        self.state_mgr.set(
            workflow_code=workflow_code,
            current_step=start_step,
            data={}
        )

        self.run_step(workflow_code, start_step)

        return True

    # ==========================================
    # HANDLE USER INPUT
    # ==========================================
    def handle(self, text):

        # 🚨 اگر workflow فعال نیست
        if not self.state_mgr.workflow_code:
            return False

        if not self.state_mgr.current_step:
            return False

        wf_code = self.state_mgr.workflow_code
        step_code = self.state_mgr.current_step

        wf_id = WorkflowEngine.get_workflow(wf_code)

        if not wf_id:
            self.state_mgr.clear()
            return False

        step = WorkflowEngine.get_step(wf_id, step_code)

        if not step:
            self.state_mgr.clear()
            return False

        # ==========================================
        # ذخیره input کاربر
        # ==========================================
        if step.get("field"):

            self.state_mgr.update(
                **{
                    step["field"]: text
                }
            )

        next_step = step.get("next")

        # ==========================================
        # پایان workflow
        # ==========================================
        if not next_step or next_step == "END":

            self.bot.send_message(
                self.chat_id,
                "✅ عملیات کامل شد"
            )

            # 🔥 اینجا میتونی data نهایی را ذخیره کنی
            print("FINAL DATA:", self.state_mgr.data)

            self.state_mgr.clear()

            return True

        # ==========================================
        # رفتن به step بعد
        # ==========================================
        self.state_mgr.next_step(next_step)

        self.run_step(wf_code, next_step)

        return True

    # ==========================================
    # RUN STEP
    # ==========================================
    def run_step(self, wf_code, step_code):

        wf_id = WorkflowEngine.get_workflow(wf_code)

        if not wf_id:
            return

        step = WorkflowEngine.get_step(wf_id, step_code)

        if not step:
            return

        message = step.get("message") or "..."

        self.bot.send_message(
            self.chat_id,
            message
        )