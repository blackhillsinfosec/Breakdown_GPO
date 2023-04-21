import os

def parse(args):
    input_path=""
    output_path=""

    for indx, arg in enumerate(args):
        if arg.lower() in ["--intput", "-i", "--in"]:
            if len(args) > (indx + 1):
                input_path = args[indx+1]
        if arg.lower() in ["--output", "-o", "--out"]:
            if len(args) > (indx + 1):
                output_path = args[indx+1]
        elif arg.lower() in ["--default_output", "--do", "-do"]:
            output_path = os.getcwd()

    if (not (os.path.exists(input_path))) or (not (os.access(input_path, os.R_OK))):
        if (not (os.path.exists(input_path))):
            print(f"The file '{input_path}' could not be found.")
        elif (not (os.access(input_path, os.R_OK))):
            print(f"You do not have permissions to read '{input_path}'.")
        while (not (os.path.exists(input_path))):
            input_path = input("What is the input file path? ")
            if (not (os.path.exists(input_path))):
                print(f"The file '{input_path}' could not be found.")
            elif (not (os.access(input_path, os.R_OK))):
                print(f"You do not have permissions to read '{input_path}'.")

    if (not (os.path.exists(output_path))) or (os.path.isfile(output_path)) or (not (os.access(output_path, os.W_OK))) or os.path.exists(os.path.join(output_path, "breakdown_gpo")):
        if (os.path.isfile(output_path)):
            print(f"The output directory cannot be a file path.")
        elif (not (os.path.exists(output_path))):
            print(f"The directory '{output_path}' could not be found.")
        elif (not (os.access(output_path, os.W_OK))):
            print(f"You do not have permissions to write to the path '{output_path}'.")
        elif os.path.exists(os.path.join(output_path, "breakdown_gpo")):
            print(f"Cannot use '{output_path}' because the needed write locations already exist!")
        while ((not (os.path.exists(output_path))) or (os.path.isfile(output_path))) or (not (os.access(output_path, os.W_OK))) or os.path.exists(os.path.join(output_path, "breakdown_gpo")):
            output_path = input("What is the path to the output directory? ")
            if (os.path.isfile(output_path)):
                print(f"The output directory cannot be a file path.")
            elif (not (os.path.exists(output_path))):
                print(f"The directory '{output_path}' could not be found.")
            elif (not (os.access(output_path, os.W_OK))):
                print(f"You do not have permissions to write to the path '{output_path}'.")
            elif os.path.exists(os.path.join(output_path, "breakdown_gpo")):
                print(f"Cannot use '{output_path}' because the needed write locations already exist!")

    return input_path, os.path.join(output_path,"breakdown_gpo")