import os
import hashlib
import argparse
from collections import defaultdict

def search_for_equal_files(path):            
    for filepath in get_files(path): 
        next = get_hash_of_file(filepath) 
        files_dict[next].append(filepath)

def get_files(path):
    file_list = []
    for rootdir, _, files in os.walk(path):
        for filepath in files:
            if ((not os.path.islink(filepath)) and (not (filepath[0] == '~' or filepath[0] == '.'))):
                file_list.append(os.path.join(rootdir, filepath))

    return file_list

def print_equal_files():      
    for _, files in files_dict.items():
        if (len(files) > 1):
            print(':'.join(files))

def get_hash_of_file(filepath):
    with open(filepath, 'rb') as f:
        h = hashlib.sha1()
        s = f.read(5475)
        while (s):
            h.update(s)       
            s = f.read(5475) 
        return h.hexdigest()            
    
                
if __name__ == "__main__":
    files_dict = defaultdict(list)
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help = 'Root directory of the search path')
    rootpath = parser.parse_args().path
    search_for_equal_files(rootpath)
    print_equal_files()