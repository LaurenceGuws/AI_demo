import vertexai
from vertexai.preview.language_models import ChatModel, InputOutputTextPair

def bard_interact(messages):
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
