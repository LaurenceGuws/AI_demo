import os
import importlib.util

def load_module(module_path):
    spec = importlib.util.spec_from_file_location("model_module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_models():
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    passed_test = []
    failed_test = []

    for filename in os.listdir(models_dir):
        file_path = os.path.join(models_dir, filename)
        if os.path.isdir(file_path) or not filename.endswith('.py') or filename == '__init__.py':
            continue
        try:
            module = load_module(file_path)
        except Exception as e:
            print(f"Error loading module '{filename}': {e}")
            failed_test.append(filename)
            continue
        try:
            test_input = [{'role': 'user', 'content': 'test message'}]
            response = module.interact(test_input)
            assert isinstance(response, str), "Response is not a string"
            passed_test.append(filename)
        except Exception as e:
            print(f"Error testing module '{filename}': {e}")
            failed_test.append(filename)
    return passed_test, failed_test

if __name__ == "__main__":
    passed_test, failed_test = test_models()
    print("Models that passed the test:", passed_test)
    print("Models that failed the test:", failed_test)