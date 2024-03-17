from moonshot.api import (
    api_create_recipe,
    api_delete_recipe,
    api_get_all_recipes,
    api_get_all_recipes_names,
    api_read_recipe,
    api_read_recipes,
    api_update_recipe,
)


# ------------------------------------------------------------------------------
# Recipes APIs Test
# ------------------------------------------------------------------------------
def test_create_recipe():
    api_create_recipe(
        name="my new recipe",
        description="Consists of adversarially perturned and benign MNLI and MNLIMM datasets. MNLI consists is a crowd-sourced collection of sentence pairs with textual entailment annotations. Given a premise sentence and a hypothesis sentence, the task is to predict whether the premise entails the hypothesis.",
        tags=["robustness"],
        datasets=["dataset1", "dataset2"],
        prompt_templates=["prompt-template1"],
        metrics=["metrics1", "metrics2"],
    )


def test_read_recipe():
    print(api_read_recipe("my-new-recipe"))


def test_read_recipes():
    recipes = api_read_recipes(["my-new-recipe", "my-new-recipe", "my-new-recipe"])
    for recipe_no, recipe in enumerate(recipes, 1):
        print("-" * 100)
        print("Recipe No. ", recipe_no)
        print(recipe)


def test_update_recipe():
    api_update_recipe(
        "my-new-recipe",
        description="my new description.",
        tags=["fairness"],
        datasets=["dataset2", "dataset5"],
        prompt_templates=["prompt-template2"],
        metrics=["metrics3"],
    )


def test_delete_recipe():
    # Delete recipe if do not exists
    try:
        api_delete_recipe("recipe123")
        print("Delete recipe if exist: FAILED")
    except Exception as ex:
        print(f"Delete recipe if do not exist: PASSED")

    # Delete recipe if exists
    try:
        api_delete_recipe("my-new-recipe")
        print("Delete recipe if exist: PASSED")
    except Exception:
        print("Delete recipe if exist: FAILED")


def test_get_all_recipes():
    print(api_get_all_recipes())


def test_get_all_recipes_names():
    print(api_get_all_recipes_names())


def test_run_recipe_api():
    # Create recipe
    print("=" * 100, "\nTest creating recipe")
    test_create_recipe()

    # Read recipe
    print("=" * 100, "\nTest reading recipe")
    test_read_recipe()

    # Update recipe
    print("=" * 100, "\nTest updating recipe")
    test_update_recipe()

    # Read recipe
    print("=" * 100, "\nTest reading recipe after updating")
    test_read_recipe()

    # Read recipes
    print("=" * 100, "\nTest reading recipes")
    test_read_recipes()

    # Delete recipe
    print("=" * 100, "\nTest deleting recipes")
    test_delete_recipe()

    # List all recipes
    print("=" * 100, "\nTest listing all recipes")
    test_get_all_recipes()

    # List all recipes names
    print("=" * 100, "\nTest listing all recipes names")
    test_get_all_recipes_names()
