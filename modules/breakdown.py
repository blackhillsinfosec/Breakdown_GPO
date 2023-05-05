from modules.attributes import find_attributes
from modules.files import write_individual_files
from modules.indices import Indices

def breakdown(file_path, output_dir):
    indices = Indices()
    # Search the document for attibutes of interest
    for attribute in find_attributes(file_path):
        indices.parse_index(attribute)

    # Ensure the attibute indices are the same length.
    # If the same number isn't returned, the file is corrupt or incorrect and cannot be broken down.
    if indices.append_start.count == indices.append_end.count and indices.append_start.count == indices.append_name.count and indices.append_start.count == indices.append_status.count and indices.append_start.count == indices.append_ineffective.count:
        print(f"\n{indices.append_start.count} GPOs detected.")
        write_individual_files(indices, file_path, output_dir)
    else:
       print("ERROR in indices!\nThe input file is corrupt or incorrect.")
       quit()