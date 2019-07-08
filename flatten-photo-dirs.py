#!/usr/bin/python

import getopt
import os
import shutil
import sys

def Usage():
    print("Usage: %s -s <directory> -od <directory> -y <year>" % sys.argv[0])
    print("  -s <directory>  source directory of all pictures")
    print("  -d <directory>  destination directory to create with flattened files")
    print("  -y <num>        year to copy/flatten")

def main():  
    srcDirectory  = ''
    destDirectory = ''
    year = 0
    try:
        # process command arguments
        ouropts, args = getopt.getopt(sys.argv[1:],"s:d:y:h")
        for o, a in ouropts:
            if   o == '-s':
                srcDirectory = a
            elif o == '-d':
                destDirectory = a
            elif o == '-y':
                year  = int(a)
            elif o == '-h':
                Usage()
                sys.exit(0)
    except getopt.GetoptError as e:
        print(str(e))
        Usage()
        sys.exit(2)
 
    if type(srcDirectory) != str or len(srcDirectory) <= 0:
        print("please use -s for source directory")
        Usage()
        sys.exit(0)
    if type(destDirectory) != str or len(destDirectory) <= 0:
        print("please use -d for destination directory")
        Usage()
        sys.exit(0)
    if type(year) != int or year <= 0:
        print("please use -y for year")
        Usage()
        sys.exit(0)

    os.mkdir(destDirectory)

    total = 0
    list_dirs = os.walk(srcDirectory)
    for root, dirs, files in list_dirs: 
        for f in files:
            if f.endswith("MOV"):
                continue
            if f.endswith("mov"):
                continue
            if f.endswith("m4v"):
                continue
            if f.endswith("mp4"):
                continue
            if f.endswith("pdf"):
                continue
            if f.endswith("DS_Store"):
                continue
            srcName = os.path.join(root, f)
            yearDirPath = os.path.join(srcDirectory, "2017-")
            if srcName.find(yearDirPath) != -1:
                # src/2017-01(Jan)-04.phone/IMG03.mpg
                # dest/01(Jan)-04.phone.IMG03.mpg
                destName = srcName.replace(srcDirectory, "").replace("/",".")
                destName = destName.replace("{0}-".format(year), "")
                destName = os.path.join(destDirectory, destName[1:])
                print "cp {0} {1}...".format(srcName, destName)
                shutil.copy (srcName, destName)
                total += 1
    print "{0} total files copied".format(total)
    
if __name__ == "__main__":
  main()

