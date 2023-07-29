import openai
import base64

class Chat:
    
    def chat_gpt_interact(messages):
        import configparser
        config = configparser.ConfigParser()
        config.read('conf\config.conf')
        openai_api_key = base64.b64decode(config['OpenAI']['API_KEY']).decode()
        messages_dicts = []
        openai.api_key = openai_api_key
        # print(openai.Model.list())
        for i, message in enumerate(messages):
            if i % 2 == 0:
                messages_dicts.append({"role": "system", "content": message})
            else:
                messages_dicts.append({"role": "user", "content": message})

        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=messages_dicts
        )
        return response['choices'][0]['message']['content']
