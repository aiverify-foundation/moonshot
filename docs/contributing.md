# Moonshot Contribution Guide

## Welcome

Welcome to Moonshot's Contributor Guide!

We always welcome community contributions to Moonshot, and the Moonshot team appreciates any help the community can give to make Moonshot better. This guide will help you understand how to contribute to the test assets in Moonshot.

* Submit your changes directly with a [pull request](https://github.com/aiverify-foundation/moonshot-data/pulls)
* Log a bug or make a feature request with an [issue](https://github.com/aiverify-foundation/moonshot/issues)

It is recommended that you follow these steps in order:

* [Prerequisites](#prerequisites) - what you need to do first before you can start contributing to Moonshot
* [Your First Contribution](#your-first-contribution) - things you need to do to make your first contribution
* [Contributing by Pull Requests](#contributing-by-pull-requests-prs) - contribute to our repository

## Prerequisites

Before contributing to Moonshot's test assets, you should first ensure that you have these ready:

### Create a Github Account

You will need to [sign up](https://github.com/signup) for a Github user account.

### Setting up your development environment

You will need to install both `moonshot` and `moonshot-data` to test your test assets.

Visit [this page](./getting_started/quick_install.md) to learn how to install the necessary dependencies.

### Contribution Scope

Currently, Moonshot is only accepting contributions for `moonshot-data`. This includes `connectors`, `metrics`, `benchmarks` (in the form of `dataset`, `recipe` and `cookbook`).

## Your First Contribution

### Adding a new connector

You can find a list of [available connectors here](https://github.com/aiverify-foundation/moonshot-data/tree/main/connectors).

For more details, you may refer to the HOW-TO guide on [how to add a new connector](./tutorial/contributor/create_connector.md).

### Adding a new metric

You can find a list of [available metrics here](https://github.com/aiverify-foundation/moonshot-data/tree/main/metrics).

The best way to start developing a new metric is to learn by an example. We have included a sample metric, [samplemetric.py](https://github.com/aiverify-foundation/moonshot-data/blob/main/metrics/samplemetric.py).

#### Modify Your Metric Metadata

Using `samplemetric.py` as an example, you can edit the following elements from line 20 to line 22.

1. `id`: This is the identifier of the metric that the user will use in their recipe or red teaming module. This should be the file name.
2. `name`: This is the name of the metric. This will be shown when the user lists the metrics.
3. `description`: This is the description of the metrics. This will be shown when the user lists the metrics. The description should describe what the metrics measure.

#### Add Evaluation Code

The core code should be written in `get_results`. In this function, you will have access to three parameters:

1. `prompts`: the list of prompts used to generate the predictions
2. `predicted_results`: the list of predicted responses based on the prompts
3. `targets`: the list of ground truth

In addition to these 3 parameters, you can also access user-defined metric configurations at line 23. Users provide their configurations through the `metrics_config.json` file.
```
{
    "samplemetric":{
        "endpoints": [
            "openai-gpt35-turbo-16k",
            "openai-gpt35-turbo"
        ],
        "threshold_value": "0.35",
        "num_of_prompts_to_calculate": 1
    }
}
```
!!! note
    Do you need to use an external model for your metric?<br>
    You have the flexibility to do so. For instance, you can use the transformers library to download a model from HuggingFace and run inference on the predicted responses.

#### Prepare Results

The output of a metric module must be a dictionary.

```
result = {
    "samplemetric": {"num_above_threshold": count},
    "grading_criteria": {"num_above_threshold": count},
}
```

The `grading_criteria` will be used by the grading scale in the recipe to assess the outcome of the test. The key `grading_criteria` must be present in the returned dictionary, but its value can be an empty dictionary. If the value is an empty dictionary, the report generated from the UI will display '-' as the grade.

### Adding a new dataset.

You can find a list of [available datasets here](https://github.com/aiverify-foundation/moonshot-data/tree/main/datasets).

To create a Moonshot-compatible dataset, you can convert your raw dataset into this format:

```
{
    "name": "name of the dataset",
    "description": "description",
    "license": "",
    "reference": "",
    "examples": [
        {
            "input": "prompt 1",
            "target": "ground truth"
        },

        {
            "input": "prompt 2",
            "target": "ground truth"
        }
        ....
    ]
}
```

To run your dataset, you need to create a [recipe](#adding-a-new-recipe) so that Moonshot knows how it can be evaluated. The filename of the dataset will serve as the unique identifier in the recipe. 

### Adding a new recipe

You can find a list of [available recipes here](https://github.com/aiverify-foundation/moonshot-data/tree/main/recipes).

To create a recipe, you can copy one of the recipe files and edit the following elements:

1. `id`: This is an unique identifier that will be used by the user. This should be the file name.
2. `name`: This is the name of the recipe, which will be displayed when a recipe is listed.
3. `description`: This describes what the recipe tests. We recommend also including what constitutes a better score and what that implies..
4. `tags`: This is a list of tags, which can help the user to find your recipe. We suggest to insert some relevant keywords related to domain and nature of the test.
5. `categories`: This helps to group the recipe. We suggest using `Trust & Safety`, `Capability` and `Quality`.
6. `datasets`: This contains a list of dataset identifiers used in this recipe. This dataset must be included in [this folder](https://github.com/aiverify-foundation/moonshot-data/tree/main/datasets).
7. `prompt_templates`: This contains a list of prompt templates used in this recipe. This prompt template must be found in [this folder](https://github.com/aiverify-foundation/moonshot-data/tree/main/prompt-templates).
8. `attack_modules`: A list of attack modules that is used in this recipe. The attack modules must be available in [this folder](https://github.com/aiverify-foundation/moonshot-data/tree/main/attack-modules).
9. `metrics`: This contains a list of metric identifiers used in this recipe. This metric must be included in [this folder](https://github.com/aiverify-foundation/moonshot-data/tree/main/metrics).
10. `grading_scale`: This grading scale helps to determine the outcome of the test. Leaving this empty will result in '-' as its grade in the report.

Here's an example recipe:

```
{
    "id": "recipe1",
    "name": "Recipe 1",
    "description": "This recipe measures performance of the system.",
    "tags": ["Safety"],
    "categories": ["Trust & Safety"],
    "datasets": ["dataset1"],
    "prompt_templates": [],
    "metrics": ["exactstrmatch"],
    "attack_modules": [],
    "grading_scale": {
        "A": [
            80,
            100
        ],
        "B": [
            60,
            79
        ],
        "C": [
            40,
            59
        ],
        "D": [
            20,
            39
        ],
        "E": [
            0,
            19
        ]
    }
}
```

### Adding a new cookbook

You can find a list of [available cookbooks here](https://github.com/aiverify-foundation/moonshot-data/tree/main/cookbooks).

To create a cookbook, you can copy one of the cookbook files and edit the following elements:

1. `id`: This is an unique identifier that will be used by the user. This should be the file name.
2. `name`: This is the name of the recipe, which will be displayed when a recipe is listed.
3. `description`: This describes what the recipe test.
4. `recipes`: This contains a list of recipe identifiers that this cookbook will execute. These recipes must be found in [this folder](https://github.com/aiverify-foundation/moonshot-data/tree/main/recipes).

Here's an example cookbook:

```
{
    "id": "example-cookbook",
    "name": "Example Cookbook",
    "description": "This cookbook measures the system performance. ",
    "recipes": [
        "recipe1",
        "recipe2"
    ]
}
```

## Contributing by Pull Requests (PRs)

Any contributions are greatly appreciated.

Please fork the repo and create a pull request. You can also open an issue with the tag `"enhancement"`. Do give the project a star too!

1. Fork the `moonshot-data` Project
2. Install `moonshot` (to run your test assets)
3. Create your branch (`git checkout -b connector/X` or `git checkout -b metric/X` or `git checkout -b cookbook/X` or `git checkout -b recipe/X` or ... )
4. Push to the branch (`git push origin metric/X`)
5. Open a Pull Request