# Running Moonshot via CLI

Two modes are available on the Moonshot CLI: Command-Based Mode and Interactive Mode.

<details open>

<summary>Full list of commands in Moonshot</summary>

``` bash
Initialisation
======================================================================================================
interactive           Run the interactive shell.                                                      
list_connect_types    Get a list of available Language Model (LLM) connection types.                  
list_endpoints        Get a list of available Language Model (LLM) endpoints.                         
version               Get the version of the application.                                             

Moonshot Benchmarking
======================================================================================================
add_cookbook          Add a new cookbook.                                                             
add_endpoint          Add a new endpoint.                                                             
add_recipe            Add a new recipe.                                                               
list_cookbooks        Get a list of available cookbooks.                                              
list_recipes          Get a list of available recipes.                                                
list_results          Get a list of available results.                                                
list_runs             Get a list of available runs.                                                   
resume_run            Resume an interrupted run.                                                      
run_cookbook          Run a cookbook.                                                                 
run_recipe            Run a recipe.                                                                   
view_cookbook         View a cookbook.                                                                
view_results          View a results file.                                                            

Moonshot RedTeaming
=======================================================================================================
end_session            End the current session.                                                        
list_prompt_templates  List all prompt templates available.                                            
list_sessions          List all available sessions.                                                    
new_session            Add a new red teaming session.                                                  
use_context_strategy   Use a context strategy.                                                         
use_prompt_template    Use a prompt template.                                                          
use_session            Use an existing red teaming session.                                            

Uncategorized
======================================================================================================
alias                 Manage aliases                                                                  
edit                  Run a text editor and optionally open a file with it                            
help                  List available commands or provide detailed help for a specific command         
history               View, run, edit, save, or clear previously entered commands                     
macro                 Manage macros                                                                   
quit                  Exit this application                                                           
run_pyscript          Run a Python script file inside the console                                     
run_script            Run commands in script file that is encoded as either ASCII or UTF-8 text       
set                   Set a settable parameter or show current settings of parameters                 
shell                 Execute a command as if at the OS prompt                                        
shortcuts             List available shortcuts                                                
```
</details>

## Command-based Mode

In the command-based mode, run commands by prepending `python -m moonshot cli`. 

For example,

- To list all the available commands: `python -m moonshot cli help`
- To list the connector types available: `python -m moonshot cli list_connect_types`

## Interactive Mode

We recommend the interactive mode for a more efficient experience, especially if you are using Moonshot to red-team. 

To enter interactive mode: `python -m moonshot cli interactive` (You should see the command prompt change to `moonshot >` ) For example,
- To list all the available commands: 
    ```
    moonshot > help
    ```
- To list the connector types available:
    ```
    moonshot > list_connect_types
    ```
