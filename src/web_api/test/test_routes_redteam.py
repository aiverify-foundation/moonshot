from fastapi.testclient import TestClient
from unittest.mock import patch
from web_api.schemas.session_create_dto import SessionCreateDTO
from web_api.app import init_api
from web_api.schemas.session_response_model import SessionMetadataModel

app = init_api()

@patch('web_api.services.session_service.create_session')
def test_create_session(mock_create_session):
    mock_create_session.return_value = SessionMetadataModel(
        session_id="id_1",
        name="Test Session",
        description="This is a test session",
        created_epoch=123456789,
        created_datetime="2021-01-01T00:00:00",
        endpoints=["mock_endpoint_1"],
        metadata_file="mock_metadata_file",
        prompt_template="mock_prompt_template",
        context_strategy=0,
        chats=["mock_chat_1", "mock_chat_2"],
        filename="mock_filename",
        chat_history=None
    )

    with TestClient(app) as client:
        response = client.post("/v1/sessions", json={
            "name": "Test Session",
            "description": "This is a test session",
            "endpoints": ["mock_endpoint_1"]
        })
    print(response.json())
    sessionData = response.json()["session"]
    assert response.status_code == 200
    assert sessionData["session_id"] == "id_1"
    assert sessionData["name"] == "Test Session"
    assert sessionData["description"] == "This is a test session"
    assert sessionData["created_epoch"] == 123456789
    assert sessionData["created_datetime"] == "2021-01-01T00:00:00"
    assert sessionData["metadata_file"] == "mock_metadata_file"
    assert sessionData["prompt_template"] == "mock_prompt_template"
    assert sessionData["context_strategy"] == 0
    assert sessionData["chats"] == ["mock_chat_1", "mock_chat_2"]
    assert sessionData["filename"] == "mock_filename"
    assert sessionData["chat_history"] is None
    assert sessionData["endpoints"] == ["mock_endpoint_1"]

    mock_create_session.assert_called_once()
    mock_create_session.assert_called_with(
        SessionCreateDTO(name='Test Session', description='This is a test session', endpoints=['mock_endpoint_1'])
    )

    @patch('web_api.services.session_service.get_session')
    def test_get_session(mock_get_session):
        mock_get_session.return_value = SessionMetadataModel(
            session_id="id_2",
            name="Retrieved Session",
            description="This is a retrieved session",
            created_epoch=987654321,
            created_datetime="2021-02-01T00:00:00",
            endpoints=["mock_endpoint_2"],
            metadata_file="mock_metadata_file_retrieved",
            prompt_template="mock_prompt_template_retrieved",
            context_strategy=1,
            chats=["mock_chat_3", "mock_chat_4"],
            filename="mock_filename_retrieved",
            chat_history={"mock_chat_3": ["message_1", "message_2"]}
        )

        with TestClient(app) as client:
            response = client.get("/v1/sessions/id_2")
        print(response.json())
        sessionData = response.json()["session"]
        assert response.status_code == 200
        assert sessionData["session_id"] == "id_2"
        assert sessionData["name"] == "Retrieved Session"
        assert sessionData["description"] == "This is a retrieved session"
        assert sessionData["created_epoch"] == 987654321
        assert sessionData["created_datetime"] == "2021-02-01T00:00:00"
        assert sessionData["metadata_file"] == "mock_metadata_file_retrieved"
        assert sessionData["prompt_template"] == "mock_prompt_template_retrieved"
        assert sessionData["context_strategy"] == 1
        assert sessionData["chats"] == ["mock_chat_3", "mock_chat_4"]
        assert sessionData["filename"] == "mock_filename_retrieved"
        assert sessionData["chat_history"] == {"mock_chat_3": ["message_1", "message_2"]}
        assert sessionData["endpoints"] == ["mock_endpoint_2"]

        mock_get_session.assert_called_once()
        mock_get_session.assert_called_with("id_2")

    @patch('web_api.services.session_service.update_session')
    def test_update_session(mock_update_session):
        mock_update_session.return_value = SessionMetadataModel(
            session_id="id_3",
            name="Updated Session",
            description="This is an updated session",
            created_epoch=123987654,
            created_datetime="2021-03-01T00:00:00",
            endpoints=["mock_endpoint_3"],
            metadata_file="mock_metadata_file_updated",
            prompt_template="mock_prompt_template_updated",
            context_strategy=2,
            chats=["mock_chat_5", "mock_chat_6"],
            filename="mock_filename_updated",
            chat_history={"mock_chat_5": ["message_3", "message_4"]}
        )

        with TestClient(app) as client:
            response = client.put("/v1/sessions/id_3", json={
                "name": "Updated Session",
                "description": "This is an updated session",
                "endpoints": ["mock_endpoint_3"]
            })
        print(response.json())
        sessionData = response.json()["session"]
        assert response.status_code == 200
        assert sessionData["session_id"] == "id_3"
        assert sessionData["name"] == "Updated Session"
        assert sessionData["description"] == "This is an updated session"
        assert sessionData["created_epoch"] == 123987654
        assert sessionData["created_datetime"] == "2021-03-01T00:00:00"
        assert sessionData["metadata_file"] == "mock_metadata_file_updated"
        assert sessionData["prompt_template"] == "mock_prompt_template_updated"
        assert sessionData["context_strategy"] == 2
        assert sessionData["chats"] == ["mock_chat_5", "mock_chat_6"]
        assert sessionData["filename"] == "mock_filename_updated"
        assert sessionData["chat_history"] == {"mock_chat_5": ["message_3", "message_4"]}
        assert sessionData["endpoints"] == ["mock_endpoint_3"]

        mock_update_session.assert_called_once()
        mock_update_session.assert_called_with(
            "id_3",
            SessionCreateDTO(name='Updated Session', description='This is an updated session', endpoints=['mock_endpoint_3'])
        )

    @patch('web_api.services.session_service.delete_session')
    def test_delete_session(mock_delete_session):
        mock_delete_session.return_value = {"message": "Session deleted successfully"}

        with TestClient(app) as client:
            response = client.delete("/v1/sessions/id_4")
        print(response.json())
        assert response.status_code == 200
        assert response.json() == {"message": "Session deleted successfully"}

        mock_delete_session.assert_called_once()
        mock_delete_session.assert_called_with("id_4")


