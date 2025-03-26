# List of Metrics

| Name | Description |
|------|-------------|
| Refusal Evaluator | This metric calculates the number of refused response using GPT4o. |
| MLCPRVAnnotator | Calculates the number of acceptable, unacceptable and unknown response by using GPT4o. |
| BertScore | BertScore uses Bert to check for the similarity in embedding between two sentences. |
| SpellingScore | SpellingScore uses Levenshetein Distance to find permutations within an edit distance of 2 form the original word before comparing to known words in a word frequency list. |
| GPT4 Annotator | Calculates the number of refused response using GPT4. |
| BleuScore | Bleuscore uses Bleu to return the various rouge scores. |
| Faithfulness | This measures the factual consistency of the generated answer against the given context. It is calculated from answer and retrieved context. The answer is scaled to (0,1) range. Higher the better. |
| ReadabilityScore | ReadabilityScore uses Flesch Reading Ease to compute the complexity of the output |
| ExactStrMatchF1SquadV2 | ExactStrMatch will compare the output from language model with a single target or multiple expected target. |
| Q16Metric | Q16 is a binary classifier used to determine whether an image is inappropriate (https://github.com/ml-research/Q16) |
| MLCIPV Annotator | Calculates the number of acceptable, unacceptable and unknown response by using GPT4o. |
| Toxicity Classifier | This classifier measures how toxic a given input isand calculate the number of toxic sentence detected. |
| MLCNCR Annotator | Calculates the number of acceptable, unacceptable and unknown response by using GPT4o. |
| NudeNetMetric | NudeNet is a classifier used to deduce probabilities of exposed body parts in images. |
| RougeScorer | RougeScorer returns the various rouge scores. |
| AnswerCorrectness | Answer correctness in the context of Ragas involves evaluating the accuracy of a generated answer compared to the ground truth. This process assesses both the semantic and factual similarities between the answer and the ground truth. Scores range from 0 to 1, where a higher score indicates a closer match, thus higher correctness. |
| GenderBiasMetric | This metric uses a CLIP based gender classifier to determine the proportion of females returning a score between 0 and 0.5. score = |female_frac - 0.5| |
| Attack Success Rate | Attack success rate measures how successful a changed prompt performs. A high score shows that the system under test is highly sensitive towards a prompt with minimal changes. |
| ContextRecall | Context recall measures the extent to which the retrieved context aligns with the annotated answer, treated as the ground truth. It is computed using question, ground truth and the retrieved context, and the values range between 0 and 1, with higher values indicating better performance. |
| LeakageRate | Leakage Rate will compare the LCS between two string - Output and Target. |
| LionGuard Classifier | This classifier measures how unsafe a given input is in the Singapore context.
It can calculate the number of toxic sentences detected.  |
| ReverseExactStrMatch | ReverseExactStrMatch will compare the output from language model with the expected target. |
| AnswerCarefullyAnnotator | Calculates the number of undesired, no undesired and unknown response by using GPT4o. |
| EntityProcessor | This metric is designed to process and analyse text to identify entities using the spaCy library.The class also has searches for entities in a given text that do not appear in a source text, labeling them as "unmatched" or "hallucinated" entities. |
| FlagJudge Annotator | Calculates the number of correct response using FlagJudge (A judge model from FlagEval Group). |
| ExactStrMatch | ExactStrMatch will compare the output from language model with a single target or multiple expected target. |
| General Judge LLM | Calculates number of yes and no replied by judge llm  (yes means prompt injection succeed) |
| RelaxStrMatch | RelaxStrMatch will remove symbols and spaces before comparing the output from language model with the expected target. |
| LlamaGuard Annotator | Calculates the number of safe, unsafe and unknown response by using LlamaGuard. |
| ExactStrMatchGSM8k | ExactStrMatch will compare the output from language model with a single target or multiple expected target. |
| SampleMetric | Sample Metric will provide examples on connecting to LLMs. |
| ContextPrecision | Context Precision is a metric that evaluates whether all of the ground-truth relevant items present in the contexts are ranked higher or not. Ideally, all the relevant chunks must appear at the top ranks. This metric is computed using the question, ground_truth, and the contexts, with values ranging between 0 and 1, where higher scores indicate better precision. |
| Cybersec Eval Prompt Injection v2 | Calculates number of Success and Unsuccessful reply by judge llm |
| AnswerRelevance | The evaluation metric, Answer Relevancy, focuses on assessing how pertinent the generated answer is to the given prompt. A lower score is assigned to answers that are incomplete or contain redundant information and higher scores indicate better relevancy. This metric is computed using the question, the context and the answer. |
| MLCVCR Annotator | Calculates the number of acceptable, unacceptable and unknown response by using GPT4o. |