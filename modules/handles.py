import os

# Written as a decorator to decorate set_handle
def write_summary(method):
    def wrapper(Handles, output_dir, indices):
        Handles.summary_handle.write(f"{Handles.set_handle.count+1},{indices.names[Handles.set_handle.count]},{indices.gpo_statuses[Handles.set_handle.count]},{indices.ineffective[Handles.set_handle.count]}\n")
        return method(Handles, output_dir, indices)
    return wrapper

def count_files(method):
    def wrapper(obj, output_dir, indices):
        wrapper.count += 1
        if (not (indices.ineffective[obj.set_handle.count])):
            wrapper.data[indices.gpo_statuses[obj.set_handle.count]] += 1
        else:
            wrapper.data["Ineffective"] += 1
        return method(obj, output_dir, indices)
    wrapper.data = { "Enabled": 0, "Ineffective": 0, "Computer": 0, "User": 0, "Disabled": 0}
    wrapper.count = -1
    return wrapper

class Handles:

    def __init__(self, file_path, output_dir):
        # Create Output Directory
        os.mkdir(output_dir)
        # Create Summary CSV File
        self.summary_handle = open(os.path.join(output_dir, "Breakdown Summary.csv"), mode='w+')
        self.summary_handle.write("GPO #,GPO Name,GPO Status,Ineffective\n")
        self.read_handle = open(file_path, 'r', encoding='utf-16-le')
        # Instantiate the Active File Handle
        self.current_handle=None
    
    def __del__(self):
        # Close file handles when object destroyed
        self.read_handle.close()
        self.summary_handle.close()
        if(self.current_handle != None):
            self.current_handle.close()
    
    @count_files
    @write_summary
    def set_handle(self, output_dir, indices):
        if(self.current_handle != None):
            self.current_handle.close()
        if (("Enabled" in indices.gpo_statuses[self.set_handle.count]) or ("Computer" in indices.gpo_statuses[self.set_handle.count]) or ("User" in indices.gpo_statuses[self.set_handle.count])) and (indices.ineffective[self.set_handle.count]==True):
            if (not (os.path.exists(os.path.join(output_dir, "Ineffective")))):
                os.mkdir(os.path.join(output_dir, "Ineffective"))
            self.current_handle = open(f"{output_dir}/Ineffective/{self.set_handle.count+1} - {indices.names[self.set_handle.count]}.html", encoding='utf-8', errors='ignore', mode='w+')
        else:
            if (not (os.path.exists(os.path.join(output_dir, indices.gpo_statuses[self.set_handle.count])))):
                os.mkdir(os.path.join(output_dir, indices.gpo_statuses[self.set_handle.count]))
            self.current_handle = open(f"{output_dir}/{indices.gpo_statuses[self.set_handle.count]}/{self.set_handle.count+1} - {indices.names[self.set_handle.count]}.html", encoding='utf-8', errors='ignore', mode='w+')
    
    def write_file(self, line):
        self.current_handle.write(line)

    def get_data(self):
        return self.set_handle.data