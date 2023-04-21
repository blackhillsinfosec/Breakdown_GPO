import sys

def help():
    print("\nBreakdown GPO\n")
    column_print(f"Usage: python3 {sys.argv[0]} -i <input> -o <output>", "")
    print("")
    column_print("Options:", "")
    print("")
    column_print("--input, -i, --in", "Define the GPOReport to be broken down.")
    column_print("--output, -o, --out", "Define the output directory.")
    column_print("--default_output, -do, --do", "Use the current working directory as the output directory.")
    column_print("--help, -h, no arguments", "Print this help menu.")
    print("")
    quit()

# This logic does not account for overflowing text.
def column_print(col1, col2):
    col1_width = 30
    col2_width = 50
    col1_text = f"\t{col1}{' ' * (col1_width - len(col1))}"
    col2_text = f"\t{col2}{' ' * (col2_width - len(col2))}"
    print(col1_text+col2_text)