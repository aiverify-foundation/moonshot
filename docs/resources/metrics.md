# List of Metrics

| Name | Description |
|------|-------------|
| AnswerCarefullyAnnotator <br> *answercarefully-annotator.py* | Calculates the number of undesired, no undesired and unknown response by using GPT4o. |
| AnswerCorrectness <br> *answercorrectness.py* | Answer correctness in the context of Ragas involves evaluating the accuracy of a generated answer compared to the ground truth. This process assesses both the semantic and factual similarities between the answer and the ground truth. Scores range from 0 to 1, where a higher score indicates a closer match, thus higher correctness.|
| AnswerRelevance <br> *answerrelevance.py* | The evaluation metric, Answer Relevancy, focuses on assessing how pertinent the generated answer is to the given prompt. A lower score is assigned to answers that are incomplete or contain redundant information and higher scores indicate better relevancy. This metric is computed using the question, the context and the answer. |
| Attack Success Rate <br> *advglue.py* | Attack success rate measures how successful a changed prompt performs. A high score shows that the system under test is highly sensitive towards a prompt with minimal changes. |
| BertScore <br> *bertscore.py* | BertScore uses Bert to check for the similarity in embedding between two sentences. |
| BleuScore <br> *bleuscore.py* | Bleuscore uses Bleu to return the various rouge scores. |
| ContextPrecision <br> *contextprecision.py* | Context Precision is a metric that evaluates whether all of the ground-truth relevant items present in the contexts are ranked higher or not. Ideally, all the relevant chunks must appear at the top ranks. This metric is computed using the question, ground_truth, and the contexts, with values ranging between 0 and 1, where higher scores indicate better precision. |
| ContextRecall <br> *contextrecall.py* | Context recall measures the extent to which the retrieved context aligns with the annotated answer, treated as the ground truth. It is computed using question, ground truth and the retrieved context, and the values range between 0 and 1, with higher values indicating better performance. |
| EntityProcessor <br> *entity_processor.py* | This metric is designed to process and analyse text to identify entities using the spaCy library. The class also has searches for entities in a given text that do not appear in a source text, labeling them as "unmatched" or "hallucinated" entities. |
| ExactStrMatch <br> *exactstrmatch.py* | ExactStrMatch will compare the output from language model with a single target or multiple expected target. |
| ExactStrMatchF1SquadV2 <br> *exactstrmatch-f1-squad-v2.py* | ExactStrMatch will compare the output from language model with a single target or multiple expected target.|
| ExactStrMatchGSM8k <br> *exactstrmatch-gsm8k-test.py* | ExactStrMatch will compare the output from language model with a single target or multiple expected target. |
| Faithfulness <br> *faithfulness.py* | This measures the factual consistency of the generated answer against the given context. It is calculated from answer and retrieved context. The answer is scaled to (0,1) range. Higher the better.|
| FlagJudge Annotator <br> *flagjudgeannotator.py* | Calculates the number of correct response using FlagJudge (A judge model from FlagEval Group). |
| GenderBiasMetric <br> *genderbias_metric.py* | This metric uses a CLIP based gender classifier to determine the proportion of females returning a score between 0 and 0.5. score = \|female_frac - 0.5\| |
| LlamaGuard Annotator <br> *llamaguardannotator.py* | Calculates the number of safe, unsafe and unknown response by using LlamaGuard. |
| LeakageRate <br> *leakagerate.py* | Leakage Rate will compare the LCS between two string - Output and Target. |
| MLCPRVAnnotator <br> *mlcprv-annotator.py* | Calculates the number of acceptable, unacceptable and unknown response by using GPT4o. |
| MLCIPV Annotator <br> *mlcipv-annotator.py* | Calculates the number of acceptable, unacceptable and unknown response by using GPT4o. |
| MLCNCR Annotator <br> *mlcncr-annotator.py* | Calculates the number of acceptable, unacceptable and unknown response by using GPT4o. |
| MLCVCR Annotator <br> *mlcvcr-annotator.py* | Calculates the number of acceptable, unacceptable and unknown response by using GPT4o. |
| NudeNetMetric <br> *nudenet_metric.py* | NudeNet is a classifier used to deduce probabilities of exposed body parts in images. |
| Q16Metric <br> *q16_metric.py* | Q16 is a binary classifier used to determine whether an image is inappropriate (https://github.com/ml-research/Q16) |
| ReadabilityScore <br> *readabilityscore.py* | ReadabilityScore uses Flesch Reading Ease to compute the complexity of the output |
| RelaxStrMatch <br> *relaxstrmatch.py* | RelaxStrMatch will remove symbols and spaces before comparing the output from language model with the expected target. |
| ReverseExactStrMatch <br> *reverseexactstrmatch.py* | ReverseExactStrMatch will compare the output from language model with the expected target. |
| RougeScorer <br> *rougescorer.py* | RougeScorer returns the various rouge scores. |
| SpellingScore <br> *spelling.py* | SpellingScore uses Levenshtein Distance to find permutations within an edit distance of 2 from the original word before comparing to known words in a word frequency list.|
| Toxicity Classifier <br> *toxicity-classifier.py* | This classifier measures how toxic a given input is and calculates the number of toxic sentences detected.|
| Cybersec Eval Prompt Injection v2 <br> *cybersecevalannotator2.py* | Calculates number of Success and Unsuccessful reply by judge llm. |
| General Judge LLM <br> *cybersecevalannotator.py* | Calculates number of yes and no replied by judge llm  (yes means prompt injection succeed) |