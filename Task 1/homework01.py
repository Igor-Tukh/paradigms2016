import os
import hashlib
import argparse
#import time

def search(path):            
    global files_dict
    cur_dir = os.walk(os.path.dirname(os.path.realpath(__file__)) + '\\' + path)
    for rootdir, _, files in cur_dir:
        for file in files:
            if (file[0] != '.' and file[0] != '~'):
                filepath = rootdir + '\\' + file
                with open(filepath, 'r') as f:
                    h = hashlib.sha1()
                    s = f.read(5475).encode('utf-8')
                    while (s):
                        h.update(s)       
                        s = f.read(5475).encode('utf-8') 
                    next = h.hexdigest() 
                    if (next in files_dict):
                        files_dict[next].append(rootdir+'\\'+file)
                    else:
                        files_dict[next] = [rootdir+'\\'+file]

def printing():        
    global files_dict
    for hash in files_dict:
        if (len(files_dict[hash]) > 1):
            for ind, name in enumerate(files_dict[hash]):
                if (ind - len(files_dict[hash]) + 1):
                    print(name+':',end="")
                else:
                    print(name)

#startime = round(time.time() * 1000)
files_dict = {}
parser = argparse.ArgumentParser()
parser.add_argument('path', help = 'Root directory of the search local path')
rootpath = parser.parse_args().path
search(rootpath)
printing()
#print(round(time.time() * 1000)-startime)