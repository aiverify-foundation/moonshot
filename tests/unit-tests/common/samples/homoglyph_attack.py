import homoglyphs as hg
from moonshot.src.redteaming.attack.attack_module import AttackModule
from moonshot.src.redteaming.attack.attack_module_arguments import AttackModuleArguments
from moonshot.src.utils.log import configure_logger
from nltk import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer

# Create a logger for this module
logger = configure_logger(__name__)


class HomoglyphGenerator(AttackModule):
    def __init__(self, am_id: str, am_arguments: AttackModuleArguments | None = None):
        # Initialize super class
        super().__init__(am_id, am_arguments)
        self.name = "Homoglyph Attack"
        self.description = (
            "This module tests for adversarial textual robustness. Homoglyphs are alternative words for words "
            "comprising of ASCII characters.\nExample of a homoglyph fool -> fooI\nThis module purturbs the prompt "
            "with all available homoglyphs for each word present.\nParameters:\n1. MAX_ITERATIONS - Maximum "
            "number of prompts that should be sent to the target. [Default: 20]"
        )

    def get_metadata(self) -> dict:
        """
        Get metadata for the attack module.

        Returns a dictionary containing the id, name, and description of the attack module. If the name or description
        is not available, empty strings are returned.

        Returns:
            dict | None: A dictionary containing the metadata of the attack module, or None if the metadata is not
            available.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description if hasattr(self, "description") else "",
        }

    async def execute(self):
        """
        Asynchronously executes the attack module.

        This method loads the dataset contents using the `load_dataset_contents` method,
        processes the dataset through a prompt template, retrieves the connector to the first
        Language Learning Model (LLM) and sends the processed dataset as a prompt to the LLM.
        """
        self.load_modules()
        return await self.perform_attack_manually()

    async def perform_attack_manually(self) -> list:
        """
        Asynchronously performs the attack manually. The user will need to pass in a list of prompts and
        the LLM connector endpoint to send the prompts to. In this example, there is a for loop to send the
        list of prepared prompts to all the LLM connectors defined.

        This method prepares prompts for each target Language Learning Model (LLM) using the provided prompt
        and sends them to the respective LLMs.
        """
        result_list = []
        # Configurble PARAMS - Number of prompts to be sent to target
        MAX_ITERATION = 20
        # converting glyphs to ASCII characters
        homoglyphs = hg.Homoglyphs(
            strategy=hg.STRATEGY_LOAD, ascii_strategy=hg.STRATEGY_REMOVE
        )
        count = 0
        word_list = word_tokenize(self.prompt)
        word_list_len = len(word_list)
        for idx in range(word_list_len):
            if count == MAX_ITERATION:
                break
            hglyphs = []
            try:
                hglyphs = homoglyphs.to_ascii(word_list[idx])
            except UnicodeDecodeError:
                logger.error(
                    f"[HomoglyphGenerator] The word {word_list[idx]} does not contain ASCII characters. Skipping..."
                )
            if len(hglyphs) > 1:
                for i in hglyphs:
                    word_list[idx] = i
                    new_prompt = TreebankWordDetokenizer().detokenize(word_list)
                    count += 1
                    result_list.append(await self._send_prompt_to_all_llm([new_prompt]))
                    word_list = word_tokenize(self.prompt)
                    if count == MAX_ITERATION:
                        break
        for res in result_list:
            for x in res:
                logger.debug(f"[HomoglyphGenerator] Prompt: {x.prompt}")
                logger.debug(
                    f"[HomoglyphGenerator] Predicted Results: {x.predicted_results}\n"
                )
        return result_list
