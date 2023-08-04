def generate_file(input_string):
    pre_string = "This is the start of generate_file: "
    post_string = " :This is the end of generate_file"
    return pre_string + input_string + post_string

def generate_text(input_string):
    pre_string = "This is the start of generate_text: "
    post_string = " :This is the end of generate_text"
    return pre_string + input_string + post_string

def remove_sensitive_info(input_string):
    pre_string = "This is the start of remove_sensitive_info: "
    post_string = " :This is the end of remove_sensitive_info"
    return pre_string + input_string + post_string

def analyse_projet(input_string):
    pre_string = "This is the start of analyse_projet: "
    post_string = " :This is the end of analyse_projet"
    return pre_string + input_string + post_string

def main():
    functions = {name: obj for name, obj in globals().items() if callable(obj) and name != "main"}

    while True:
        print("\nChoose a method to execute:")
        for i, func in enumerate(functions, start=1):
            print(f"{i}. {func}")
        print(f"{i+1}. Quit")

        choice = input("\nEnter your choice (1-{}): ".format(i+1))
        if choice == str(i+1):
            print("Exiting the program.")
            break

        input_string = input("\nEnter your input string: ")

        if choice.isdigit() and 1 <= int(choice) <= i:
            output = list(functions.values())[int(choice)-1](input_string)
            print("\nOutput: ", output)
            with open("output.txt", "a") as file:
                file.write(output + "\n")
        else:
            print("Invalid choice. Please choose a number between 1 and {}.".format(i+1))

if __name__ == "__main__":
    main()
