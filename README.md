<div align="center">

```
  _____           _           _     __  __                       _           _   
 |  __ \         (_)         | |   |  \/  |                     | |         | |  
 | |__) | __ ___  _  ___  ___| |_  | \  / | ___   ___  _ __  ___| |__   ___ | |_ 
 |  ___/ '__/ _ \| |/ _ \/ __| __| | |\/| |/ _ \ / _ \| '_ \/ __| '_ \ / _ \| __|
 | |   | | | (_) | |  __/ (__| |_  | |  | | (_) | (_) | | | \__ \ | | | (_) | |_ 
 |_|   |_|  \___/| |\___|\___|\__| |_|  |_|\___/ \___/|_| |_|___/_| |_|\___/ \__|
                _/ |                                                             
               |__/                                                              

```
**Version 0.3.0**

A simple and modular tool to evaluate and red-team any LLM application.

[![Python 3.11](https://img.shields.io/badge/python-3.11-green)](https://www.python.org/downloads/release/python-3111/)


</div>

Moonshot is a tool designed for AI developers and security experts to evaluate and red-team any LLM/ LLM application. In this initial version, Moonshot can be used through its interative Command Line Interface, within python notebooks [(example)](https://github.com/moonshot-admin/moonshot/tree/main/examples/test-openai-gpt35.ipynb), or even seamlessly integrated into your model development workflow to to run repeatable tests.



## Getting Started
### Prerequisites
1. Python (at least version 3.11)

2. Virtual Environment (optional) - Good to have different environments to separate Python dependencies

    - Create a virtual environment:
    ```
    python -m venv venv
    ```
    - Activate the virtual environment:
    ```
    source venv/bin/activate
    ```
### Installation
The source code is available on GitHub at: [https://github.com/moonshot-admin/moonshot](https://github.com/moonshot-admin/moonshot)
```
$ pip install projectmoonshot-imda # To install Moonshot library.
$ pip install "projectmoonshot-imda[web-api]" # To enable running Moonshot using the web API.
```
#### Installation from source
1. Download the source files by cloning this repository. i.e. Git clone (via SSH): 
    
    ```
    $ git clone git@github.com:moonshot-admin/moonshot.git
    ```
2. Change directory to project's root directory: 

    ```
    $ cd moonshot
    ```

3. Install the required packages: 

    ```
    $ pip install -r requirements.txt
    ```

## Running Moonshot
### Web API
To run Moonshot Web API:
```
$ python -m moonshot web-api
```

For instructions on setting up the Moonshot UI, please refer to the [Moonshot UI repository](https://github.com/moonshot-admin/moonshot-ui).

## Acknowledgements

### Datasets used in Moonshot recipes
| Dataset       | Source           | License           |
| :-------------:|:-------------:| :-------------:|
|AdvGLUE|https://adversarialglue.github.io/|Creative Commons Attribution 4.0 International|
|Analogical Similarity|https://github.com/google/BIG-bench/tree/main/bigbench/benchmark_tasks/analogical_similarity |Apache License Version 2.0, January 2004  |
|AI2 Reasoning Challenge |https://allenai.org/data/arc|Creative Commons Attribution-ShareAlike 4.0 International|
|Auto Categorization |https://github.com/google/BIG-bench/tree/main/bigbench/benchmark_tasks/auto_categorization|Apache License Version 2.0, January 2004|
|BBQ|https://github.com/nyu-mll/BBQ|Creative Commons Attribution 4.0 International| 
|CBBQ|https://github.com/YFHuangxxxx/CBBQ| Creative Commons Attribution Share Alike 4.0 International|
|Cause and Effect|https://github.com/google/BIG-bench/tree/main/bigbench/benchmark_tasks/cause_and_effect|Apache License Version 2.0, January 2004|
|Challenging Toxicity Prompts|https://decodingtrust.github.io/|Creative Commons Attribution ShareAlike 4.0 International|
|Contextual Parametric Knowledge|https://github.com/google-research/language|Apache License Version 2.0, January 2004|
|CoQA|https://stanfordnlp.github.io/coqa/|Creative Commons Attribution 4.0 International; MSR-LA;     Apache License Version 2.0, January 2004|
|CValues|https://github.com/X-PLUG/CValues/tree/main|Apache License Version 2.0, January 2004|
|Enron Email|https://github.com/ParakweetLabs/EmailIntentDataSet|Apache License Version 2.0, January 2004| 
|GRE Reading Comprehension|https://github.com/google/BIG-bench/tree/main/bigbench/benchmark_tasks/gre_reading_comprehension|Apache License Version 2.0, January 2004|
|GSM8K|https://github.com/openai/grade-school-math|MIT License|
|HellaSwag|https://github.com/rowanz/hellaswag|MIT License|
|MMLU|https://github.com/hendrycks/test|MIT License|
|TR9856|https://aclanthology.org/P15-2069.pdf|Creative Commons Attribution 3.0 International|
|Winogrande|https://github.com/allenai/winogrande|Apache-2.0 License|
|WORD|https://aclanthology.org/L18-1408/|Creative Commons Attribution 3.0 International|
|Real Toxicity Prompts|https://github.com/allenai/real-toxicity-prompts/|Apache License Version 2.0, January 2004|
|Stanford Question Answering Dataset (SQuAD)|https://modestyachts.github.io/squadshifts-website/|Creative Commons Attribution 4.0 International|
|Tanglish Tweets for Sentiment Ananlysis|https://www.kaggle.com/datasets/vyombhatia/tanglish-comments-for-sentiment-ananlysis/data|Creative Commons Attribution 1.0 International|
|Tamil News Classification|https://github.com/vanangamudi/tamil-news-classification/tree/master/dataset/news|GNU General Public License v3.0|
|Thirukkural Dataset|https://github.com/vijayanandrp/Thirukkural-Tamil-Dataset|Creative Commons Attribution 4.0 International|
|TruthfulQA|https://github.com/sylinrl/TruthfulQA|Apache License Version 2.0, January 2004|
|UCI Adult|https://archive.ics.uci.edu/dataset/2/adult|Creative Commons Attribution 4.0 International|

## License
Licensed under [Apache Software License 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt)
