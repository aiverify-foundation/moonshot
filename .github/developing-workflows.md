This branch is used to develop GHA workflows before commiting to the main
branch, to avoid creating unwanted commit records to the main branch.

Workflows created in a non-main branch can be only be run via CLI as follows:

gh workflow run <workflow-name> --ref <branch-name> -f <parameter-name>=<parameter-value>

For example,  gh workflow run 'License File Generation' --ref ci-workflow-dev -f repo=aiverify-foundation/moonshot -f branch=ci-workflow-dev

Before you can run the workflow via CLI, it must first appear in the
workflow list as follows:

gh workflow list

If it is not in the list, you have to trigger it once by creating a trigger
for push in your workflow and pushing a commit to the branch.

on:
    push:
        branches: [ 'ci-workflow-dev' ]

