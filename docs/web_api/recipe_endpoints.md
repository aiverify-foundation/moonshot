# Moonshot Recipe API Endpoints

<details>
<summary> [GET] /v1/recipes</summary>
This endpoint is use to get all recipes.
<br/>
<b> Parameters (body)</b> : None
<br/>
<b>Success Response: </b>
```json
[
    {
        "id": "squad-shifts-tnf",
        "name": "squad-shifts-tnf",
        "description": "Zero-shot reading comprehension on paragraphs and questions from squadshifts. Augmented to true/false statement.",
        "tags": [],
        "datasets": [
            "squad-shifts-tnf"
        ],
        "prompt_templates": [],
        "metrics": [
            "relaxstrmatch"
        ]
    },
    {
        "id": "tamil-kural-classification",
        "name": "TAMIL-KURAL-CLASSIFICATION",
        "description": "This recipe is used to test the comprehension abilities for the Thirukkural. Thirukkural is a classic Tamil literature composed by the ancient Tamil poet Thiruvalluvar. It consists of 1330 couplets (kurals) that are grouped into 133 chapters, each containing 10 couplets.",
        "tags": [
            "tamil",
            "text classification"
        ],
        "datasets": [
            "tamil-kural-classification"
        ],
        "prompt_templates": [
            "tamil-templatekuralclassification"
        ],
        "metrics": [
            "exactstrmatch"
        ]
    }
]
```
</details>

<details>
<summary>[POST] /v1/recipes</summary>
This endpoint is use to create new recipe.
<br/>
<b> Parameters (body): </b>
```json
{
    "name": "string",
    "description": "string",
    "tags": ["string"],
    "datasets": ["string"],
    "prompt_templates": ["string"],
    "metrics": ["string"]
}
``` 
<b>Example</b> 
<br/>
```json
{
    "name": "Measuring Tape 2",
    "description": "Test Recipe",
    "tags": [],
    "datasets": [
        "winogrande"
    ],
    "prompt_templates": [
        "question-answer-template1"
    ],
    "metrics": [
        "exactstrmatch"
    ]
}
```
<b>Success Response: </b>
```json
{
    "message": "Recipe created successfully"
}
```
</details>


<details>
<summary>[DELETE] /v1/recipes/{recipe_id}</summary>
This endpoint is use to delete an existing recipe.
<br/>
<b> Parameters (path)</b> :<code>recipe_id</code>: The ID of the recipe to delete.
<br/>
<b>Example: </b>  <code>/v1/recipe/sample-recipe</code>
<br/>
<b>Success Response: </b>
```json
{
    "message": "Recipe deleted successfully"
}
```
</details>
