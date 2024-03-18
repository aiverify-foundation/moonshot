# Moonshot Cookbook API Endpoints

<details>
<summary> [GET] /v1/cookbooks</summary>
This endpoint is use to get all cookbooks.
<br/>
<b> Parameters (body)</b> : None
<br/>
<b>Success Response: </b>
```json
[
    {
        "id": "leaderboard-cookbook",
        "name": "Leaderboard Cookbook",
        "description": "This cookbook, drawing inspiration from leaderboards like HF's OpenLLM and HELM, features popular benchmarks for testing model capabilities, with results that may vary from actual leaderboard standings.",
        "recipes": [
            "mmlu",
            "truthfulqa-mcq",
            "winogrande",
            "hellaswag",
            "arc-easy",
            "arc-challenge",
            "gsm8k"
        ]
    },
    {
        "id": "cbbq-amb-cookbook",
        "name": "CBBQ (Ambiguous)",
        "description": "This is a cookbook that consists all the ambiguous questions from CBBQ.",
        "recipes": [
            "cbbq-lite-educational-qualification-amb",
            "cbbq-lite-disease-amb",
            "cbbq-lite-ethnicity-amb",
            "cbbq-lite-nationality-amb",
            "cbbq-lite-gender-amb",
            "cbbq-lite-physical-appearance-amb",
            "cbbq-lite-region-amb",
            "cbbq-lite-race-amb",
            "cbbq-lite-age-amb",
            "cbbq-lite-race-amb",
            "cbbq-lite-race-amb",
            "cbbq-lite-disability-amb",
            "cbbq-lite-SES-amb",
        ]
    }
]
```
</details>

<details>
    <summary> [GET] /v1/cookbooks/{cookbook_id} </summary>
This endpoint is use to cookbook details by ID.
<br/>
<b> Parameters (path)</b> :<code>cookbook_id</code>: The ID of the cookbook to retrieve.
<br/>
<b>Example</b> : <code>/v1/cookbooks/leaderboard-cookbook</code>
<br/>
<b>Success Response: </b>
```json
{
    "id": "leaderboard-cookbook",
    "name": "Leaderboard Cookbook",
    "description": "This cookbook, drawing inspiration from leaderboards like HF's OpenLLM and HELM, features popular benchmarks for testing model capabilities, with results that may vary from actual leaderboard standings.",
    "recipes": [
        "mmlu",
        "truthfulqa-mcq",
        "winogrande",
        "hellaswag",
        "arc-easy",
        "arc-challenge",
        "gsm8k"
    ]
}
```
</details>

<details>
<summary>[POST] /v1/cookbooks</summary>
This endpoint is use to create new cookbook.
<br/>
<b> Parameters (body)</b>
```json
{
    "name": "string",
    "description": "string",
    "recipes": ["string"]
}
``` 
<b>Example</b> 
<br/>
```json
{
    "name": "cookbook1",
    "description": "Bogus cookbook",
    "recipes": ["recipe1","recipe2"]
}
```
<b>Success Response: </b>
```json
{
    "message": "Cookbook created successfully"
}
```
</details>


<details>
<summary>[PUT] /v1/cookbooks/{cookbook_id}</summary>

This endpoint is use to update an existing cookbook.
<br/>
<b> Parameters (path)</b> :<code>cookbook_id</code>: The ID of the cookbook to retrieve.
<br/>
<b> Parameters (body): </b>
```json
{
    "name": "string",
    "description": "string",
    "recipes": ["string"]
}

``` 
<b>Example</b> 
<br/>
<code>/v1/cookbooks/cookbook1</code>
```json
{
    "name": "cookbook1-A",
    "description": "Bogus cookbook A",
    "recipes": ["recipe1","recipe2"]
}
```
<b>Success Response: </b>
```json
{
    "message": "Cookbook updated successfully"
}
```
</details>