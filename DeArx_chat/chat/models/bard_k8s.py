import os
import base64
import json
import vertexai
from vertexai.preview.language_models import ChatModel, InputOutputTextPair

def get_service_account_key_from_env():
    """
    Decodes the service account key from the environment variable and returns it as a dictionary.
    """
    encoded_key = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON_BASE64", "")
    decoded_key = base64.b64decode(encoded_key).decode('utf-8')
    return json.loads(decoded_key)

def setup_google_auth():
    """
    Sets up the environment for Google Cloud authentication using the service account key from the environment variable.
    """
    service_account_info = get_service_account_key_from_env()
    temp_path = "/tmp/service_account.json"
    
    with open(temp_path, "w") as file:
        json.dump(service_account_info, file)
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_path

def interact(messages):
    setup_google_auth()  # Set up authentication at the beginning of the function
    project_id='palm-386622'
    model_name='chat-bison@001'
    temperature=0.5
    max_output_tokens=256
    top_p=0.9
    top_k=40
    location = "us-central1"
    """Predict using a Large Language Model."""
    vertexai.init(project=project_id, location=location)

    chat_model = ChatModel.from_pretrained(model_name)
    parameters = {
      "temperature": temperature,
      "max_output_tokens": max_output_tokens,
      "top_p": top_p,
      "top_k": top_k,
    }

    chat = chat_model.start_chat(
      examples=[]
    )

    # Find the last user message
    request_text = None
    for message in reversed(messages):
        if message['role'] == 'user':
            request_text = message['content']
            break

    if request_text is None:
        return 'No user message found'

    response = chat.send_message(request_text, **parameters)
    return response.text
