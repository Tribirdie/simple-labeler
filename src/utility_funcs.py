from pathlib import Path
import os
import json

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

    try:
        for d in os.listdir(directory):
            filename = Path(d).name
            
            if not file_ext_allowed(filename, ext_allowed):
                continue
            
            full_file_directory = os.path.join(directory, d)

            if full_file_directory not in file_label_statuses:
                file_label_statuses[full_file_directory] = "False"

            full_file_paths.append(full_file_directory)
            dir_list += filename
            dir_list += "\n"
            
        amount_of_entries = len(full_file_paths)
        return dir_list, full_file_paths
    except FileNotFoundError:
        return 0,0

def make_json(directory):
    with open(directory, 'w') as json_file:
        json_file.write("{}")

def dump_dict_to_json(json_f, dictionary):
    with open(json_f, 'w') as json_file: 
        json.dump(dictionary, json_file, indent=2)

def json_entry_exists(json_f):
    '''Remove entries from the persistant json file if they do not exist'''
    load_json = json.load(json_f)

    for key in list(load_json.keys()):
        if not os.path.exists(key):
            load_json.pop(key)

    return load_json

def load_json_if_exists(json_f):
    with open(json_f, 'r') as json_file:
         check_if = json_entry_exists(json_file)
         return check_if
    return {}
