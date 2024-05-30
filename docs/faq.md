# FAQ

## Installation 

### How do I get started?

To install Moonshot, please follow our [quick start guide](./getting_started/) or [quick install page](./getting_started/quick_start.md) 


### What are Moonshot's prerequisites?

Here are the requirements. You can also find this table in our [quick install page](./getting_started/quick_start.md).

 | Software                                                                           | Version Requirement |
| ---------------------------------------------------------------------------------- | ------------------- |
| [Python](https://www.python.org/downloads/)                                        | v3.11               |
| [NodeJs](https://nodejs.org/en/download)                                           | v20.11.1 LTS or above               |
| npm                                        | v10.8.0 or above               |
| git       

### Should I use the stable version or development version?

If you are using Moonshot in production, you should use a stable release. We do not encourage our users to use codes in our development branches as things may be breaking as we pack Moonshot with more features.

### Where can I go to get help?

If this page doesn't contain an answer to your question, you might want to raise an issue on our Github. Feel free to ask any question!

### What should I do when I face missing dependency errors?

We highly recommend using `pypi` to install our latest release.

### What happens if I'm not using Python 3.11?

You may face issues installing some of the dependencies. We suggest using virtual environment of your choice and use Python 3.11 with Moonshot.

### What happens if I experience timeouts during package installation?

Some of the functions may not work as expected. We suggest users to reinstall Moonshot to ensure that all libraries are installed successfully.

## Using Moonshot

### My tests are all completed with errors! I can't view any report!

Some benchmark tests and attack modules require connector endpoints to be configured beforehand. You may encounter this type of error:

![](./getting_started/getting_started/8.png)

Some examples are:

| Test | Model Required | Name of the Endpoint |
| --- | ---| --- |
| MLCommons AI Safety Benchmarks v0.5 (Cookbook) | Meta LlamaGuard | Together Llama Guard 7B Assistant | 
| Singapore Safety (Recipe) | Meta LlamaGuard | Together Llama Guard 7B Assistant | 
| Malicious Question Generator (Attack Module) | OpenAI GPT4 | OpenAI GPT4 | 
| Violent Durian (Attack Module) | OpenAI GPT4 | OpenAI GPT4 |

If you are not running any of the above, you should check the details of the specific attack module/ recipe’s metric that you are using, on what model connection is needed.

If you do not have tokens for Llama Guard via Together AI, 

1.	Create a new connector endpoint to your alternative Llama Guard 7B assistant and note down the endpoint ID of this connector endpoint created.
2.	Open up `moonshot-data/metrics_config.json` in a code editor
3.	Replace `together-llama-guard-7b-assistant` with your new endpoint ID.
4.	Save the file and run your test.

### I can't delete my runner in the CLI on Windows.

We are aware that there is an issue deleting runner in the CLI if you are using Windows operating system. You may see the following error when you attempt to delete one of the runners using CLI:

```
moonshot > delete_runner new-recipe
Are you sure you want to delete the runner (y/N)? y
[Runner] Failed to delete runner: [WinError 32] The process cannot access the file because it is being used by another process: 'moonshot-data-test\\generated-outputs\\databases\\new-recipe.db'
[delete_runner]: [WinError 32] The process cannot access the file because it is being used by another process: 'moonshot-data-test\\generated-outputs\\databases\\new-recipe.db'
```

We are working to produce a fix. In the meanwhile, please exit the program and delete it via your file explorer.

### I can't save my token for the connector endpoint!

We acknowledge a potential issue with saving tokens via the UI. As a workaround, you can directly access the JSON file of your endpoint. This file is located in the `moonshot-data/connector-endpoints` directory, which was created during the installation process.

### I cannot see my newly created endpoints in the model endpoint page.

Please refresh the page.