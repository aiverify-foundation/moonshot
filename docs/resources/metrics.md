# List of Metrics

| Name | Description |
|------|-------------|
| Attack Success Rate | Attack success rate measures how successful a changed prompt performs. A high score shows that the system under test is highly sensitive towards a prompt with minimal changes. |
| BertScore | BertScore uses Bert to check for the similarity in embedding between two sentences. |
| SpellingScore | SpellingScore uses Levenshetein Distance to find permutations within an edit distance of 2 form the original word before comparing to known words in a word frequency list. |
| GPT4 Annotator | Calculates the number of refused response using GPT4. |
| BleuScore | Bleuscore uses Bleu to return the various rouge scores. |
| ReadabilityScore | ReadabilityScore uses Flesch Reading Ease to compute the complexity of the output |
| Toxicity Classifier | This classifier measures how toxic a given input isand calculate the number of toxic sentence detected. |
| RougeScorer | RougeScorer returns the various rouge scores. |
| Attack Success Rate | Attack success rate measures how successful a changed prompt performs. A high score shows that the system under test is highly sensitive towards a prompt with minimal changes. |
| LeakageRate | Leakage Rate will compare the LCS between two string - Output and Target. |
| ReverseExactStrMatch | ReverseExactStrMatch will compare the output from language model with the expected target. |
| ExactStrMatch | ExactStrMatch will compare the output from language model with a single target or multiple expected target. |
| RelaxStrMatch | RelaxStrMatch will remove symbols and spaces before comparing the output from language model with the expected target. |
| LlamaGuard Annotator | Calculates the number of safe, unsafe and unknown response by using LlamaGuard. |
| SampleMetric | Sample Metric will provide examples on connecting to LLMs. |
| LionGuard Classifier | This classifier measures how unsafe a given input is in the Singapore context. It can calculate the number of toxic sentences detected. |
| FlagJudge Annotator | Calculates the number of correct response using FlagJudge (A judge model from FlagEval Group). |