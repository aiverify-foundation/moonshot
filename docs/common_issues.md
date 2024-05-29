# Common Issues

## Missing Dependencies

Error: This can lead to installation failures or runtime errors.

Troubleshoot: Check the toolkit's documentation for a list of dependencies and ensure they are installed using pip or your system's package manager.

## Python Version Compatibility

Error: An outdated version can lead to compatibility issues.

Troubleshoot: Verify the Python version requirements in the documentation. If your Python version is not compatible, consider using a virtual environment with the correct Python version.

## Network Issues

Error: Interrupted downloads or timeouts during package installation.

Troubleshoot: Check your internet connection and try again. Consider using a mirror for package repositories if available. You can also download the package manually and install it using pip.

## Conflicting Packages

Error: Fail install if there are conflicting versions of packages already installed on your system.

Troubleshoot: Use a virtual environment to isolate the toolkit and its dependencies from other Python packages. Alternatively, uninstall conflicting packages or use package version pinning to ensure compatibility.

## Missing connections to required models

Error: Failure to generate benchmarking scores/ automated attack prompts

Troubleshoot: Failure to generate benchmarking scores/ automated attack prompts might be due to missing connections to models required for metrics/ attack modules.

If you are running these cookbooks/ recipes, you will need connection to Llama Guard via Together AI:
-	MLCommons AI Safety Benchmarks v0.5
-	Facts about Singapore

If you are running these attack modules, you will need connection to OpenAI’s GPT4:
-	Malicious Question Generator
-	Violent Durian
If you are not running any of the above, you should check the details of the specific attack module/ recipe’s metric that you are using, on what model connection is needed.

If you do not have tokens for Llama Guard via Together AI, 

1.	Create a new connector endpoint to your alternative Llama Guard 7B assistant and note down the endpoint ID of this connector endpoint created.
2.	Open up moonshot-data/metrics_config.json in a code editor
3.	Replace “together-llama-guard-7b-assistant” with your new endpoint ID.
4.	Save the file and run your test.

## CLI - Unable to delete runner

You may encounter this error when you delete a runner in CLI on Windows operating system.

```
moonshot > delete_runner new-recipe
Are you sure you want to delete the runner (y/N)? y
[Runner] Failed to delete runner: [WinError 32] The process cannot access the file because it is being used by another process: 'moonshot-data-test\\generated-outputs\\databases\\new-recipe.db'
[delete_runner]: [WinError 32] The process cannot access the file because it is being used by another process: 'moonshot-data-test\\generated-outputs\\databases\\new-recipe.db'
```

For temporary fix, please exit the program and delete it via your file explorer.

