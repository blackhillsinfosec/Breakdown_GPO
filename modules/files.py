from modules.handles import Handles

def report_count(data_obj):
    col = 0
    for key in data_obj.keys():
        if len(str(data_obj.get(key))) > col:
            col = len(str(data_obj.get(key))) + 2
    for key in data_obj.keys():
        if(data_obj.get(key) > 0):
            print(f"{col*' '}{data_obj.get(key)}{(col-len(str(data_obj.get(key))))*' '}{key}")
    print()

def write_individual_files(indices, file_path, output_dir):

    handles = Handles(file_path, output_dir)

    try:
        # Read each line from the original file one-by-one
        for indx, line in enumerate(handles.read_handle):
            if indx in indices.start_indices:
                handles.set_handle(output_dir, indices)
            handles.write_file(line)

        report_count(handles.get_data())

    except KeyboardInterrupt:
        print("Keyboard interupt detected!")

    except Exception as e:
        print(e)