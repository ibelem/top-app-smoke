# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os, sys
import re, codecs
import shutil, glob
import json
import subprocess
import threading
import logging

def multi_replace(string, dic):
    rx = re.compile('|'.join(map(re.escape, dic)))
    def one_xlat(match):
        return dic[match.group(0)]
    return rx.sub(one_xlat, string)

def rename_file(dir, na, nb):
    files = os.listdir(dir)
    for i in files:
        if i.find(na) > -1:
            f_path = dir + os.sep + i
            if os.path.isfile(f_path):
                os.rename(f_path, dir + os.sep + i.replace(na,nb))

def del_files(path, ext):
    for root , dirs, files in os.walk(path):
        for name in files:
            if name.endswith(ext):
                os.remove(os.path.join(root, name))

def del_file(path):
    os.remove(path)

def del_dir(path):
    shutil.rmtree(path)

def find_file(pathname):
    return _find(pathname)

def find_dir(path):
    return _find(path, matchFunc=os.path.isdir)

def mk_dir(path):
    if not find_dir(path):
        os.mkdir(path)

#class Error(Exception): False
def _find(pathname, matchFunc=os.path.isfile):
    for dirname in sys.path:
        candidate = os.path.join(dirname, pathname)
        if matchFunc(candidate):
            return candidate
    #raise Error("##### Can't find file %s" % pathname)

def find_glob_path(filepath):
    return glob.glob(filepath)

def remove_glob_path(filepath):
    if find_glob_path(filepath):
        for path in glob.glob(filepath):
            os.remove(path)

def find_text_in_file(str, filepath):
    count = 0
    reader = open(filepath, "r+")
    line = reader.readline()
    while line != '' and line != None:
        li = re.findall(str, line)
        count = count + len(li)
        line = reader.readline()
    reader.close()
    return count

def find_text_in_file_case_insensitive(str, filepath):
    count = 0
    reader = open(filepath, "r+")
    line = reader.readline()
    while line != '' and line != None:
        line = line.lower()
        li = re.findall(str, line)
        count = count + len(li)
        line = reader.readline()
    reader.close()
    return count

def copy_tree(sourceDir,  targetDir):
    shutil.copytree(sourceDir,  targetDir)

def copy_file(sourceDir,  targetDir):
    shutil.copy(sourceDir,  targetDir)

def copy_files(sourceDir,  targetDir):
     if sourceDir.find(".git") > 0:
         return
     for file in os.listdir(sourceDir):
         sourceFile = os.path.join(sourceDir,  file)
         targetFile = os.path.join(targetDir,  file)
         if os.path.isfile(sourceFile):
             if not os.path.exists(targetDir):
                 os.makedirs(targetDir)
             if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                     open(targetFile, "wb").write(open(sourceFile, "rb").read())
         if os.path.isdir(sourceFile):
             First_Directory = False
             copy_files(sourceFile, targetFile)

def readFile(filename):
    try:
        file=open(filename,"r")
    except IOError:
        print >> sys.stderr, "file " + filename + " could not be opened"
        sys.exit(1)
    return file

def writeFile(filename, content):
    file = open(filename, "w")
    file.write(content)
    file.close()

def run_command(str):
    # use Popen instead of os.system to avoid "command line too long" on Windows
    p = subprocess.Popen("cmd /c " + str)
    p.wait()
    return p.returncode

def parse_c_json(pathname, field):
    fp = open(pathname)
    reader = fp.read()
    d = json.loads(reader, strict=False)
    if field.startswith('device_'):
        t = []
        for var in d['device']:
            t.append(var[field])
        return t
    if field.startswith('rtlib_'):
        t = []
        for var in d['runtimelib_test_build']:
            t.append(var[field])
        return t
    if field.startswith('keyword_fail'):
        t = []
        for var in d['logcat_check']:
            t.append(var[field])
        return t
    elif field.startswith('davinci_'):
        return d['davinci'][field]
    elif field.startswith('runtimelib_'):
        return d['runtimelib'][field]
    elif field.startswith('test_suite_'):
        return d['test_suite'][field]
    elif field.startswith('test_result_'):
        return d['test_result'][field]
    else:
        for var in d:
            value = d[field]
            return value

def log_info(message, file):
    logging.basicConfig(filename=file,level=logging.INFO, format='%(asctime)s: %(message)s')
    print message
    logging.info(message)

def log_err(err, file):
    logging.basicConfig(filename=file,level=logging.INFO, format='%(asctime)s: %(message)s')
    print err
    logging.error(err)
