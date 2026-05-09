from core.state.state_store import StateStore


class StateManager:

    def __init__(self, user_id: int):

        self.user_id = user_id

        # defaults
        self.workflow_code = None
        self.current_step = None
        self.data = {}

        try:

            state = StateStore.get_state(user_id)

            if not state:
                return

            # ===================================
            # dict mode
            # ===================================
            if isinstance(state, dict):

                self.workflow_code = state.get("workflow_code")
                self.current_step = state.get("current_step")
                self.data = state.get("data") or {}

                return

            # ===================================
            # tuple mode
            # ===================================
            if isinstance(state, (tuple, list)):

                if len(state) >= 3:

                    self.workflow_code = state[0]
                    self.current_step = state[1]
                    self.data = state[2] or {}

                    return

        except Exception as e:

            print("STATE MANAGER LOAD ERROR:", e)

            self.workflow_code = None
            self.current_step = None
            self.data = {}

    # ===================================
    # Start / Set State
    # ===================================
    def set(
        self,
        workflow_code: str,
        current_step: str,
        data: dict = None
    ):

        self.workflow_code = workflow_code
        self.current_step = current_step
        self.data = data or {}

        StateStore.set_state(
            self.user_id,
            self.workflow_code,
            self.current_step,
            self.data
        )

    # ===================================
    # Update Data
    # ===================================
    def update(self, **kwargs):

        if not self.data:
            self.data = {}

        self.data.update(kwargs)

        StateStore.set_state(
            self.user_id,
            self.workflow_code,
            self.current_step,
            self.data
        )

    # ===================================
    # Move To Next Step
    # ===================================
    def next_step(self, step_name: str):

        self.current_step = step_name

        StateStore.set_state(
            self.user_id,
            self.workflow_code,
            self.current_step,
            self.data
        )

    # ===================================
    # Clear State
    # ===================================
    def clear(self):

        self.workflow_code = None
        self.current_step = None
        self.data = {}

        StateStore.clear_state(self.user_id)

    # ===================================
    # Checks
    # ===================================
    def is_workflow(self, workflow_code: str):

        return self.workflow_code == workflow_code

    def is_step(self, step_name: str):

        return self.current_step == step_name

    # ===================================
    # Helpers
    # ===================================
    @property
    def state(self):

        """
        compatibility layer
        old code:
            state_mgr.state.startswith(...)
        """

        if not self.workflow_code:
            return None

        return f"WF:{self.workflow_code}"

    @property
    def step(self):

        return self.current_step