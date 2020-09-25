import os
from os import path
import datetime
from datetime import date, time, datetime, timedelta
import time
import shutil
from shutil import make_archive
from zipfile import ZipFile

def path_exists(path2):
    return path.exists(path2)

def dir_exists(path2):
    return path.isdir(path2)

if __name__ == '__main__':
    fullfile = '/Users/sbommireddy/Documents/python/assignments/dq/python/classes.py'
    print(path_exists(fullfile))
    print(path_exists("classes.py"))
    print(dir_exists("/Users/sbommireddy/Documents/python/assignments/dq/python/"))
    print(os.name)

    dir, file = path.split(fullfile)
    print(dir)
    print(file)

    # Get file modified time.
    print(time.ctime(path.getmtime(fullfile)))
    print(time.ctime(path.getatime(fullfile)))

    shutil.copy(fullfile, fullfile+'.bak')
    #shutil.copystat(fullfile, fullfile+'.bak') # Copies metadata
    os.rename(fullfile+'.bak',fullfile+'.bk')

    #Put things into zip archive.
    root_dir, tail = path.split(fullfile)
    #shutil.make_archive("sidarchive","zip",root_dir)
    with ZipFile("sidtest.zip","w") as newzip:
        # selectively add files to zip
        newzip.write(fullfile)
