Developing GitHub Workflows
===========================
These instructions are used to develop Github workflows in a non-main branch 
instead of in the main branch to avoid creating unwanted commit records to
the main branch.

Workflows created in a non-main branch can be only be run via CLI as follows:

`gh workflow run <workflow-name> --ref <branch-name> -f <parameter-name>=<parameter-value>`

For example, to run a workflow called License File Generation:

`gh workflow run 'License File Generation' --ref ci-workflow-dev -f repo=aiverify-foundation/moonshot -f branch=ci-workflow-dev`

Before you can run the workflow via CLI, it must first appear in the workflow
list when you run the following command:

`gh workflow list`

If it is not in the list, you have to trigger it once, this can be done by
creating a trigger for push in your workflow as follows and pushing a commit
to the branch. Once the workflow appears in the workflow list, you can remove
the trigger for push from your workflow.

    on:  
        push:  
            branches: [ "ci-workflow-dev" ]  

