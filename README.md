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
**Version 0.2.5**

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

    </br>

## Running Moonshot
### Web API
To run Moonshot Web API:
```
$ python -m moonshot web-api
```

For instructions on setting up the Moonshot UI, please refer to the [Moonshot UI repository](https://github.com/moonshot-admin/moonshot-ui).

</br>

## Quickstart Guide

Users can use this tool to run benchmark tests and perform red teaming on LLMs. Before doing these, we need to configure a LLM endpoint to connect to. Currently, these are the connectors we support out of the box for connectiong to LLMs:
    
| LLM | LLM Connector Name |
| --- | ----------- |
| OpenAI GPT4 |  `openai-gpt4`|
| OpenAI GPT3.5 Turbo 16k | `openai-gpt35-turbo-16k` |
| OpenAI GPT3.5 |`openai-gpt35` |
| Hugging Face Llama2 13B GPTQ | `hf-llama2-13b-gptq` |
| Anthropic Claude2    | `claude2` |
| OpenAI GPT2 (Hugging Face)    | `hf-gpt2` |

### Configuring Your Connector

If you see the LLM you are connecting to in our list of supported connectors, good for you! You can simply configure the connector by referring to --insert link to sample JSON file-- by doing the following:
    
1. Make a copy of the sample JSON file in the same directory and rename the file to your liking. Let's say I want to connect to GPT4, and I have renamed the file to  ```my-gpt4-config.json ```.

2. Modify the contents of ```my-gpt4-config.json ```:
    ```
    {
        "id": "my-gpt4-config",
        "name": "my-gpt4-config",
        "connector_type": "openai-gpt4", 
        "uri": "", 
        "token": "my-api-token",
        "max_calls_per_second": 100,
        "max_concurrency": 100,
        "params": {
            "timeout": 234,
            "allow_retries": true,
            "num_of_retries": 3
        }
    }
    ```

If you do not see the connector for the LLM you want to connect to, fret not. You can refer to --insert link to connector.py files--. You can simply make a copy of the Python in the same directory, modify the name of the class and the logic inside the file. 

When you have configured your connector, you can start doing your benchmark tests and red teaming!

### Running Benchmark Tests
To start running a benchmark, you will have to first select your Recipe or Cookbook. So what is a <b>Recipe</b> and a <b>Cookbook</b>?

<b>Recipe</b>: A file which contains the dataset(s), prompt template(s) and metric(s) to run for a benchmark. Click on the links to find out more.

<b>Cookbook</b>: A file which contains a collection of <b>Recipes</b>

1. Select a Recipe/Cookbook to run 
   
    ```
    Codes to select recipe
    ```

2. Execute the Recipe/Cookbook
    ```
    Codes to execute recipe
    ```

3. View results of the run
    ```
    Codes to view results
    ```

### Performing Red Teaming

To start red teaming, you will first have to create a <b>Session</b>. 

<b>Session</b>: A Session helps users to send prompts to multiple LLM endpoints. Each LLM endpoint will have a <b>Chat</b>, which stores the conversation between users and the LLM. 

1. Create/Resume a Session
```
    Codes to create/resume session
```

2. Send a prompt
```
    Codes to send prompt
```
3. View the responses from the LLM
```
    Codes to view response
```


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
