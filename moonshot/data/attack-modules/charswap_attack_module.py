import math
import random
import string
from nltk import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer

from moonshot.src.redteaming.attack.attack_module import AttackModule
from moonshot.src.redteaming.attack.attack_module_arguments import AttackModuleArguments


def get_n_random(low: int, high: int, n: int) -> list:
    """
    Util function to generate random indices.
    Words of these indices after word tokenization will be subjected to perturbation.
    """
    result = []
    try:
        result = random.sample(range(low, high), n)
    except ValueError:
        print(f"Sample size of {n} exceeds population size of {high - low}")
    return result


"""
About this attack module:
This module creates perturbations through swapping characters for words that contains more than 3 characters.
Configurable Params:
1. MAX_ITERATIONS - Number of prompts that should be sent to the target.
2. word_swap_ratio - Percentage of words in a prompt that should be perturbed.
"""


class CharSwapGenerator(AttackModule):
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
        self.description = (
            "This attack creates perturbations through swapping characters for words that contains "
            "more than 3 characters."
        )
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
        MAX_ITERATION = 10
        # Configurble PARAMS - Percentage of words in a prompt that should be changed
        word_swap_ratio = 0.2

        word_list = word_tokenize(self.prompt)
        word_list_len = len(word_list)
        num_perturb_words = math.ceil(word_list_len * word_swap_ratio)
        for attempt in range(MAX_ITERATION):
            # get random indices of words to undergo swapping algo
            random_words_idx = get_n_random(0, word_list_len, num_perturb_words)
            for idx in random_words_idx:
                if word_list[idx] not in string.punctuation and len(word_list[idx]) > 3:
                    idx1 = random.randint(1, len(word_list[idx]) - 2)
                    idx_elements = list(word_list[idx])
                    # swap characters
                    idx_elements[idx1], idx_elements[idx1 + 1] = (
                        idx_elements[idx1 + 1],
                        idx_elements[idx1],
                    )
                    word_list[idx] = "".join(idx_elements)
            new_prompt = TreebankWordDetokenizer().detokenize(word_list)
            result_list.append(await self._send_prompt_to_all_llm([new_prompt]))
            word_list = word_tokenize(self.prompt)
        for res in result_list:
            for x in res:
                print(x.prompt)
                print(x.predicted_results)
                print()

        return result_list
