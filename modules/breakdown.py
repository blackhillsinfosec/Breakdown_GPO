from modules.attributes import find_attributes
from modules.files import write_individual_files

def breakdown(file_path, output_dir):
    counter=0
    start_indices=[]
    end_indices=[]
    gpo_statuses=[]
    names = []
    ineffective=[]
    # Search the document for attibutes of interest
    for attribute in find_attributes(file_path):
        #
        counter+=1
        if counter > 5:
            counter = 1
        #
        # Closing HTML tags
        if (counter)==5 and isinstance(attribute, int):
            end_indices.append(attribute)
        elif (counter) == 4 and isinstance(attribute, bool):
            ineffective.append(attribute)
        # GPO Status
        elif (counter)==3 and isinstance(attribute, str):
            gpo_statuses.append(attribute)
        # Title Tags
        elif (counter)==2 and isinstance(attribute, str):
            names.append(attribute)
        # Opening HTML Tags    
        elif (counter)==1 and isinstance(attribute, int):
            start_indices.append(attribute)
        else:
            print(f"{counter} {type(attribute)} {attribute}")

    # Ensure the attibute indices are the same length.
    # If the same number isn't returned, the file is corrupt or incorrect and cannot be broken down.
    if len(start_indices) == len(end_indices) and len(start_indices) == len(names) and len(start_indices) == len(gpo_statuses) and len(start_indices) == len(ineffective):
        write_individual_files(start_indices, names, gpo_statuses, ineffective, file_path, output_dir)
    else:
       quit()