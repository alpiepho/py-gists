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
import sys
from urllib.request import urlopen

from subprocess import PIPE, run

def Usage():
  print("Usage: %s -u <github user> -d <directory>" % sys.argv[0])
  print("  -u <github user>  github user name")
  print("  -d <directory>    local directory for repos and gists")
  print("  -S <date>         git log --since, ie. 2019-07-31")
  print("  -A <date>         git log --after, ie. 2019-06-01")
  print("  -U <date>         git log --until, ie. 2019-07-01")
  print("  -I <list>         list of repos to ignore, ie 'gatsby,test1")

def main():

  githubUser  = ''
  destDirectory = ''
  sinceDate = ''
  afterDate = ''
  untilDate = ''
  ignoreList = ''

  print("command:")
  print("python3", " ".join(sys.argv))

  try:
    # process command arguments
    ouropts, args = getopt.getopt(sys.argv[1:],"u:d:S:A:U:I:h")
    for o, a in ouropts:
      if   o == '-u':
        githubUser = a
      if   o == '-d':
        destDirectory = a
      if   o == '-S':
        sinceDate = a
      if   o == '-A':
        afterDate = a
      if   o == '-U':
        untilDate = a
      if   o == '-I':
        ignoreList = a.split(',')
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

  if sinceDate and afterDate:
      print("please use only -S, or -A and -U")
      Usage()
      sys.exit(0)
  if sinceDate and untilDate:
      print("please use only -S, or -A and -U")
      Usage()
      sys.exit(0)

  all_names = []
  all_commit_count = dict()
  repos = os.path.join(destDirectory, 'repos')
  for dir in os.listdir(repos):
      if '.json' in dir:
        continue
      if os.path.basename(dir) in ignoreList:
        continue

      path = os.path.join(destDirectory, 'repos', dir)
      os.chdir(path)

      if (sinceDate):
        command = ['git', 'log', '--since', sinceDate]
      else:
        command = ['git', 'log', '--after', afterDate, '--until', untilDate]
      result2 = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
      if (len(result2.stdout)):
        print()
        print()
        print("####################################################################################################################################")
        print("####################################################################################################################################")
        command = ['pwd']
        result1 = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        #print(result.returncode, result.stdout, result.stderr)
        name = os.path.basename(result1.stdout).strip()
        print("REPO: ", name)
        all_names.append(name)

        print(result2.stdout, result2.stderr)
        count = 0
        lines = result2.stdout.split('\n')
        for line in lines:
          if "commit " in line:
            count += 1
        all_commit_count[name] = count

      os.chdir(os.path.join('..', '..', '..'))

  print()
  print()
  print('===========================================')
  print('Summary of REPOS:')
  for name in all_names:
    s = '{:3d}'.format(all_commit_count[name])
    print(s, " ", name)


if __name__ == "__main__":
  main()