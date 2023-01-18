#! /bin/python3
# Version 1.2.0
from colorama import Fore, Style
from pathlib import Path
import sys, os, time, threading

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
    except:
        print(Style.BRIGHT+Fore.RED+"Something wrong happened! Unable to determine the error."+Style.RESET_ALL)
        sys.exit()

    # Returns the initializaed filecontent
    return filecontent

# Class used to define index storage object.
class GPO_Indexes:
    def __init__(self):
        self.html_start=[]
        self.html_end=[]
        self.title_start=[]
        self.title_end=[]
        self.link_anchor=[]
    def __str__(self):
        return f'''
            Master:
            html_start indexes are {self.html_start}
            html_end indexes are {self.html_end}
            title_start indexes are {self.title_start}
            title_end indexes are {self.title_end}
            link_anchor indexes are {self.link_anchor}
        '''
    def print_index_counts(self):
        print(f'''
            Counts:
            html_start - {len(self.html_start)}
            html_end - {len(self.html_end)}
            title_start - {len(self.title_start)}
            title_end - {len(self.title_end)}
            link_anchor - {len(self.link_anchor)}
        ''')
    def validate_indexes(self):
        error_out = ""
        
        gpo_num = len(self.html_start)
        for indx in [self.html_end, self.title_start, self.title_end, self.link_anchor]:
            if len(indx)!=gpo_num:
                error_out = "\r"+Style.BRIGHT+Fore.RED+"Indexing experienced an error.\n"+Style.RESET_ALL+"It appears the file might be corrupted.\nThere is not a matching number of indexes!"        
        return error_out

    def construct_master_index(self, thread_list):
        for thread in thread_list:
            for indx in thread.html_start:
                self.html_start.append(indx)
            for indx in thread.html_end:
                self.html_end.append(indx)
            for indx in thread.title_start:
                self.title_start.append(indx)
            for indx in thread.title_end:
                self.title_end.append(indx)
            for indx in thread.link_anchor:
                self.link_anchor.append(indx)

# Class for threads to index file
class indx_thread(threading.Thread):
    def __init__(self, read_material, read_start, read_end, thread_name):
        threading.Thread.__init__(self)
        #Each thread will track it's own found indexes
        self.name = thread_name
        self.read_material = read_material
        self.read_start = read_start
        self.read_end = read_end
        self.html_start = []
        self.html_end = []
        self.title_start = []
        self.title_end = []
        self.link_anchor = []
    def __str__(self):
        return f'''
            html_start indexes are {self.html_start}
            html_end indexes are {self.html_end}
            title_start indexes are {self.title_start}
            title_end indexes are {self.title_end}
            link_anchor indexes are {self.link_anchor}
        '''
    def run(self):
        
        for indx, content in enumerate(self.read_material[self.read_start:self.read_end]):
            if(content=="<"):
                # Search for opening HTML tags of interest
                if(self.read_material[(self.read_start+indx):(self.read_start+indx)+6]=="<html " and self.read_material[(self.read_start+indx)-1:(self.read_start+indx)+6]!="\"<html "):
                    self.html_start.append((self.read_start+indx))
                elif(self.read_material[(self.read_start+indx):(self.read_start+indx)+7]=="<title>" and self.read_material[(self.read_start+indx)-1:(self.read_start+indx)+8]!="\"<title>\""):
                    self.title_start.append((self.read_start+indx)+7)
                elif(self.read_material[(self.read_start+indx):(self.read_start+indx)+101]=="<th scope=\"col\">Link Status</th><th scope=\"col\">Path</th></tr>\n    <tr><td colspan=\"4\">None</td></tr>"):
                    self.link_anchor.append("unlinked")    
                elif(self.read_material[(self.read_start+indx):(self.read_start+indx)+62]=="<th scope=\"col\">Link Status</th><th scope=\"col\">Path</th></tr>"):
                    self.link_anchor.append((self.read_start+indx))
                # Search for closing HTML tags of interest.
                elif(self.read_material[(self.read_start+indx):(self.read_start+indx)+7]=="</html>" and self.read_material[(self.read_start+indx):(self.read_start+indx)+8]!="</html>\""):
                    self.html_end.append((self.read_start+indx))
                elif(self.read_material[(self.read_start+indx):(self.read_start+indx)+8]=="</title>" and self.read_material[(self.read_start+indx)-1:(self.read_start+indx)+9]!="\"</title>\"" and self.read_material[(self.read_start+indx-1):(self.read_start+indx)+9]!="\"</title>\\"):
                    self.title_end.append((self.read_start+indx))

# Index GPOReport
def concurrent_index_file(filecontent):
    thread_count = 3
    thread_divisible = int((len(filecontent)/thread_count))
    thread_pool = []

    for count in range(thread_count):
        if(count!=thread_count-1):
            thread_pool.append(indx_thread(filecontent, (thread_divisible*count), ((thread_divisible*(count+1))-1), "thread"+str(count)))
        else:
            thread_pool.append(indx_thread(filecontent, (thread_divisible*count), len(filecontent), "thread"+str(count)))
    
    # Push threads to the background and start
    for thread in thread_pool:
        thread.setDaemon(True)
        thread.start()
    
    # Print feedback to indicate processing.
    counter = 0
    options = [
        "\r"+Style.BRIGHT+Fore.BLUE+"."+"   "+Style.RESET_ALL,
        "\r"+Style.BRIGHT+Fore.BLUE+"."+Fore.GREEN+".  "+Style.RESET_ALL,
        "\r"+Style.BRIGHT+Fore.BLUE+"."+Fore.GREEN+"."+Fore.RED+". "+Style.RESET_ALL,
        "\r"+Style.BRIGHT+Fore.BLUE+"."+Fore.GREEN+"."+Fore.RED+"."+Fore.WHITE+"."+Style.RESET_ALL]
    while(threading.active_count() > 1):
        if(counter==4):
            counter=0
        print(options[counter], end="")
        time.sleep(0.05)
        counter+=1

    Indexes = GPO_Indexes()
    Indexes.construct_master_index(thread_pool)
    return Indexes

# Check for Errors - Exit in the case of error
def review_validation(validate, start):
    if(validate):
        print("\r"+validate)
        sys.exit()
    else:
        print(Style.BRIGHT+Fore.GREEN+f'\rParsing the GPO Report took{time.time() - start : .2f} seconds.'+Style.RESET_ALL)

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
    # Create directory for unlinked GPOs
    os.mkdir(os.path.join(current_working_directory, output_dir, "0_unlinked_gpos"))
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
    # Index unlinked indexes, unliked indexes will be output after linked GPOs
    unlinked_indx=[]
    # Preserve the order of effect of the GPOs.
    name_indx=0
    # Create summary file in the new directory.
    try:
        with open(os.path.join(cwd, output_dir, "0_gpo_summary.txt"),'w+') as summary_file:
            # If the GPO is unlinked, save for adding to the end of the summary file
            for indx, _ in enumerate(indexes.html_start):
                if(indexes.link_anchor[indx]=="unlinked"):
                    unlinked_indx.append(indx)
            # Create summary file with a context manager
            summary_file.write("GPO Summary\n"+str(len(indexes.html_start))+" GPOs were found.\n"+str(len(unlinked_indx))+" unlinked GPOs were found.\n\nLinked GPOs:\n\n")
            for indx, _ in enumerate(indexes.html_start):
                if(indexes.link_anchor[indx]!="unlinked"):
                    name_indx+=1
                    summary_file.write(("\t"+str(name_indx)+"_"+filecontent[indexes.title_start[indx]:indexes.title_end[indx]]+"\n"))
            summary_file.write("\nUnlinked GPOs:\n\n")
            for indx in unlinked_indx:
                summary_file.write("\t"+filecontent[indexes.title_start[indx]:indexes.title_end[indx]]+"\n")
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
        if(indexes.link_anchor[indx]=="unlinked"):
            try:
                with open(os.path.join(cwd, output_dir,"0_unlinked_gpos",new_name+".html"),'w+') as new_file:
                    new_file.write(filecontent[indexes.html_start[indx]:indexes.html_end[indx]])
            except:
                print(Style.BRIGHT+Fore.RED+"An error ocurred writing file: "+new_name+".html"+Style.RESET_ALL)
        else:
            name_index+=1
            try:
                with open(os.path.join(cwd, output_dir,str(name_index)+"_"+new_name+".html"),'w+') as new_file:
                    new_file.write(filecontent[indexes.html_start[indx]:indexes.html_end[indx]])
            except:
                print(Style.BRIGHT+Fore.RED+"An error ocurred writing file: "+new_name+".html"+Style.RESET_ALL)

def main():
    cwd=os.getcwd()
    # Memory-related processes. Keyboard Interupt shouldn't be a problem.
    try:
        start = time.time()
        filecontent=initialize_filecontent()
        Indexes = concurrent_index_file(filecontent)
        validate=Indexes.validate_indexes()
        review_validation(validate, start)
        output_dir=create_output_dirs(cwd)
    # Cleanly exit the program if interupt is found.
    except KeyboardInterrupt:
        print("\r\n", end="")
        sys.exit()
    try:
        create_summary_file(cwd, output_dir, filecontent, Indexes)
        create_gpo_files(cwd, output_dir, filecontent, Indexes)
        print(Style.BRIGHT+Fore.GREEN+"Export complete."+Style.RESET_ALL)
    except KeyboardInterrupt:
        print("\rExport was interupted. The files are corrupt and not complete.")
        sys.exit

if __name__=='__main__':
    main()
