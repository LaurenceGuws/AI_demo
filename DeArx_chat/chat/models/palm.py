import google.generativeai as palm

def interact(messages):
    # Configuration for PALM (Google GenerativeAI)
    palm.configure(api_key="AIzaSyCHebgU21R_Wy2IjqCFvGIbNZXJiIKstwU")

    defaults = {
        'model': 'models/chat-bison-001',
        'temperature': 0.25,
        'candidate_count': 1,
        'top_k': 40,
        'top_p': 0.95,
    }
    context = ""

    # Formatting the messages for PALM as a conversation list
    conversation_messages = []
    for message in messages:
        conversation_messages.append(message["role"] + ": " + message["content"])
    
    conversation_messages.append("NEXT REQUEST")

    response = palm.chat(
        **defaults,
        context=context,
        examples=[], # You can include any examples here as needed
        messages=conversation_messages
    )
    
    # Extracting the response of the AI to your most recent request and casting it to string
    response_content = str(response.last)

    # Formatting the response to match the existing method's output
    return response_content  # Now returns a string directly


def main():
    print("Welcome to the interactive chat! Type 'exit' to quit.")

    user_messages = []

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        user_messages.append({"role": "user", "content": user_input})

        response = interact(user_messages)

        print("Assistant:", response)

if __name__ == "__main__":
    main()

