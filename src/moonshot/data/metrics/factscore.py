from __future__ import annotations

import json
import logging
import re
import time
from typing import Any, Union

import numpy as np
import spacy
from sentence_transformers import SentenceTransformer

from moonshot.src.common.connection import Connection, get_predictions
from moonshot.src.common.env_variables import EnvironmentVars
from moonshot.src.utils.timeit import timeit

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load spacy model 'en_core_web_trf'
logging.info("[FactScore] Loading spacy model 'en_core_web_trf'.")
start_time = time.perf_counter()
nlp = spacy.load("en_core_web_trf")
logging.info(
    f"[FactScore] Loading spacy model 'en_core_web_trf' took {(time.perf_counter() - start_time):.4f}s"
)

# Load SBert model 'https://huggingface.co/sentence-transformers/all-mpnet-base-v2'
logging.info(
    "[FactScore] Loading sentence transformer 'sentence-transformers/all-mpnet-base-v2'."
)
start_time = time.perf_counter()
sbert_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
logging.info(
    f"[FactScore] Loading sentence transformer 'sentence-transformers/all-mpnet-base-v2' took "
    f"{(time.perf_counter() - start_time):.4f}s"
)

# Precompile the regular expression
start_time = time.perf_counter()
pattern = re.compile(r": \(?(at )?\[\d*(\(\w\)(\(i{1,3}\))?)?].*?\.", re.DOTALL)
logging.info(
    f"[FactScore] Compiling regression pattern took {(time.perf_counter() - start_time):.4f}s"
)


class FactScore:
    """
    FactScore returns the various fact scores.
    """

    break_prompt = """Split the following document (delimited by ```) to sentences:
    Document: ```{document}```
    Output the sentences in JSON format with the following key: 'list_of_sentences'.
    """

    fact_check_prompt = """You are a careful fact-checker. Below is a reference document (delimited by ```):
    Document: ```{document}```
    According to the above reference document, is the following hypothesis: \
    true (entailment), false (contradiction), or undetermined (neutral)?
    Hypothesis: {statement}
    If the hypothesis is not true, revise it to be consistent with the reference document.
    Provide output in JSON format with the following four keys:
    'hypothesis', 'decision': (true, false, or undetermined), 'reason', 'revision'.
    """

    @staticmethod
    @timeit
    def get_results(
        prompts: Any, predicted_results: Any, targets: Any, *args, **kwargs
    ) -> dict:
        """
        Get the results of a prediction using the FactScore algorithm.

        Parameters:
            prompts (Any): The prompts used for the prediction.
            predicted_results (Any): The predicted results.
            targets (Any): The target results.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A dictionary containing the final fact score.
        """
        try:
            logging.info("Getting results using FactScore")

            # Set up the FactScore class
            factscore = FactScore.setup_factscore(predicted_results, prompts)

            # Calculate the rouge scores
            output_dict = factscore.compute_factscore()

            # Return the final rouge scores dictionary
            return {"factscore": output_dict}

        except Exception as exception:
            # Raise an error if there is an exception during calculation
            logging.error(
                f"[FactScore] Unable to generate metrics results - {str(exception)}"
            )
            raise RuntimeError(
                f"[FactScore] Unable to generate metrics results - {str(exception)}"
            )

    @classmethod
    def setup_factscore(cls, output_response: Any, targets: Any) -> FactScore:
        """
        Set up the FactScore class.
        """
        with open(f"{EnvironmentVars.METRICS_CONFIG}", "r") as json_file:
            json_file_info = json.load(json_file)
            if __name__ in json_file_info:
                file_info = json_file_info[__name__]
            else:
                file_info = {}

            # Read model endpoint, length limit, perform_postparsing from config
            if "model_endpoint" in file_info:
                model_endpoint = file_info["model_endpoint"]
            else:
                model_endpoint = "my-openai-gpt35"

            if "length_limit" in file_info:
                length_limit = file_info["length_limit"]
            else:
                length_limit = 10000

            if "perform_postparsing" in file_info:
                if file_info["perform_postparsing"] == "true":
                    perform_postparsing = True
                else:
                    perform_postparsing = False
            else:
                perform_postparsing = False

            if "extract_facts_model" in file_info:
                if file_info["extract_facts_model"] == "external":
                    extract_facts_use_local_model = False
                else:
                    extract_facts_use_local_model = True
            else:
                extract_facts_use_local_model = True

            if "extract_facts_model" in file_info:
                if file_info["extract_facts_model"] == "external":
                    extract_facts_use_local_model = False
                else:
                    extract_facts_use_local_model = True
            else:
                extract_facts_use_local_model = True

            return cls(
                length_limit,
                model_endpoint,
                perform_postparsing,
                extract_facts_use_local_model,
                output_response,
                targets,
            )

    def __init__(
        self,
        length_limit: int = 0,
        model_endpoint: str = "",
        perform_postparsing: bool = False,
        extract_facts_use_local_model: bool = True,
        output_response: Any = None,
        targets: Any = None,
    ) -> None:
        self.length_limit = length_limit
        self.model_endpoint = model_endpoint
        self.perform_postparsing = perform_postparsing
        self.extract_facts_use_local_model = extract_facts_use_local_model
        self.output_response = output_response
        self.targets = targets

        # Load connection from model endpoint
        self.conn_instance = None

    def extract_facts(self, input_document: str, prompt: str = break_prompt) -> list:
        """
        Split text document to sentences using ChatGPT

        Args:
            input_document: input text document
            prompt: prompt for text splitting

        Return:
            a list of dict [{'list_of_sentences'}]
            length of list: number of paragraphs in the input document
        """
        # Split document to paragraphs
        paragraphs = input_document.split("\n")

        if self.extract_facts_use_local_model:
            logging.info("[FactScore] Extracting facts using local model.")
            facts_dicts = [
                {
                    "list_of_sentences": split_paragraph_to_sentences(
                        paragraph, cleaning=False
                    )
                }
                for paragraph in paragraphs
                if paragraph
            ]
            return facts_dicts
        else:
            logging.info("[FactScore] Extracting facts using api model.")
            prompts_list = [
                prompt.format(document=paragraph)
                for paragraph in paragraphs
                if paragraph
            ]
            return self.batch_call_api(prompts_list)

    def check_facts(self, facts_list: list, prompt: str = fact_check_prompt) -> list:
        """
        Check the fact in the list against reference

        Args:
            facts_list: a list of dict
            prompt: prompt for fact-checking

        Return:
            a list of dict: [{'hypothesis', 'decision', 'reason', 'revision'}]
        """
        if not facts_list:
            return []
        prompts_list = [
            prompt.format(document=tmp_fact["reference"], statement=tmp_fact["fact"])
            for tmp_fact in facts_list
        ]
        return self.batch_call_api(prompts_list)

    def batch_call_api(self, prompts_list: list) -> list:
        # Format the targets and output response
        prompts_info = {
            "data": [
                {
                    "prompt": prompt,
                }
                for prompt in prompts_list
            ]
        }

        # Compute factscore for all input samples
        extracted_facts = get_predictions(
            prompts_info,
            self.conn_instance,
            None,
        )

        # Combine the extracted facts
        return [
            json.loads(tmp_fact["predicted_result"]) for tmp_fact in extracted_facts
        ]

    def check_facts_in_completions(
        self, facts_completions: list, ref_dict: dict
    ) -> tuple:
        """
        This function checks the facts in the completions against the reference document.

        Args:
            facts_completions: a list of dict [{'list_of_sentences'}]
            ref_dict: a dict of reference: {'parags', 'word_counts', 'sents', 'idx'}

        Return:
            fact_check_results: a list of dict: [{'fact', 'max_score', 'decision', 'reason', 'revision'}]
            total_facts: an integer for the total number of facts checked
            total_bad_facts: an integer for the total number of bad facts found
        """
        fact_check_results = []
        total_facts = total_bad_facts = 0
        for completion in facts_completions:
            # Retrieve the reference for each completion
            retrieval_output = retrieve_reference(
                completion["list_of_sentences"], ref_dict, self.length_limit
            )

            # Create a list of facts to check
            fact_check_list = [
                {"index": i, "fact": d["sentence"], "reference": d["reference"]}
                for i, d in enumerate(retrieval_output)
                if d.get("max_score") is not None and d["max_score"] < 0.9
                # Skip facts with very high similarity scores
            ]
            fact_check_completions = self.check_facts(fact_check_list)

            # Prepare the output data
            fact_check_output = self.prepare_output_data(
                retrieval_output, fact_check_completions, fact_check_list
            )
            fact_check_results.append(fact_check_output)

            # Compute total facts and total bad facts
            total_facts += sum(1 for d in fact_check_output if d["max_score"])
            total_bad_facts += sum(
                1
                for d in fact_check_output
                if "max_score" in d
                and d["max_score"]
                and "decision" in d
                and str(d["decision"]).lower() != "true"
            )

        return fact_check_results, total_facts, total_bad_facts

    def prepare_output_data(
        self, retrieval_output: list, fact_check_completions: list, facts_list: list
    ) -> list:
        """
        Prepare the output data for fact checking.

        Args:
            retrieval_output (list): A list of dictionaries representing the retrieval output.
            fact_check_completions (list): A list of dictionaries representing the fact check completions.
            facts_list (list): A list of dictionaries representing the facts list.

        Returns:
            list: The prepared output data for fact checking.
        """
        fact_check_output = [
            {"fact": d["sentence"], "max_score": d.get("max_score", "")}
            for d in retrieval_output
        ]
        for i, d in enumerate(fact_check_completions):
            d.pop("hypothesis")
            fact_check_output[facts_list[i]["index"]].update(d)
        return fact_check_output

    def compute_factscore_helper(
        self, reference: Union[str, list], candidate: str
    ) -> tuple[bool, dict]:
        """
        Compute FactScore for evaluating the factual consistency of generated summary.

        Args:
            reference: the source document
            candidate: the generated summary

        Returns:
            dict: {'factscore': {'total_facts', 'total_bad_facts', 'factscore', 'run_time', 'revision', 'results'}}
            'results': a list of dict: [{'fact', 'max_score', 'decision', 'reason', 'revision'}]
        """
        try:
            total_start_time = time.perf_counter()

            # Check if you need to message the candidate
            if self.perform_postparsing:
                # Perform prompt processing
                if isinstance(reference, list):
                    reference = slr_extract_judgment(reference)
                else:
                    reference = slr_extract_judgment(json.loads(reference))

                # Perform candidate processing
                candidate = "Facts\n\n" + candidate.split("Facts\n\n")[1]

            # Split the reference document into sentences
            logging.info("[Factscore] Splitting document to sentences")
            start_time = time.perf_counter()
            reference_dict = split_document_to_sentences(reference)
            doc_to_str_duration = f"{(time.perf_counter() - start_time):.4f}s"

            # Extract facts from the candidate document
            logging.info("[Factscore] Extracting facts from candidate document")
            start_time = time.perf_counter()
            facts_completions = self.extract_facts(candidate)
            extraction_facts_duration = f"{(time.perf_counter() - start_time):.4f}s"

            # Check the extracted facts against the reference document
            logging.info("[Factscore] Checking facts against reference document")
            start_time = time.perf_counter()
            (
                fact_check_results,
                total_facts,
                total_bad_facts,
            ) = self.check_facts_in_completions(facts_completions, reference_dict)
            check_facts_duration = f"{(time.perf_counter() - start_time):.4f}s"

            # Compute the fact score
            factscore = 1 - (total_bad_facts / total_facts) if total_facts else ""

            # Compute run time
            run_duration = f"{(time.perf_counter() - total_start_time):.4f}s"

            return True, {
                "reference": reference,
                "candidate": candidate,
                "total_facts": total_facts,
                "bad_facts": total_bad_facts,
                "factscore": factscore,
                "doc_to_str_duration": doc_to_str_duration,
                "extraction_facts_duration": extraction_facts_duration,
                "check_facts_duration": check_facts_duration,
                "total_run_duration": run_duration,
                "results": fact_check_results,
            }
        except ConnectionError as conn_error:
            logging.error(f"Failed to compute factscore: {str(conn_error)}")
            raise conn_error
        except Exception as error:
            logging.warning(f"Failed to compute factscore: {str(error)}")
            return False, {
                "reference": reference,
                "candidate": candidate,
            }

    @timeit
    def compute_factscore(self) -> dict:
        """
        Compute factscores for an input list of source document and summary pairs

        Returns:
            a dict: {'factscore', 'results'}
        """
        start_perf_time = time.perf_counter()

        # Load model endpoint and set db instance
        self.conn_instance = Connection.load_from_json_config(self.model_endpoint)

        individual_factscore = []
        for index, (reference, candidate) in enumerate(
            zip(self.targets, self.output_response)
        ):
            is_success, result = self.compute_factscore_helper(reference, candidate)
            individual_factscore.append(result)
            if is_success:
                logging.info(f"#{index} FactScore computed")
            else:
                logging.warning(f"#{index} Compute FactScore error")

        # Generate statistics
        factscore_stats = {"total_facts": 0, "total_bad_facts": 0, "avg_factscore": 0.0}
        for result in individual_factscore:
            if result and "total_facts" in result and "bad_facts" in result:
                factscore_stats["total_facts"] += result["total_facts"]
                factscore_stats["total_bad_facts"] += result["bad_facts"]

        if factscore_stats["total_facts"] > 0:
            factscore_stats["avg_factscore"] = (
                1 - factscore_stats["total_bad_facts"] / factscore_stats["total_facts"]
            )

        # Compute run time
        end_time = time.perf_counter()
        run_duration = f"{(end_time - start_perf_time):.4f}s"

        factscore_stats["total_runtime"] = run_duration
        factscore_stats["llm-endpoint"] = self.model_endpoint

        return {
            "individual_scores": individual_factscore,
            "average_scores": factscore_stats,
        }


# Support utility functions
def remove_ref(s: str) -> str:
    """
    To replace the reference of the following format to period ".":
        ": at [12], [34] and [56]."
        ": [12], [34] and [56]."
        ": at [40(a)], [74] to [79] and [83(e)]."
        ": (at [64] and [68])."
        ": at [25(c)(ii)]."
        Parameters:
            s (str): input text
        Returns:
            text (str): output of all references matching the formats removed.
    """
    return pattern.sub(".", s)


def remove_list_number(text: str) -> str:
    """Remove list number at the beginning of a text paragraph"""
    words = text.split(maxsplit=1)
    if words[0].strip("().").isdigit():
        return words[1] if len(words) > 1 else ""
    return text


def clean_text(text: str) -> str:
    """Remove paragraph numbers at the beginning
    Remove references at the end
    """
    return " ".join(remove_ref(remove_list_number(text)).split())


def fit_paragraphs_to_limit(word_counts: list, length_limit: int) -> int:
    """Check how many paragraphs can fit into length limit
    Args:
        word_counts: Number of words in each paragraph
        length_limit: The total number words in selected paragraphs should not exceed this limit.
    Return:
        Number of paragraphs that can fit into length limit
    """
    total_words = 0
    for i, count in enumerate(word_counts):
        total_words += count
        if total_words > length_limit:
            return i
    return len(word_counts)


def find_top_reference(scores, ref_dict: dict, length_limit: int) -> dict:
    """Find indexes of the most relevant paragraphs in reference
    Args:
        scores: a numpy array of similarity scores
        length_limit: The total number words in selected paragraphs should not exceed this limit.
        ref_dict: a dict of reference: {'parags', 'word_counts', 'sents', 'idx'}
    Return:
        a dict: ['max_score', 'idx']
        idx: indexes of the most relevant reference paragraphs
    """
    # Sort reference sentences on scores in descending order
    scores_dict = sorted(
        [
            {
                "i": parag_index,
                "score": score,
                "word_count": ref_dict["word_counts"][parag_index],
            }
            for parag_index, score in zip(ref_dict["idx"], scores)
        ],
        key=lambda x: x["score"],
        reverse=True,
    )

    # Remove duplicates and keep only the first occurrence
    seen = set()
    scores_dict = [d for d in scores_dict if not (d["i"] in seen or seen.add(d["i"]))]

    # Find how many reference paragraphs can fit into length limit
    number_of_parags = fit_paragraphs_to_limit(
        word_counts=[d["word_count"] for d in scores_dict], length_limit=length_limit
    )

    return {
        "max_score": round(float(scores_dict[0]["score"]), 4),
        "idx": sorted([d["i"] for d in scores_dict[:number_of_parags]]),
    }


def retrieve_reference(sentences: list, ref_dict: dict, length_limit: int) -> list:
    """Retrieve relevant reference paragraphs for a list of candidate sentences.
    Args:
        sentences: a list of candidate sentences
        ref_dict:  a dict of reference: {'parags', 'word_counts', 'sents', 'idx'}
        length_limit: The total number words in selected paragraphs should not exceed this limit.
    Return:
        a list of dict: [{'sentence', 'cleaned', 'reference', 'max_score'}]
    """
    # Select candidate sentences (>= 3 words) for similarity computation
    candidates = [
        {"index": i, "sentence": sent, "cleaned": clean_text(sent)}
        for i, sent in enumerate(sentences)
    ]

    selected_candidates = [
        cand for cand in candidates if len(cand["cleaned"].split()) > 2
    ]

    if not selected_candidates:
        return candidates

    # Compute similarity scores
    sim_scores = compute_sbert_scores(
        ref_dict["sents"], [cand["cleaned"] for cand in selected_candidates]
    )
    logging.info(f"Similarity scores (shape): {sim_scores.shape}")

    # Retrieve top reference paragraphs for each selected sentence
    for i, cand in enumerate(selected_candidates):
        d = find_top_reference(
            scores=sim_scores[:, i], ref_dict=ref_dict, length_limit=length_limit
        )

        candidates[cand["index"]]["max_score"] = d["max_score"]
        candidates[cand["index"]]["reference"] = "\n".join(
            ref_dict["parags"][index] for index in d["idx"]
        )

    return candidates


def split_paragraph_to_sentences(text: str, cleaning=True) -> list:
    """Split a text paragraph to a list of sentences
    Remove short sentences with less than 3 words
    Return:
        a list of sentences
    """
    if cleaning:
        text = clean_text(re.sub(r";", ".", text))
        return [
            " ".join(sent.text.split())
            for sent in nlp(text).sents
            if len(sent.text.split()) > 2
        ]
    else:
        return [sent.text for sent in nlp(text).sents]


def split_document_to_sentences(text: str) -> dict:
    """Split document first to paragraphs and then to sentences
    return:
        a dict: {'parags', 'word_counts', 'sents', 'idx'}
        words_counts: number of words in each paragraph
        idx: paragraph indexes of sentences
    """
    # Split document to paragraphs
    parags = list(filter(None, text.split("\n")))
    word_counts = [len(parag.split()) for parag in parags]

    # Split paragraph to sentences
    sents = []
    idx = []
    for i, parag in enumerate(parags):
        strs = split_paragraph_to_sentences(parag)
        sents.extend(strs)
        idx.extend([i] * len(strs))

    return {"parags": parags, "word_counts": word_counts, "sents": sents, "idx": idx}


def compute_sbert_scores(ref_strs: list, test_strs: list):
    """Use Sentence Transformer to compute cosine similarity scores
    between ref strings and test strings
    Returns:
         Cosine similarity scores in M x N numpy array
         M: length of ref_strs, N: length of test_strs
    """
    start = time.time()
    embeddings1 = sbert_model.encode(ref_strs)
    embeddings2 = sbert_model.encode(test_strs)
    scores = np.inner(embeddings1, embeddings2)
    end = time.time()
    logging.info(
        f"Time for similarity computation (SBert): {(end - start):.1f} seconds"
    )
    return scores


def slr_extract_judgment(jsondict: list) -> str:
    """Extract Judgment text from SAL JSON dict data.
    Output:
        text string for judgment
    """
    output_buf = []
    for data in jsondict:
        # Extract header text
        output_buf.append(data["header"]["text"])

        # Extract paragraph text
        for parag_data in data["paragraphs"]:
            if parag_data["paragraph_number"]:
                output_buf.append(
                    parag_data["paragraph_number"] + " " + parag_data["text"]
                )
            else:
                output_buf.append(parag_data["text"])

        # Extract table text
        for table_data in data["tables"]:
            rows = [row.replace("\t", " | ") for row in table_data]
            output_buf.append("\n".join(rows))

    text = "\n\n".join(output_buf)
    return text
