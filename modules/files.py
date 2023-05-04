import os

def write_individual_files(indices, file_path, output_dir):
    start_list, _, gpo_statuses, names, ineffective = indices.return_indices()
    iteration=-1
    os.mkdir(output_dir)
    try:
        summary_handle = open(os.path.join(output_dir, "Breakdown Summary.csv"), mode='w+')
        summary_handle.write("GPO #,GPO Name,GPO Status,Ineffective\n")
        # Read each line from the original file one-by-one
        with open(file_path, 'r', encoding='utf-16-le') as read_handle:
            write_handle=None
            for indx, line in enumerate(read_handle):
                if indx in start_list:
                    if write_handle!=None:
                        write_handle.close()
                    iteration+=1
                    if (("enabled" in gpo_statuses[iteration]) or ("computer" in gpo_statuses[iteration]) or ("user" in gpo_statuses[iteration])) and (ineffective[iteration]==True):
                        if (not (os.path.exists(os.path.join(output_dir, "ineffective")))):
                            os.mkdir(os.path.join(output_dir, "ineffective"))
                        write_handle = open(f"{output_dir}/ineffective/{iteration+1} - {names[iteration]}.html", encoding='utf-8', errors='ignore', mode='w+')
                        summary_handle.write(f"{iteration+1},{names[iteration]},{gpo_statuses[iteration]},{ineffective[iteration]}\n")
                    else:
                        if (not (os.path.exists(os.path.join(output_dir, gpo_statuses[iteration])))):
                            os.mkdir(os.path.join(output_dir, gpo_statuses[iteration]))
                        write_handle = open(f"{output_dir}/{gpo_statuses[iteration]}/{iteration+1} - {names[iteration]}.html", encoding='utf-8', errors='ignore', mode='w+')
                        summary_handle.write(f"{iteration+1},{names[iteration]},{gpo_statuses[iteration]},{ineffective[iteration]}\n")
                else:
                    write_handle.write(line)     
            write_handle.close()
    except KeyboardInterrupt:
        write_handle.close()
        summary_handle.close()
        read_handle.close()