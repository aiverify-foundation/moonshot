
import homoglyphs as hg
from nltk import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer

from moonshot.src.redteaming.attack.attack_module import AttackModule
from moonshot.src.redteaming.attack.attack_module_arguments import AttackModuleArguments

class HomoglyphGenerator(AttackModule):
    def __init__(self, am_arguments: AttackModuleArguments):
        # Initialize super class
        super().__init__(am_arguments)

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
        
        MAX_ITERATION = 10
        # converting glyphs to ASCII characters
        homoglyphs = hg.Homoglyphs(languages={'en'}, strategy=hg.STRATEGY_LOAD)
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
                print(f'The word {word_list[idx]} does not contain ASCII characters. Skipping...')
            for i in hglyphs:
                word_list[idx] = i
                new_prompt = TreebankWordDetokenizer().detokenize(word_list)
                count+=1
                result_list.append(
                await self._send_prompt_to_all_llm(
                    [new_prompt]
                )
                )
                word_list = word_tokenize(self.prompt)
                if count == MAX_ITERATION:
                    break
        for res in result_list:
            for x in res:
                print(x.prompt)
                print(x.predicted_results)
                print()

        return result_list