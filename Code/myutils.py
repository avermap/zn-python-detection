from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import LSTM
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.models import load_model
from keras.layers.embeddings import Embedding
from keras.layers import Bidirectional
from keras.preprocessing import sequence
from keras import backend as K
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.utils import class_weight
import tensorflow as tf
import builtins
import keyword
import pickle
from gensim.models import Word2Vec, KeyedVectors


def findposition(badpart,sourcecode):
  splitchars = ["\t", "\n", " ", ".", ":", "(", ")", "[", "]", "<", ">", "+", "-", "=","\"", "\'","*", "/","\\","~","{","}","!","?","*",";",",","%","&"]
  pos = 0
  matchindex = 0
  inacomment = False
  bigcomment = False
  bigcomment2 = False
  startfound = -1
  endfound = -1
  position = []
  end = False
  last = 0
  
  while "#" in badpart:
    f = badpart.find("#")
    badpart = badpart[:f]

  b = badpart.lstrip()
  if len(b) < 1:
  #  print(b)
  #  print("nope.\n\n")
    return[-1,-1]


  while(not end):
    #print("position : " + str(pos))
    
    if not inacomment:
      last = pos-1
    
    if pos >= len(sourcecode):
      end = True
      break
    
    if sourcecode[pos] == "\n":
 #     print("end of comment")
 #     print("[" + sourcecode[last]+ "]")
      inacomment = False
      
    if sourcecode[pos] == "\n" and (sourcecode[pos-1] == "\n" or sourcecode[last] == " "):
      #print("one further")
      pos = pos +1
      continue
      
    if sourcecode[pos] == " " and (sourcecode[pos-1] == " " or sourcecode[last] == "\n"):
     # print("one further")
      pos = pos +1
      continue
      
    if sourcecode[pos] == "#":
      
      inacomment = True
      

#    if sourcecode[pos] == "'":      
#      if pos+2 < len(sourcecode):
#        if sourcecode[pos+1] == "'" and sourcecode[pos+2] == "'":
#          if not bigcomment:
#            pos = pos+3
#            bigcomment = True
#        #    print(">>> BIGCOMMENT")
#            continue
#          else:
#            pos = pos+3
#            bigcomment = False
#         #   print(">>> BIGCOMMENT END")
#            continue

#    if sourcecode[pos] == '"':      
#      if pos+2 < len(sourcecode):
#        if sourcecode[pos+1] == '"' and sourcecode[pos+2] == '"':
#          if not bigcomment2:
#            pos = pos+3
#            bigcomment2 = True
#          #  print(">>> BIGCOMMENT")
#            continue
#          else:
#            pos = pos+3
#            bigcomment2 = False
#           # print(">>> BIGCOMMENT END")
#            continue
      
    if (False):
      
                      print("---------------------------------")
                      string1 = ""
                      string2 = ""
                      for i in range(0,pos):
                        string1 = string1 + sourcecode[i]

                      for i in range(pos+1,len(sourcecode)):
                        string2 = string2 + sourcecode[i]
                        
                      print(string1 + "[" + sourcecode[pos] + "]" + string2)
                      print("---------------------------------")


                      string1 = ""
                      string2 = ""
                      
                      for i in range(0,matchindex):
                        string1 = string1 + badpart[i]

                      for i in range(matchindex+1,len(badpart)):
                        string2 = string2 + badpart[i]
                        
                      print(string1 + "[" + badpart[matchindex] + "]" + string2)
  
                      print("---------------------------------")
                

    if not inacomment: # and not bigcomment and not bigcomment2:
      a = sourcecode[pos]
      if a == "\n":
        a = " "
      b = badpart[matchindex]
      
      c = ""
      if matchindex > 0:
        c = badpart[matchindex-1]
      
      d = ""
      if matchindex < len(badpart)-2:
        d = badpart[matchindex+1]
        
      if (a != b) and (a == " " or a == "\n") and ((b in splitchars) or (c in splitchars)):
        pos = pos+1
        continue
      
      if (a != b) and (b == " " or b == "\n"):
        #print("here")
        if (c in splitchars or d in splitchars):
          #print("here2")
          if (matchindex < len(badpart)-1):
            matchindex = matchindex + 1
            continue
        
      if a == b:
          if matchindex == 0:
            startfound = pos
         # print("\n>>match: " + badpart[matchindex] + "(" + str(matchindex) + "/" + str(len(badpart)) + ")\n\n")
          matchindex = matchindex + 1
          
      else:
          #print("\n>>no match" )
          matchindex = 0
          startfound = -1
        
      if matchindex == len(badpart):
        endfound = pos
    #    print("FOUND at pos "+ str(startfound) + ":" + str(endfound))
        break
        
    if pos == len(sourcecode):
      end = True
    pos = pos + 1
  
  position.append(startfound)
  position.append(endfound)
  
  if endfound < 0:
    startfound = -1
    
  if endfound < 0 and startfound < 0: #and not "#" in badpart and not '"""' in badpart and not "'''" in badpart:
#    print(sourcecode)
#    print(":::::::::::")
#    print(badpart)
#    print("-----------------")
    return[-1,-1]
  return position




def findpositions(badparts,sourcecode):
  
  positions = []
  
  
  for bad in badparts:
    
    if "#" in bad:
      find = bad.find("#")
      bad = bad[:find]
      
    place = findposition(bad,sourcecode)
    if place != [-1,-1]:
      positions.append(place)
    
    
  return positions
  








def nextsplit(sourcecode,focus):
  splitchars = [" ","\t","\n", ".", ":", "(", ")", "[", "]", "<", ">", "+", "-", "=","\"", "\'","*", "/","\\","~","{","}","!","?","*",";",",","%","&"]
  for pos in range(focus+1, len(sourcecode)):
      if sourcecode[pos] in splitchars:
        return pos
  return -1

def previoussplit(sourcecode,focus):
  splitchars = [" ","\t","\n", ".", ":", "(", ")", "[", "]", "<", ">", "+", "-", "=","\"", "\'","*", "/","\\","~","{","}","!","?","*",";",",","%","&"]
  pos = focus-1
  while(pos >= 0):
      if sourcecode[pos] in splitchars:
        return pos
      pos = pos-1
  return -1

def getcontextPos(sourcecode,focus,fulllength):

  
  startcontext = focus
  endcontext = focus
  if focus > len(sourcecode)-1:
    return None

  start = True
  
      
  while not len(sourcecode[startcontext:endcontext]) > fulllength:
   # print(str(startcontext) + ":" + str(endcontext))
   # print(len(sourcecode[startcontext:endcontext]))
    
    if previoussplit(sourcecode,startcontext) == -1 and nextsplit(sourcecode,endcontext) == -1:
   #   print("NONE!")
      return None
    
    if start:
      if previoussplit(sourcecode,startcontext) > -1:
        startcontext = previoussplit(sourcecode,startcontext)
      #print("new start: " + str(startcontext))
      start = False
    else:
      if nextsplit(sourcecode,endcontext) > -1:
        endcontext = nextsplit(sourcecode,endcontext)
      #print("new end: " + str(endcontext))
      start = True

        
#  print("focus: " + str(focus))
#  print("start: " + str(startcontext))
#  print("end: " + str(endcontext))
  return [startcontext,endcontext]

def getcontext(sourcecode,focus,fulllength):

  
  startcontext = focus
  endcontext = focus
  if focus > len(sourcecode)-1:
    return None

  start = True
  
      
  while not len(sourcecode[startcontext:endcontext]) > fulllength:
   # print(str(startcontext) + ":" + str(endcontext))
   # print(len(sourcecode[startcontext:endcontext]))
    
    if previoussplit(sourcecode,startcontext) == -1 and nextsplit(sourcecode,endcontext) == -1:
   #   print("NONE!")
      return None
    
    if start:
      if previoussplit(sourcecode,startcontext) > -1:
        startcontext = previoussplit(sourcecode,startcontext)
      #print("new start: " + str(startcontext))
      start = False
    else:
      if nextsplit(sourcecode,endcontext) > -1:
        endcontext = nextsplit(sourcecode,endcontext)
      #print("new end: " + str(endcontext))
      start = True

        
#  print("focus: " + str(focus))
#  print("start: " + str(startcontext))
#  print("end: " + str(endcontext))
  return sourcecode[startcontext:endcontext]
  











def getblocks(sourcecode, badpositions, step, fulllength):
      blocks = []
       
      focus = 0
      lastfocus = 0
      while (True):
        if focus > len(sourcecode):
          break
        
        focusarea = sourcecode[lastfocus:focus]
                
        if not (focusarea == "\n"):
              
            middle = lastfocus+round(0.5*(focus-lastfocus))              
            context = getcontextPos(sourcecode,middle,fulllength)
            #print([lastfocus,focus,len(sourcecode)])
            
            
            if context is not None:
              
              
                
              vulnerablePos = False
              for bad in badpositions:
                    
                  if (context[0] > bad[0] and context[0] <= bad[1]) or (context[1] > bad[0] and context[1] <= bad[1]) or (context[0] <= bad[0] and context[1] >= bad[1]):
                    vulnerablePos = True
            
                  
              q = -1
              if vulnerablePos:
                q = 0
              else:
                q = 1
              
              
              singleblock = []
              singleblock.append(sourcecode[context[0]:context[1]])
              singleblock.append(q)
                
              already = False
              for b in blocks:
                if b[0] == singleblock[0]:
                #  print("already.")
                  already = True
                  
              if not already:
                blocks.append(singleblock)


        if ("\n" in sourcecode[focus+1:focus+7]):
          lastfocus = focus
          focus = focus + sourcecode[focus+1:focus+7].find("\n")+1
        else:
          if nextsplit(sourcecode,focus+step) > -1:
            lastfocus = focus
            focus = nextsplit(sourcecode,focus+step)
          else:
            if focus < len(sourcecode):
              lastfocus = focus
              focus = len(sourcecode)
            else:
              break

      
      return blocks




def getBadpart(change):
  
  #print("\n")
  removal = False
  lines = change.split("\n")
  for l in lines:
    if len(l) > 0:
      if l[0] == "-":
        #print("a line is removed")
        removal = True
      
  
  if not removal:
    #print("There is no removal.")
    return None
  
  pairs = []
  
  badexamples = []
  goodexamples = []

  for l in range(len(lines)):
    
    line = lines[l]
    line = line.lstrip()
    if len(line.replace(" ","")) > 1:
        if line[0] == "-":
          if not "#" in line[1:].lstrip()[:3] and not "import os" in line:
            badexamples.append(line[1:])
        if line[0] == "+":
          if not "#" in line[1:].lstrip()[:3] and not "import os" in line:
            goodexamples.append(line[1:])
    
  if len(badexamples) == 0:
#    print("removed lines were empty or comments")
    return None
  
  return [badexamples,goodexamples]
    


  

def getTokens(change):
  tokens = []  
  
  change = change.replace(" .",".")
  change = change.replace(" ,",",")
  change = change.replace(" )",")")
  change = change.replace(" (","(")
  change = change.replace(" ]","]")
  change = change.replace(" [","[")
  change = change.replace(" {","{")
  change = change.replace(" }","}")
  change = change.replace(" :",":")
  change = change.replace("- ","-")
  change = change.replace("+ ","+")
  change = change.replace(" =","=")
  change = change.replace("= ","=")
  splitchars = [" ","\t","\n", ".", ":", "(", ")", "[", "]", "<", ">", "+", "-", "=","\"", "\'","*", "/","\\","~","{","}","!","?","*",";",",","%","&"]
  start = 0
  end = 0
  for i in range(0, len(change)):
    if change[i] in splitchars:
      if i > start:
        start = start+1
        end = i
        if start == 1:
          token = change[:end]
        else:
          token = change[start:end]
        if len(token) > 0:
          tokens.append(token)
        tokens.append(change[i])
        start = i
  return(tokens)
  



def removeDoubleSeperatorsString(string):
  return ("".join(removeDoubleSeperators(getTokens(string))))







def removeDoubleSeperators(tokenlist):
    last = ""
    newtokens = []
    for token in tokenlist:
      if token == "\n":
        token = " "
      if len(token) > 0:
        if ((last == " ") and (token == " ")):
          o = 1 #noop
          #print("too many \\n.")
        else:
          newtokens.append(token)
          
        last = token
        
    return(newtokens)
  
  
def isEmpty(code):
  token = getTokens(stripComments(code))
  for t in token:
    if (t != "\n" and t != " "):
      return False
  return True

def is_builtin(name):
    return name in builtins.__dict__
def is_keyword(name):
      return name in keyword.kwlist



def removeTripleN(tokenlist):
    secondlast = ""
    last = ""
    newtokens = []
    for token in tokenlist:
      if len(token) > 0:
        
        if ((secondlast == "\n") and (last == "\n") and (token == "\n")):
          #print("too many \\n.")
          o = 1 #noop
        else:
          newtokens.append(token)
          
        
        thirdlast = secondlast
        secondlast = last
        last = token
        
    return(newtokens)
  
  



def getgoodblocks(sourcecode,goodpositions,fullength):
  blocks = []
  if (len(goodpositions) > 0):
    for g in goodpositions:
     # print("g " + str(g))
      if g != []:
        focus = g[0]
        while (True):
          if focus >= g[1]:
            #print("  too far.")
            break

    #        print("Focus is on " + str(focus) + " " + sourcecode[focus])
            
          
          context = getcontext(sourcecode,focus,fulllength)
          
          if context is not None:
            singleblock = []
            singleblock.append(context)
            singleblock.append(1)
              
            already = False
            for b in blocks:
              if b[0] == singleblock[0]:
              #  print("already.")
                already = True
                  
            if not already:
              blocks.append(singleblock)
              
              
            if nextsplit(sourcecode,focus+15) > -1:
              focus = nextsplit(sourcecode,focus+15)
            else:
              break
      
#  if len(blocks) > 0:
#    print(blocks)
  return blocks




def stripComments(code):
    
  withoutComments = ""
  lines = code.split("\n")
  withoutComments = ""
  therewasacomment = False
  for c in lines:
    if "#" in c:
      therewasacomment = True
      position = c.find("#")
      c = c[:position]
    withoutComments = withoutComments + c + "\n"
  
  
  change = withoutComments
  
  withoutComments = change

  return withoutComments



