#!/bin/python3.6

from TimeIt import TimeIt
import argparse
from pathlib import Path

parser = argparse.ArgumentParser('find', add_help=True, description='search for files in a directory hierarchy')
parser.add_argument('path', nargs='?', default='.')
parser.add_argument('-name')
parser.add_argument('-type', help="TYPE is f|l|d|c|b|s|p")

# parser.print_help()

def search_all(path, files = []):
    p = Path(path)
    for file in p.iterdir():
        if file.is_dir():
            files.append(str(file.parent) + '/' + file.name)
            search_all(file, files = files)
        else:
            files.append(str(file.parent) + '/' + file.name)

def search_dir(path, files = []):
    p = Path(path)
    for file in p.iterdir():
        if file.is_dir():
            files.append(str(file.parent)+'/' + file.name)
            search_dir(file, files = files)


def file_type(file:Path, type):
    if type == 'f':
        return file.is_file()
    if type == 'l':
        return file.is_symlink()
    if type == 'c':
        return file.is_char_device()
    if type == 'b':
        return file.is_block_device()
    if type == 's':
        return file.is_socket()
    if type == 'p':
        return file.is_fifo()

def search_others(path, type, files = []):
    p = Path(path)
    for file in p.iterdir():
        if file.is_dir():
            search_others(file, type, files = files)
        elif file_type(file, type):
            files.append(str(file.parent) + '/' + file.name)

def searchbyname(path, name, files = []):
    p = Path(path)
    dstname = name[1:]
    for file in p.iterdir():
        if file.is_dir():
            searchbyname(file, name, files = files)
        elif file.suffix == dstname:
            files.append(str(file.parent) + '/' + file.name)

@TimeIt
def searchfiles(path, name = None, type = None, files = []):
    if name:
        searchbyname(path, name, files = files)
    elif type:
        if type == 'd':
            search_dir(path, files = files)
        else:
            search_others(path, type, files = files)
    else:
        search_all(path, files = files)

    return files

para = parser.parse_args('/Users/Simone/Downloads -name *.pdf'.split())
print(para)

result = searchfiles(para.path, name = para.name, type = para.type)
for file in result:
    print(file)

# 看了一下逻辑，写的超乎我的想象，比我想的全面多了。