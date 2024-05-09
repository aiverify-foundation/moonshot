import time
import os
import tensorflow as tf
import logging
from textattack.augmentation import Augmenter
from textattack.constraints.pre_transformation import (
    RepeatModification,
    StopwordModification,
)
from textattack.constraints.semantics.sentence_encoders import UniversalSentenceEncoder
from textattack.transformations import (
    CompositeTransformation,
    WordSwapEmbedding,
    WordSwapHomoglyphSwap,
    WordSwapNeighboringCharacterSwap,
    WordSwapRandomCharacterDeletion,
    WordSwapRandomCharacterInsertion,
)

from moonshot.src.redteaming.attack.attack_module import AttackModule
from moonshot.src.redteaming.attack.attack_module_arguments import AttackModuleArguments


os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel(logging.ERROR)

class BugGenerator(AttackModule):
    def __init__(self, am_id: str, am_arguments: AttackModuleArguments | None = None):
        # Initialize super class
        super().__init__(am_id, am_arguments)
        self.name = "TextBugger Attack"
        self.description = (
            "About this attack module:\nThis module implements the perturbations listed in the paper "
            "TEXTBUGGER: Generating Adversarial Text Against Real-world Applications.\nParameters:\n1. "
            "MAX_ITERATIONS - Number of prompts that should be sent to the target. This is also the"
            "number of transformations that should be generated. [Default: 5]\n2. word_swap_ratio - "
            "Percentage of words in a prompt that should be perturbed. [Default: 0.2]\n3. top_k - "
            "To select top k number of semantic words from the GLoVe embedding. [Default: 5]\n4. "
            "threshold - semantic similarity threshold for the universal encoder. [Default: 0.8]\n"
            "Note:\nUsage of this attack module requires the internet. Initial downloading of the "
            "GLoVe embedding occurs when the UniversalEncoder is called.\nEmbedding is retrieved from "
            "the following URL: https://textattack.s3.amazonaws.com/word_embeddings/paragramcf"
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
        # Configurble PARAMS - Percentage of words in a prompt that should be changed
        word_swap_ratio = 0.2
        # Configurble PARAMS - To select top 5 semantic words our of GloVe emedding
        top_k = 5
        # Configurble PARAMS -Threshold for Universal Sentence Encoder
        threshold = 0.8
        # Configurble PARAMS - Number of prompts to be sent to target
        MAX_ITERATION = 5
        transformation = CompositeTransformation(
            [
                # (1) Insert: Insert a space into the word.
                # Generally, words are segmented by spaces in English. Therefore,
                # we can deceive classifiers by inserting spaces into words.
                WordSwapRandomCharacterInsertion(
                    random_one=True,
                    letters_to_insert=" ",
                    skip_first_char=True,
                    skip_last_char=True,
                ),
                # (2) Delete: Delete a random character of the word except for the first
                # and the last character.
                WordSwapRandomCharacterDeletion(
                    random_one=True, skip_first_char=True, skip_last_char=True
                ),
                # (3) Swap: Swap random two adjacent letters in the word but do not
                # alter the first or last letter. This is a common occurrence when
                # typing quickly and is easy to implement.
                WordSwapNeighboringCharacterSwap(
                    random_one=True, skip_first_char=True, skip_last_char=True
                ),
                # (4) Substitute-C (Sub-C): Replace characters with visually similar
                # characters (e.g., replacing “o” with “0”, “l” with “1”, “a” with “@”)
                # or adjacent characters in the keyboard (e.g., replacing “m” with “n”).
                WordSwapHomoglyphSwap(),
                # (5) Substitute-W
                # (Sub-W): Replace a word with its topk nearest neighbors in a
                # context-aware word vector space. Specifically, we use the pre-trained
                # GloVe model [30] provided by Stanford for word embedding and set
                # topk = 5 in the experiment.
                WordSwapEmbedding(max_candidates=top_k),
            ]
        )
        constraints = [RepeatModification(), StopwordModification()]
        """
        In our experiment, we first use the Universal Sentence
        Encoder [7], a model trained on a number of natural language
        prediction tasks that require modeling the meaning of word
        sequences, to encode sentences into high dimensional vectors.
        Then, we use the cosine similarity to measure the semantic
        similarity between original texts and adversarial texts.
        ... 'Furthermore, the semantic similarity threshold \\eps is set
        as 0.8 to guarantee a good trade-off between quality and
        strength of the generated adversarial text.'
        """
        constraints.append(UniversalSentenceEncoder(threshold=threshold))
        augmenter = Augmenter(
            transformation=transformation,
            constraints=constraints,
            pct_words_to_swap=word_swap_ratio,
            transformations_per_example=MAX_ITERATION,
        )
        print(f'{"*"*10} Augmentation in Progress {"*"*10}')
        start = time.process_time()
        results = augmenter.augment(self.prompt)
        print(f'{"*"*10} Time Taken: {time.process_time() - start}s {"*"*10}')
        for i in results:
            print(i)
            result_list.append(await self._send_prompt_to_all_llm([i]))
        for res in result_list:
            for x in res:
                print(x.prompt)
                print(x.predicted_results)
                print()

        return result_list
