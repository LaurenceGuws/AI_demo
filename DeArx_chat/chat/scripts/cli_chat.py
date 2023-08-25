import os
import importlib.util

def load_module(module_path):
    spec = importlib.util.spec_from_file_location("model_module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    # Directory where the models are stored
    models_dir = "models"

    # Store the list of modules and their corresponding callable functions
    module_functions = {}

    # Iterate over all files in the models directory
    for filename in os.listdir(models_dir):
        # Construct the full file path
        file_path = os.path.join(models_dir, filename)

        # Skip directories, non-.py files, and __init__.py files
        if os.path.isdir(file_path) or not filename.endswith('.py') or filename == '__init__.py':
            continue

        # Attempt to import the file as a module
        try:
            module = load_module(file_path)
        except Exception as e:
            print(f"Error loading module '{filename}': {e}")
            continue

        # Extract the callable functions from the module
        functions = {name: obj for name, obj in module.__dict__.items() if callable(obj)}
        module_functions[filename[:-3]] = functions  # Store the functions for this module

    while True:
        print("\nChoose a module to interact with:")
        for i, mod in enumerate(module_functions, start=1):
            print(f"{i}. {mod}")
        print(f"{i+1}. Quit")

        choice = input("\nEnter your choice (1-{}): ".format(i+1))
        if choice == str(i+1):
            print("Exiting the program.")
            return

        if choice.isdigit() and 1 <= int(choice) <= i:
            chosen_module = list(module_functions.keys())[int(choice)-1]
            functions = module_functions[chosen_module]
        else:
            print("Invalid choice. Please choose a number between 1 and {}.".format(i+1))
            continue

        if "interact" in functions:
            conversation = []  # Initialize the conversation list
            while True:
                input_string = input("\nEnter your input string (or 'quit' to select another module): ")
                if input_string.lower() == 'quit':
                    break
                
                conversation.append({'role': 'user', 'content': input_string})  # Add the user's message to the conversation
                
                try:
                    output_string = functions['interact'](conversation)
                    print("\nOutput: ", output_string)

                    conversation.append({'role': 'assistant', 'content': output_string})  # Add the assistant's message to the conversation
                except Exception as e:
                    print(f"Error executing function 'interact' in module '{chosen_module}': {e}")
        else:
            print(f"No 'interact' method found in module '{chosen_module}'.")

if __name__ == "__main__":
    main()
