#!/usr/bin/python

# python ./all-gitlog.py -u <user> -d <directory> -s <since>
#
# Tool to inspect Github and pull local copies of all repos and gists
# for the given user. And get the git logs for each.
#
# Why?  Every ask yourself the question 'What did I do in git since
#       <insert date>?'

import getopt
import json
import os
import shutil
import subprocess
import sys
from urllib.request import urlopen

def Usage():
  print("Usage: %s -u <github user> -d <directory>" % sys.argv[0])
  print("  -u <github user>  github user name")
  print("  -d <directory>    local directory for repos and gists")
  print("  -S <date>         get logs since date")

def main():

  githubUser  = ''
  destDirectory = ''
  sinceDate = ''
  try:
    # process command arguments
    ouropts, args = getopt.getopt(sys.argv[1:],"u:d:s:h")
    for o, a in ouropts:
      if   o == '-u':
        githubUser = a
      if   o == '-d':
        destDirectory = a
      if   o == '-s':
        sinceDate = a
      elif o == '-h':
        Usage()
        sys.exit(0)
  except getopt.GetoptError as e:
    print(str(e))
    Usage()
    sys.exit(2)

  if type(githubUser) != str or len(githubUser) <= 0:
      print("please use -u for github user")
      Usage()
      sys.exit(0)
  if type(destDirectory) != str or len(destDirectory) <= 0:
      print("please use -d for local directory")
      Usage()
      sys.exit(0)


  repos = os.path.join(destDirectory, 'repos')
  for dir in os.listdir(repos):
      if '.json' in dir:
       continue
      path = os.path.join(destDirectory, 'repos', dir)
      os.chdir(path)
      subprocess.call(['echo'])
      subprocess.call(['echo', '--------------------------------------------'])
      subprocess.call(['pwd'])
      subprocess.call(['git', 'log', '--since', sinceDate])
      os.chdir(os.path.join('..', '..', '..'))

if __name__ == "__main__":
  main()