import asyncio

from moonshot.api import (
    api_create_session,
    api_delete_context_strategy,
    api_delete_session,
    api_get_all_context_strategy_names,
    api_get_all_prompt_template_details,
    api_get_all_prompt_template_names,
    api_get_all_session_details,
    api_get_all_session_names,
    api_get_session_chats_by_session_id,
    api_send_prompt,
    api_update_context_strategy,
    api_update_prompt_template,
)
from moonshot.src.redteaming.session.session import Session


def test_create_session():
    return api_create_session(
        "my_session_1",
        "my session desc",
        ["my-openai-gpt35"],
        "add_previous_prompt",
        "legal-term-template",
    )


def test_get_all_session_names():
    print(api_get_all_session_names())


def test_api_get_session_chats_by_session_id(session_id):
    for chat in api_get_session_chats_by_session_id(session_id):
        print(chat, "\n")


def test_api_get_all_session_details():
    for session_detail in api_get_all_session_details():
        print(session_detail, "\n")


async def test_send_prompt(session_id, prompt):
    await api_send_prompt(session_id, prompt)


def test_api_delete_session(session_id):
    api_delete_session(session_id)


def test_api_get_all_prompt_template_details():
    return api_get_all_prompt_template_details()


def test_api_get_all_context_strategy_names():
    print(api_get_all_context_strategy_names())


def test_api_delete_context_strategy(context_strategy_name):
    api_delete_context_strategy(context_strategy_name)


def test_api_update_context_strategy(session_id, context_strategy):
    api_update_context_strategy(session_id, context_strategy)


def test_api_update_prompt_template(session_id, prompt_template):
    api_update_prompt_template(session_id, prompt_template)


def test_api_get_all_prompt_template_names():
    for prompt_template_name in api_get_all_prompt_template_names():
        print(prompt_template_name)


def test_get_all_prompt_template_details():
    for prompt_template_details in api_get_all_prompt_template_details():
        print(prompt_template_details)


async def main():
    # Uncomment all to run all tests together. To run individual test, run that set of codes with no newline

    # ------------------------------------------------------------------------------
    # Session endpoints APIs Test
    # ------------------------------------------------------------------------------

    # Get all session names
    test_get_all_session_names()

    # Get all session details
    test_api_get_all_session_details()

    # # Create session, send prompt and create chat in DB
    created_session = test_create_session()
    await test_send_prompt(created_session.metadata.session_id, "chewing gum")

    # Get session chats (only session chats) by id
    session_id = "my-test-session"
    test_api_get_session_chats_by_session_id(session_id)

    # Delete session
    # TODO by tester: enter name of SAMPLE session to be deleted
    test_api_delete_session("")

    # ------------------------------------------------------------------------------
    # Context Strategy endpoints APIs Test
    # ------------------------------------------------------------------------------

    # Get all context strategy names
    test_api_get_all_context_strategy_names()

    # Delete context strategy
    # TODO by tester: enter name of SAMPLE context strategy to be deleted
    context_strategy_name = ""
    test_api_delete_context_strategy(context_strategy_name)

    # ------------------------------------------------------------------------------
    # Prompt Template endpoints APIs Test
    # ------------------------------------------------------------------------------

    # List prompt template names
    test_api_get_all_prompt_template_names()

    # List prompt template details
    test_get_all_prompt_template_details()

    # ------------------------------------------------------------------------------
    # Update prompt template and context strategy
    # ------------------------------------------------------------------------------

    # Create session for subsequent context strategy and prompt template tests
    created_session_for_pt_cs = test_create_session()
    # Update prompt template and context strategy
    context_strategy_name = "sample_context_strat"
    test_api_update_context_strategy(
        created_session_for_pt_cs.metadata.session_id, context_strategy_name
    )
    # # Update prompt template
    prompt_template_name = "sample_prompt_template"
    test_api_update_prompt_template(
        created_session_for_pt_cs.metadata.session_id, prompt_template_name
    )
    updated_session = Session(session_id=created_session_for_pt_cs.metadata.session_id)
    print(f"Updated context strategy:{updated_session.metadata.context_strategy}")
    print(f"Updated prompt template:{updated_session.metadata.prompt_template}")


if __name__ == "__main__":
    asyncio.run(main())
