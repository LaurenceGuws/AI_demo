import os
import openai
import base64


def interact(messages):
    openai_key = base64.b64decode(os.getenv('OPENAI_API_KEY')).decode()
    # openai_key = base64.b64decode("c2stTnRWMDRnbWpkcE8wVW9LZGJSYlpUM0JsYmtGSkdyTWVQOVpsU3FtSVdDRkFhajVx").decode()
    openai.api_key = openai_key

    # Call the GPT model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        messages=messages
    )

    # Return the assistant's response
    return response['choices'][0]['message']['content']
