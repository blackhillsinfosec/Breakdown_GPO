#! /bin/python3
# Version 2.0.0
import time, sys, os, time, modules.gpo_files as gpo_files, modules.gpo_threading as gpo_threading
from colorama import Fore, Style

def main():
    cwd=os.getcwd()
    # Memory-related processes. Keyboard Interupt shouldn't be a problem.
    try:
        start = time.time()
        filecontent=gpo_files.initialize_filecontent()
        Indexes = gpo_threading.concurrent_index_file(filecontent)
        Indexes.print_index_counts()
        validate=Indexes.validate_indexes()
        gpo_threading.review_validation(validate, start)
        output_dir=gpo_files.create_output_dirs(cwd)
        
    # Cleanly exit the program if interupt is found.
    except KeyboardInterrupt:
        print("\r\n", end="")
        sys.exit()
    try:
        gpo_files.create_summary_file(cwd, output_dir, filecontent, Indexes)
        gpo_files.create_gpo_files(cwd, output_dir, filecontent, Indexes)
        print(Style.BRIGHT+Fore.GREEN+"Export complete."+Style.RESET_ALL)
    except KeyboardInterrupt:
        print("\rExport was interupted. The files are corrupt and not complete.")
        sys.exit

if __name__=='__main__':
    main()
