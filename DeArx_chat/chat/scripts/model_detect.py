import os
import importlib.util

def load_module(module_path):
    spec = importlib.util.spec_from_file_location("model_module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_models():
    # Directory where the models are stored
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')

    passed_test = []
    failed_test = []

    # Iterate over all files in the models directory
    for filename in os.listdir(models_dir):
        # Construct the full file path
        file_path = os.path.join(models_dir, filename)

        # Skip directories and non-.py files
        if os.path.isdir(file_path) or not filename.endswith('.py') or filename == '__init__.py':
            continue

        # Attempt to import the file as a module
        try:
            module = load_module(file_path)
        except Exception as e:
            print(f"Error loading module '{filename}': {e}")
            failed_test.append(filename.replace('.py', ''))
            continue

        # Attempt to call the required method with a test prompt
        try:
            messages_for_gpt = [{'role': 'user', 'content': 'test prompt'}]
            response = module.interact(messages_for_gpt)  
            assert isinstance(response, str), "Response is not a string"
            print(f"Module '{filename}' passed the test.")
            passed_test.append(filename.replace('.py', ''))
        except Exception as e:
            print(f"Error testing module '{filename}': {e}")
            print(f"'{filename}': Undeploying")
            failed_test.append(filename.replace('.py', ''))

    return passed_test, failed_test

if __name__ == "__main__":
    passed_test, failed_test = test_models()
    print("Models that passed the test:", passed_test)
    print("Models that failed the test:", failed_test)
