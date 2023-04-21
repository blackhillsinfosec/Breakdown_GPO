#! /bin/python3
# Version 3.0.0

import sys, time, shutil, os
from modules.breakdown import breakdown
from modules.arguments import parse
from modules.help import help

def main():
    try:
        if len(sys.argv)==1 or "--help" in sys.argv or "-h" in sys.argv:
            help()
        else:
            input_path, output_path = parse(sys.argv[1:])
    except KeyboardInterrupt:
        pass
    try:
        start_time = time.time()
        breakdown(input_path, output_path)
        print(f"Breakdown took {time.time() - start_time :.2f} seconds.")
    except KeyboardInterrupt:
        if(os.path.exists(output_path)):
            print("Interupt detected.")
            shutil.rmtree(output_path)

if __name__=='__main__':
    main()