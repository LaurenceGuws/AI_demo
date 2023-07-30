import os
import openai
import base64
import configparser

class Chat:
    @staticmethod
    def chat_gpt_interact(messages):
        # Read the API key from the config file and decode it
        config = configparser.ConfigParser()
        config.read('conf\config.conf')
        openai_key = os.getenv('OPENAI_API_KEY')
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
