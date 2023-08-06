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

    # ... [rest of your existing code]
