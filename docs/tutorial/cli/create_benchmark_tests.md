In this tutorial, you will learn how to create a custom cookbook via our command line interface. A cookbook is a collection of one or more tests (or recipes). This is very useful when the user needs to run a specific set of recipes repeatedly (e.g., running different set of bias benchmarks on the same endpoint before and after safety fine-tuning) or if the user wants to test a RAG application.

1. Change directory to the root directory of Moonshot.

2. Enter the following command to enter the CLI interactive mode:
    
        python -m moonshot cli interactive

3. Choose a benchmark type to create and view help:
    - Recipe 

        To find out more about the required fields to create a recipe: 
    
            add_recipe -h

        !!! important
            If you are running the recipe on a RAG application, please ensure you name your recipe's tag as "rag":

                -t "['rag']"

            For effective evaluation of your RAG application, do ensure you are using your own custom test dataset. You can view more information on how to add your custom test dataset [here](../../user_guide/cli/add_your_own_tests.md).

        Here is an example of the command to create a cookbook:
                
            add_recipe 'My new recipe' 'I am recipe description' "['category1','category2']" "['bbq-lite-age-ambiguous']" "['bertscore','bleuscore']" -p "['analogical-similarity','mmlu']" -t "['tag1','tag2']" -g "{'A':[80,100],'B':[60,79],'C':[40,59],'D':[20,39],'E':[0,19]}" 

    - Cookbook

        To find out more about the required fields to create a cookbook: 

            add_cookbook -h

        !!! important
            If you are running the cookbook on a RAG application, please ensure you name your cookbook's tag as "rag":

                -t "['rag']"

            For effective evaluation of your RAG application, do ensure you are using your own custom test dataset. You can view more information on how to add your custom test dataset [here](../../user_guide/cli/add_your_own_tests.md).

         Here is an example of the command to create a cookbook:

            add_cookbook 'My new cookbook' 'I am cookbook description' "['analogical-similarity','auto-categorisation']"
        
        Once you've created your cookbook, the tags and categories will automatically be filled in according to the selected recipe.

4. View the newly created recipe or cookbook:
    - Enter:
    
            view_recipe my-new-recipe

        ![new recipe](images/new_recipe.png)

    - Enter:

            view_cookbook my-new-cookbook

        ![new cookbook](images/new_cookbook.png)

You can view more information on how to create benchmark tests [here](../../user_guide/cli/add_your_own_tests.md).