# Moonshot Sessions API Endpoints

<details>
<summary> [GET] /v1/sessions</summary>
This endpoint is use to get all sessions.
<br/>
<b> Parameters (body)</b> : None
<br/>
<b>Success Response: </b>
```json
[
    {
        "session_id": "testsession1_20240315-043147",
        "name": "TestSession1",
        "description": "Test 1",
        "created_epoch": 1710448307.051328,
        "created_datetime": "20240315-043147",
        "chat_ids": [
            "openaigpt35turbotest1_20240315_043147",
            "openaigpt4test1_20240315_043147"
        ],
        "endpoints": [
            "openaigpt35turbotest1",
            "openaigpt4test1"
        ],
        "prompt_template": null,
        "context_strategy": null,
        "filename": null,
        "chat_history": null
    }
]
```
</details>


<details>
    <summary> [GET] /v1/sessions/{session_id}?include_history={boolean} </summary>
This endpoint is use to session details by ID.
<br/>
<b> Parameters (path)</b>:
<br/> <code>session_id</code>: The ID of the session to retrieve.
<br/> <code>include_history</code>: A boolean to determine if you want to retrieve the history
<br/>
<b>Example</b> : <code>/v1/sessions/testsession1_20240315-043147?include_history=true</code>
<br/>
<b>Success Response: </b>
```json
{
    "session": {
        "session_id": "testsession1_20240315-043147",
        "name": "TestSession1",
        "description": "Test 1",
        "created_epoch": 1710448307.051328,
        "created_datetime": "20240315-043147",
        "chat_ids": [
            "openaigpt35turbotest1_20240315_043147",
            "openaigpt4test1_20240315_043147"
        ],
        "endpoints": [
            "openaigpt35turbotest1",
            "openaigpt4test1"
        ],
        "prompt_template": null,
        "context_strategy": null,
        "filename": null,
        "chat_history": {
            "openaigpt35turbotest1_20240315_043147": [],
            "openaigpt4test1_20240315_043147": []
        }
    }
}
```
</details>

<details>
<summary>[POST] /v1/sessions</summary>
This endpoint is use to create new session.
<br/>
<b> Parameters (body)</b>
```json
{
    "name": "string",
    "description": "string",
    "endpoints": ["string"]
}
``` 
<b>Example</b> 
<br/>
```json
{
    "name": "TestSession1",
    "description": "Test 1",
    "endpoints": ["openaigpt35turbotest1", "openaigpt4test1"]
}
```
<b>Success Response: </b>
```json
{
    "session": {
        "session_id": "testsession1_20240315-043147",
        "name": "TestSession1",
        "description": "Test 1",
        "created_epoch": 1710448307.051328,
        "created_datetime": "20240315-043147",
        "chat_ids": [
            "openaigpt35turbotest1_20240315_043147",
            "openaigpt4test1_20240315_043147"
        ],
        "endpoints": [
            "openaigpt35turbotest1",
            "openaigpt4test1"
        ],
        "prompt_template": null,
        "context_strategy": null,
        "filename": null,
        "chat_history": null
    }
}
```
</details>


<details>
<summary>[POST] /v1/sessions/{session_id}/prompt</summary>
This endpoint is use to send prompts in the session.
<br/>
<b> Parameters (path)</b>:
<br/> <code>session_id</code>: The ID of the session to retrieve.
<br/>
<b> Parameters (body)</b>
```json
{
    "prompt": "string"
}
``` 
<b>Example</b> 
<br/>
<code>/v1/sessions/testsession1_20240315-044154/prompt</code>
<br/>
```json
{
    "prompt": "Hello World"
}
```
<b>Success Response: </b>
```json
{
    "openaigpt35turbotest1_20240315_044154": [
        {
            "chat_record_id": 1,
            "conn_id": "conn_id_123",
            "context_strategy": "",
            "prompt_template": "",
            "prompt": "hello world",
            "prepared_prompt": "hello world",
            "predicted_result": "predicted results",
            "duration": "2 secs",
            "prompt_time": "03/15/2024, 04:42:02"
        }
    ],
    "openaigpt4test1_20240315_044154": [
        {
            "chat_record_id": 1,
            "conn_id": "conn_id_123",
            "context_strategy": "",
            "prompt_template": "",
            "prompt": "hello world",
            "prepared_prompt": "hello world",
            "predicted_result": "predicted results",
            "duration": "2 secs",
            "prompt_time": "03/15/2024, 04:42:02"
        }
    ]
}
```
</details>