class ContextStrategy:
    def add_in_context(
        self, prompt_without_context: str, list_of_previous_prompts: list = None
    ) -> str:
        pass

    def get_number_of_prev_prompts(
        self, prompt_without_context: str, list_of_previous_prompts: list = None
    ) -> str:
        pass

    def connect_to_llm(name_of_llm: str):
        pass
