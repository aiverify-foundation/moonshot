def transform_web_format(
    original_dict: dict[str, dict[str, list[dict[str, dict[str, float]]]]]
) -> dict[str, dict[str, list[dict[str, list[dict[str, list[dict[str, float]]]]]]]]:
    transformed = {"metadata": original_dict["metadata"], "results": {"cookbooks": []}}

    for cookbook_name, cookbook_data in original_dict.items():
        if cookbook_name == "metadata":
            continue  # Skip the metadata entry

        cookbook_entry = {"id": cookbook_name, "recipes": []}
        for recipe_name, recipe_data in cookbook_data.items():
            recipe_entry = {"id": recipe_name, "models": []}

            for model_data_str, model_data in recipe_data.items():
                # Extract model, recipe, dataset, prompt_template from the string
                model, _, dataset, prompt_template = eval(model_data_str)

                model_entry = {
                    "id": model,
                    "datasets": [
                        {
                            "id": dataset,
                            "prompt_templates": [
                                {
                                    "id": prompt_template,
                                    "metrics": model_data["results"],
                                }
                            ],
                        }
                    ],
                }

                # Check if the model already exists in the recipe_entry
                existing_model = next(
                    (m for m in recipe_entry["models"] if m["id"] == model), None
                )
                if existing_model:
                    # Check if the dataset already exists in the model
                    existing_dataset = next(
                        (d for d in existing_model["datasets"] if d["id"] == dataset),
                        None,
                    )
                    if existing_dataset:
                        existing_dataset["prompt_templates"].append(
                            model_entry["datasets"][0]["prompt_templates"][0]
                        )
                    else:
                        existing_model["datasets"].append(model_entry["datasets"][0])
                else:
                    recipe_entry["models"].append(model_entry)

            cookbook_entry["recipes"].append(recipe_entry)

        transformed["results"]["cookbooks"].append(cookbook_entry)

    return transformed
