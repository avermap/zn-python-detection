import myutils
import time
import sys
import json
import subprocess
from datetime import datetime
import requests 
import pickle
from pydriller import RepositoryMining
 

def checkFork(r):
  ### checks if a repository is a fork of another one
  myheaders = {'Authorization': 'token ' + 'c20605ddc8cfd10d1e12a1c5e89315f0bf78b6db'}
  notfound = False
  fork = False
  okay = False
  repopath = r.split("https://github.com/")[1]
  path = "https://api.github.com/repos/" + repopath
  
  while(not fork and not okay and not notfound):
    response = requests.get(path, headers = myheaders)
    try:
      re = response.json()
      if "fork" in re:
        if re["fork"]:
          fork = True
        else:
          okay = True
      elif "message" in re and "Not Found" in re["message"]:
        notfound = True
      elif "message" in re and "API rate limit" in re["message"]:
        print("API rate limit. Sleep.")
        time.sleep(200)
    except:
      return False
  if fork:
    return True
  else:
    return False


def getChanges(rest):
  
  ### extracts the changes from the pure .diff file
  ### start by parsing the header of the diff
  
  changes = []
  while ("diff --git" in rest):
    filename = ""
    start = rest.find("diff --git")+1
    secondpart = rest.find("index")+1
    #get the title line which contains the file name
    titleline = rest[start:secondpart]
    if not (".py") in rest[start:secondpart]:
      # No python file changed in this part of the commit
      rest = rest[secondpart+1]
      continue
    if "diff --git" in rest[start:]:
      end = rest[start:].find("diff --git");
      filechange = rest[start:end]
      rest = rest[end:]
    else:
      end = len(rest)
      filechange = rest[start:end]
      rest = ""
    filechangerest = filechange
    
    
    while ("@@" in filechangerest):
      ### extract all singular changes, which are recognizable by the @@ marking the line number
      change = ""
      start = filechangerest.find("@@")+2
      start2 = filechangerest[start:start+50].find("@@")+2
      start = start+start2
      filechangerest=filechangerest[start:]
      
      if ("class" in filechangerest or "def" in filechangerest) and "\n" in filechangerest:
        filechangerest = filechangerest[filechangerest.find("\n"):]
      
      if "@@" in filechangerest:
          end = filechangerest.find("@@")
          change = filechangerest[:end]
          filechangerest = filechangerest[end+2:]
          
      else:
        end = len(filechangerest)
        change = filechangerest[:end]
        filechangerest = ""
        
      if len(change) > 0:
        changes.append([titleline,change])
  
  return changes
  
  
def getFilename(titleline):
  #extracts the file name from the title line of a diff file
  s = titleline.find(" a/")+2
  e = titleline.find(" b/")
  name = titleline[s:e]
  
  if titleline.count(name) == 2:
    return name
  elif ".py" in name and (" a"+name+" " in titleline):
    return name
  else:
    print("couldn't find name")
    print(titleline)
    print(name)
  
  
def makechangeobj(changething):
  #for a single change, consisting of titleline and raw code, create a usable object by extracting all relevant info
  
  change = changething[1]
  titleline = changething[0]
  
  if "<html" in change:
    return None
  
  if "sage:" in change or "sage :" in change:
    return None
  
  thischange = {}

  if myutils.getBadpart(change) is not None:      
    badparts = myutils.getBadpart(change)[0]
    goodparts = myutils.getBadpart(change)[1]
    linesadded = change.count("\n+")
    linesremoved = change.count("\n-")
    thischange["diff"] = change
    thischange["add"] = linesadded
    thischange["remove"] = linesremoved
    thischange["filename"] = getFilename(titleline)
    thischange["badparts"] = badparts
    thischange["goodparts"] = []
    if goodparts is not None:
      thischange["goodparts"] = goodparts
    if thischange["filename"] is not None:
      return thischange

  return None



#===========================================================================
# main 



#load list of all repositories and commits
with open('PyCommitsWithDiffs.json', 'r') as infile:
  data = json.load(infile)

now = datetime.now() # current date and time
nowformat = now.strftime("%H:%M")
print("finished loading ", nowformat)
                


progress = 0
changedict = {}



#default is sql
mode = "sql" 
if (len(sys.argv) > 1):
    mode = sys.argv[1]
  

for mode in ["remote_code_execution","redirect"]:
  
    if mode == "function_injection":
      allowedKeywords = ["function injection"]
    if mode == "remote_code_execution":
      allowedKeywords = ["remote code"]
    if mode == "cross_frame_scripting":
      allowedKeywords = ["cross frame"]
    if mode == "csv_injection":
      allowedKeywords = ["csv"]
    if mode == "redirect":
      allowedKeywords = ["redirect"]
    if mode == "hijack":
      allowedKeywords = ["session hijack","session fixation"]
    if mode == "command_injection":
      allowedKeywords = ["command injection"] 
    if mode == "sql":
      allowedKeywords = ["sql"] 
    if mode == "xsrf":
      allowedKeywords = ["xsrf","request forgery"] 
    if mode == "xss":
      allowedKeywords = ["xss", "cross site scripting","cross-site scripting"] 
    if mode == "replay_attack":
      allowedKeywords = ["replay attack"] 
    if mode == "unauthorized":
      allowedKeywords = ["unauthorized", "unauthorised"]
    if mode == "brute_force":
      allowedKeywords = ["brute force"]
    if mode == "flooding":
      allowedKeywords = ["flooding"]
    if mode == "remote_code_execution":
      allowedKeywords = ["remote code execution"]
    if mode == "formatstring":
      allowedKeywords = ["format string", "formatstring"]
    if mode == "session_fixation":
      allowedKeywords = ["fixation"]
    if mode == "cross_origin":
      allowedKeywords = ["cross origin"]
    if mode == "buffer overflow":
      allowedKeywords = ["buffer"]
    if mode == "cache":
      allowedKeywords = ["cache"]
    if mode == "eval":
      allowedKeywords = ["eval"]
    if mode == "csv":
      allowedKeywords = ["csv"]
    if mode == "path_disclosure":
      allowedKeywords = ["path"]
    if mode == "man-in-the-middle":
      allowedKeywords = ["man in the middle", "man-in-the-middle"]
    if mode == "smurf":
      allowedKeywords = ["smurf"]
    if mode == "tampering":
      allowedKeywords = ["tamper"]
    if mode == "sanitize":
      allowedKeywords = ["saniti"]
    if mode == "denial":
      allowedKeywords = ["denial"]
    if mode =="directory_traversal":
      allowedKeywords = ["directory","traversal"]
    if mode == "clickjack":
      allowedKeywords = ["clickjack", "click jack"]
    if allowedKeywords == "spoof":
      allowedKeywords = ["spoof"]

    #words that should not appear in the filename, because it's a sign that the file is actually part of a demo, a hacking tool or something like that
    suspiciouswords = ["injection", "vulnerability", "exploit", " ctf","capture the flag","ctf","burp","capture","flag","attack","hack"]

    #words that should not appear in the commit message
    badwords = ["sqlmap", "sql-map", "sql_map","ctf "," ctf"]

    progress = 0
    datanew = {}
    
    
    for r in data:

      progress = progress +1
      
      
      #check the repository name
      suspicious = False
      for b in badwords:
        if b.lower() in r.lower():
          suspicious = True
      if suspicious:
        continue


      
      
      
      if("anhday22" in r or "Chaser-wind" in r or "/masamitsu-murase" in r or "joshc/young-goons" in r or "notakang" in r or "sudheer628" in r or "mihaildragos" in r or "aselimov" in r or "tamhidat-api" in r or "aiden-law" in r or "sreeragvv" in r or "LaurenH1090" in r or "/matthewdenaburg1" in r or "haymanjoyce" in r or "/bloctavius" in r or "jordanott/No-Weight-Sharing" in r or "bvanseg" in r or  "sudoku-solver" in r or "tgbot" in r or "lluviaBOT" in r or "jumatberkah" in r or "luisebg" in r or "emredir" in r or "anhday22" in r or "faprioryan" in r or "pablogsal" in r or "zhuyunfeng111" in r or "bikegeek/METplus" in r or "chasinglogic" in r or "Sudhir0547" in r or "fyp_bot" in r):
        continue


      
    #  if checkFork(r):
    #    #print("FORK!")
    #    notrep_fork = notrep_fork + 1
    #    continue


      changesfromdiff = False
      all_irrelevant = True
      
      changeCommits = []
      for c in data[r]:
        
        #print(c)
        #get the info from the commits diff file - specifically the filesnames and badparts
        
        irrelevant = True
        for k in allowedKeywords:
          if k.lower() in data[r][c]["keyword"].lower():
#            print("\""+k.lower()+"\" is in " + data[r][c]["keyword"].lower())
            irrelevant = False

        if irrelevant:
          continue
        
        if not (".py" in data[r][c]["diff"]):
        # print(">no python file")
          continue    
        

      #  print("\n\n" + r + "/commit/" + c)
      #  print("Keyword: " + data[r][c]["keyword"])
        
        if not "message" in data[r][c]:
          data[r][c]["message"] = ""
        #else:
         # print(data[r][c]["message"].replace("\n"," ")[:100]+"...")

        
        if not c in changedict:
          changedict[c] = 0
        if c in changedict:
          changedict[c] = changedict[c] + 1
          if changedict[c] > 5:
#            print(" we already have more than five. Skip.")
            continue
        else:
          changedict[c] = 1
        
    #    duplicate = False
    #    for c2 in data[r]:
    #      if c != c2:
    #        if data[r][c]["diff"] == data[r][c2]["diff"]:
    #          #print("we already have that.")
    #          duplicate = True
    #    if duplicate:
    #      #print("duplicate")
    #      continue
        
        
        badparts = {}    
        changes = getChanges( data[r][c]["diff"])
        
        #if (len(changes) == 0):
          #print("no usable changes.")
        
        for change in changes:
          thischange = makechangeobj(change)

          if thischange is not None:
            if not "files" in data[r][c]:
              data[r][c]["files"] = {}
            f = thischange["filename"]
            
            if f is not None:
              suspicious = False
              for s in suspiciouswords:
                if s.lower() in f.lower():
                  #words should not appear in the filename
         #         print("suspicious word in filename: " + f)
                  suspicious = True
              
              if not suspicious:            
                if not f in data[r][c]["files"]:
                  data[r][c]["files"][f] = {}
                if not "changes" in data[r][c]["files"][f]:
                  data[r][c]["files"][f]["changes"] = []
                data[r][c]["files"][f]["changes"].append(thischange)
                changesfromdiff = True
                changeCommits.append(c)
          #else:
          #  print("thischange is none.")
            
     # print(changesfromdiff)
      if changesfromdiff:
          #now get the sourcecode!
          print("\n\n" + mode + "    mining "  + r + " " + str(progress) + "/" + str(len(data)))

          commitlist = []
          try:
            for commit in RepositoryMining(r).traverse_commits():
              commitlist.append(commit.hash)
              
              if not commit.hash in changeCommits:
                continue
              
              for m in commit.modifications:
                  
                  if m.old_path != None and m.source_code_before != None:
                    if not ".py" in m.old_path:
                      continue
                  
                    if len(m.source_code_before) > 30000:
                    # print(str(len(m.source_code_before)) + " is too long. " +r + "/commit/" + commit.hash + " " + m.old_path)
                      continue
                      
                    print("\n  modification with old path: " + str(m.old_path))
                    
                    for c in data[r]: 
                        if c == commit.hash:   
                          print("  found commit " + c)
                          
                          if not "files" in data[r][c]:
                            print("  no files :(")
                            
                          data[r][c]["msg"] = commit.msg
                          for badword in badwords:
                            if badword.lower() in commit.msg.lower():
                              suspicious = True
                          
                          if suspicious:
                            print("  suspicious commit msg: \"" + commit.msg.replace("\n"," ")[:300] + "...\"")
                            continue
                          
                          print("  The commit has " + str(len(data[r][c]["files"])) + " files.")
                          for f in data[r][c]["files"]:
                              #print("    File " + f +  " with " + str(len(data[r][c]["files"][f]["changes"])) + " changes")
                              
                              
                              
                              if m.old_path in f:
                                
                                
                                
                                if not ("source" in data[r][c]["files"][f] and (len(data[r][c]["files"][f]["source"])> 0)):
                                  sourcecode = "\n" + myutils.removeDoubleSeperatorsString(myutils.stripComments(m.source_code_before))
                                  data[r][c]["files"][f]["source"] = sourcecode
                                
                                if not ("sourceWithComments" in data[r][c]["files"][f] and (len(data[r][c]["files"][f]["sourceWithComments"])> 0)):
                                  data[r][c]["files"][f]["sourceWithComments"] = m.source_code_before
                                
                                if not ("sourceWithComments" in data[r][c]["files"][f] and (len(data[r][c]["files"][f]["sourceWithComments"])> 0)):
                                  data[r][c]["files"][f]["sourcecodeafter"] = ""
                                  if m.source_code is not None:
                                    data[r][c]["files"][f]["sourcecodeafter"] = m.source_code   
                                
                                if not r in datanew:
                                  datanew[r] = {}
                                if not c in datanew[r]:
                                  datanew[r][c] = {}
                                  
                                datanew[r][c] = data[r][c]
                                print("     ->> added to the dataset.")
                                #print("         now there are " + str(len(datanew[r][c]["files"])))
                                  
          except Exception as e:
              print("Exception occured.")
              print(e)
              time.sleep(2)
              continue
          # print(commitlist)
            
        #                          print("added to datanew, has " + str(len(blocks)) + " blocks.")




    print("done.")



    print(len(data))  
        
    with open('data/plain_' + mode, 'w') as outfile:
      json.dump(datanew, outfile)


      
      
