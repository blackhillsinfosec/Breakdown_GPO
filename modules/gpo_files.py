import sys, os
from colorama import Fore, Style
from pathlib import Path


# Function to read the desired file into memory
def initialize_filecontent():

    # Command_line accepts a single argument as a file name
    if(len(sys.argv)==2):
        filename=sys.argv[1]
    # If passed more than a single file name, it will ask what file needs analyzed.
    else:
        filename=input(Style.BRIGHT+"What GPO report needs broken down? "+Style.RESET_ALL)

    #Attempt opening the specified file.
    try:
        # Start a context manager for file management
        with open(str(filename),'r', encoding='utf-16-le') as file:
            filecontent=file.read()
    except OSError:
        print(Style.BRIGHT+Fore.RED+f'Could not find the file \"{filename}\".'+Style.RESET_ALL)
        sys.exit()
    except Exception as e:
        print(Style.BRIGHT+Fore.RED+"Something wrong happened! Unable to determine the error.\n"+str(e)+Style.RESET_ALL)
        sys.exit()

    # Returns the initializaed filecontent
    return filecontent

# Where will the output go?
def create_output_dirs(current_working_directory):
    dir_created=False
    while(not dir_created):
        output_dir=input("\rExport directory (defaults to \"gpo_out\"): ")
        if(output_dir==""):
            output_dir="gpo_out"
        # Allow the creation of nested directories as output
        if(output_dir[0]=="\\" or output_dir[0]=="/"):
            output_dir=output_dir[1:]
        if(output_dir[-1]=="\\" or output_dir[-1]=="/"):
            output_dir=output_dir[:(len(output_dir)-1)]
        try:
            # Create output directory
            Path(os.path.join(current_working_directory, output_dir)).mkdir(parents=True, exist_ok=False)
            dir_created=True
        except FileExistsError:
            print(Style.BRIGHT+Fore.BLUE+os.path.join(current_working_directory, output_dir)+Style.RESET_ALL+" exists and cannot be overwritten!\n"+Style.BRIGHT+Fore.RED+"Try another name."+Style.RESET_ALL)
    # Create directories for GPO categories
    os.mkdir(os.path.join(current_working_directory, output_dir, "disabled_gpos"))
    os.mkdir(os.path.join(current_working_directory, output_dir, "ineffective_gpos"))
    os.mkdir(os.path.join(current_working_directory, output_dir, "enabled_gpos"))
    return output_dir

# Create a file name
def generate_file_name(name):
    new_name=""
    for indx_inner, letter in enumerate(name):
        # Eliminate the outcome of "__" in the filename
        if(indx_inner==(len(name)-1)):
            if letter=="-" or letter==",":
                pass
            elif letter==" " or letter=="/" or letter=="\\":
                new_name=new_name+"_"
            else:
                new_name=new_name+letter
        elif((letter==" " or letter=="/" or letter=="\\") and (name[indx_inner+1]==" " or name[indx_inner+1]=="/" or name[indx_inner+1]=="\\" or name[indx_inner+1]=="-" or name[indx_inner+1]==",")):
            pass
        elif letter=="-" or letter==",":
            pass
        elif letter==" " or letter=="/" or letter=="\\":
            new_name=new_name+"_"
        else:
            new_name=new_name+letter
    return new_name

# Create Summary file
def create_summary_file(cwd, output_dir, filecontent, indexes):
    enabled_indx=[]
    disabled_indx=[]
    ineffective_indx=[]
    # Preserve the order of effect of the GPOs.
    name_indx=0
    # Create summary file in the new directory.
    try:
        with open(os.path.join(cwd, output_dir, "gpo_summary.txt"), encoding='utf-8', mode='w+') as summary_file:
            for indx, _ in enumerate(indexes.html_start):
                if(indexes.status_anchor[indx]=="disabled   "):
                    disabled_indx.append(indx)
                elif(indexes.effective_anchor[indx]=="ineffective"):
                    ineffective_indx.append(indx)
                elif(indexes.status_anchor[indx] in ["enabled    ", "user       ", "computer   "]):
                    enabled_indx.append(indx)
            # Create summary file with a context manager
            summary_file.write(
                f"GPO Summary\n-----------\n{str(len(indexes.html_start))} GPOs were found.\n{str(len(enabled_indx))} enabled GPOs were found.\n{str(len(disabled_indx))} disabled GPOs were found.\n{str(len(ineffective_indx))} ineffective GPOs were found.\n\nEnabled GPOs:\n")
            for indx, _ in enumerate(indexes.html_start):
                if((indexes.status_anchor[indx] in ["enabled    ","user       ","computer   "]) and (indexes.effective_anchor[indx] != "ineffective")):
                    name_indx+=1
                    summary_file.write((f"\t\t{indexes.status_anchor[indx]}\t\t{str(name_indx)}_{filecontent[indexes.title_start[indx]:indexes.title_end[indx]]}\n"))
            summary_file.write("\nIneffective GPOs:\n")
            for indx in ineffective_indx:
                summary_file.write(f"\t\t{indexes.status_anchor[indx]}\t\t{filecontent[indexes.title_start[indx]:indexes.title_end[indx]]}\n")
            summary_file.write("\nDisabled GPOs:\n")
            for indx in disabled_indx:
                summary_file.write(f"\t\t{indexes.status_anchor[indx]}\t\t{filecontent[indexes.title_start[indx]:indexes.title_end[indx]]}\n")
    except:
        print(Style.BRIGHT+Fore.RED+"If this error is occurring, the cause is unknown and the export was not completed.\nThe files in the output directory are corrupted.\nThis error occured when creating the summary file."+Style.RESET_ALL)
        sys.exit()

# Create GPOs as individual files
def create_gpo_files(cwd, output_dir, filecontent, indexes):
    # Track order of the GPO in name
    name_index=0
    for indx, _ in enumerate(indexes.html_start):
        # Find the name of the GPO
        gpo_name=filecontent[indexes.title_start[indx]:indexes.title_end[indx]]
        # Clean-up GPO name to name file
        new_name=generate_file_name(gpo_name)    
        # Use context managers to create and populate files
        if(indexes.status_anchor[indx]=="disabled   "):
            try:
                with open(os.path.join(cwd, output_dir,"disabled_gpos",new_name+".html"), encoding='utf-8', errors='ignore', mode='w+') as new_file:
                    new_file.write(filecontent[indexes.html_start[indx]:indexes.html_end[indx]])
            except Exception as e:
                print(Style.BRIGHT+Fore.RED+"An error ocurred writing file: "+new_name+".html\n"+str(e)+Style.RESET_ALL)
        elif(indexes.effective_anchor[indx]=="ineffective"):
            try:
                with open(os.path.join(cwd, output_dir,"ineffective_gpos",new_name+".html"), encoding='utf-8', errors='ignore', mode='w+') as new_file:
                    new_file.write(filecontent[indexes.html_start[indx]:indexes.html_end[indx]])
            except Exception as e:
                print(Style.BRIGHT+Fore.RED+"An error ocurred writing file: "+new_name+".html\n"+str(e)+Style.RESET_ALL)
        elif(indexes.status_anchor[indx] in ["enabled    ","user       ","computer   "]):
            name_index+=1
            try:
                with open(os.path.join(cwd, output_dir,"enabled_gpos",str(name_index)+"_"+new_name+".html"), encoding='utf-8', errors='ignore', mode='w+') as new_file:
                    new_file.write(filecontent[indexes.html_start[indx]:indexes.html_end[indx]])
            except Exception as e:
                print(Style.BRIGHT+Fore.RED+"An error ocurred writing file: "+new_name+".html\n"+str(e)+Style.RESET_ALL)
        else:
            name_index+=1
            try:
                with open(os.path.join(cwd, output_dir,str(name_index)+"_"+new_name+".html"), encoding='utf-8', errors='ignore', mode='w+') as new_file:
                    new_file.write(filecontent[indexes.html_start[indx]:indexes.html_end[indx]])
            except Exception as e:
                print(Style.BRIGHT+Fore.RED+"An error ocurred writing file: "+new_name+".html\n"+str(e)+Style.RESET_ALL)
