from pathlib import Path
import os

def file_ext_allowed(file_str, ext_list):
    '''Checks if file in directory is supported filetype'''
    for ext in ext_list:
        if file_str.endswith(ext):
            return True
        continue

    return False

def get_files_in_dir(directory, ext_allowed, file_label_statuses):
    dir_list = ""
    full_file_paths = []
    
    for d in os.listdir(directory):
        filename = Path(d).name
        
        if not file_ext_allowed(filename, ext_allowed):
            continue
        
        full_file_directory = os.path.join(directory, d)

        file_label_statuses[full_file_directory] = "False"
        full_file_paths.append(full_file_directory)
        dir_list += filename
        dir_list += "\n"

    amount_of_entries = len(full_file_paths)

    return dir_list, full_file_paths

