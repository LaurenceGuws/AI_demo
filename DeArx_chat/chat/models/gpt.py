import os
import openai
import base64

class Chat:
    @staticmethod
    def chat_gpt_interact(messages):
        openai_key = base64.b64decode(os.getenv('OPENAI_API_KEY')).decode()
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
