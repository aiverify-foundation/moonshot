from moonshot.api import api_create_datasets, api_set_environment_variables
from dotenv import dotenv_values

api_set_environment_variables(dotenv_values(".env"))

file_path = "/Users/normanchia/LocalDocs/Moonshot/your_dataset.csv"
create_dataset_args = {
    "csv_file_path": file_path,
    "dataset_name": "cais/mmlu",
    "dataset_config": "college_biology",
    "split": "test",
    "input_col": ["question","choices"],
    "target_col": "answer"
}
print(api_create_datasets("Norman Dataset 2","Dataset convert from csv","www.reference.com","NORMAN LICENSE", "csv" , **create_dataset_args))