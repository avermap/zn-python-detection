
import time
import sys
import json
#import StringIO
from io import StringIO
import subprocess
import time
import bs4 as bs  
import urllib.request  
import re  
import nltk
from gensim.models import Word2Vec, KeyedVectors
import numpy
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
from tokenizer import tokenize
import builtins
import keyword
import pickle
from keras import backend as K
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.utils import class_weight
import numpy as np
import keras.backend as K
from termcolor import colored
import time
import sys
import json
#import StringIO
#from io import StringIO
import subprocess
from datetime import datetime
import bs4 as bs  
import urllib.request  
import re  
import nltk
import builtins
import requests 
import keyword
from random import shuffle
import random
import pickle
from pydriller import RepositoryMining
from gensim.models import Word2Vec, KeyedVectors


import json
import numpy
import pickle
from pydriller import RepositoryMining
from gensim.models import Word2Vec, KeyedVectors
from keras.preprocessing import sequence
from keras.models import load_model
import sys
import time

import tensorflow as tf

from sklearn.metrics import f1_score
import keras.backend as K
from termcolor import colored
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

nice = ["derilinx/ckan-docker-public", "onewyoming/onewyoming", "paulc1600/DB-API-Forum", "/MrCirca/scripts", "/JeremiahO/crimemap", "kayfay/python-flask-crime-map" ]
cutoff = 0.5

def f1(y_true, y_pred):
    y_pred = K.round(y_pred)
    tp = K.sum(K.cast(y_true*y_pred, 'float'), axis=0)
    tn = K.sum(K.cast((1-y_true)*(1-y_pred), 'float'), axis=0)
    fp = K.sum(K.cast((1-y_true)*y_pred, 'float'), axis=0)
    fn = K.sum(K.cast(y_true*(1-y_pred), 'float'), axis=0)

    p = tp / (tp + fp + K.epsilon())
    r = tp / (tp + fn + K.epsilon())

    f1 = 2*p*r / (p+r+K.epsilon())
    f1 = tf.where(tf.is_nan(f1), tf.zeros_like(f1), f1)
    return K.mean(f1)

def f1_loss(y_true, y_pred):
    
    tp = K.sum(K.cast(y_true*y_pred, 'float'), axis=0)
    tn = K.sum(K.cast((1-y_true)*(1-y_pred), 'float'), axis=0)
    fp = K.sum(K.cast((1-y_true)*y_pred, 'float'), axis=0)
    fn = K.sum(K.cast(y_true*(1-y_pred), 'float'), axis=0)

    p = tp / (tp + fp + K.epsilon())
    r = tp / (tp + fn + K.epsilon())

    f1 = 2*p*r / (p+r+K.epsilon())
    f1 = tf.where(tf.is_nan(f1), tf.zeros_like(f1), f1)
    return 1 - K.mean(f1)
  

  

def predict(vectorlist): 
  
  if (len(vectorlist) > 0):
    one = []
    one.append(vectorlist)
    one = numpy.array(one)
    max_length = 200
    one = sequence.pad_sequences(one, maxlen=max_length)
    yhat_probs = model.predict(one, verbose=0)
    prediction = int(yhat_probs[0][0] * 100000)
    prediction = 0.00001 * prediction 
    return prediction
  else:
    return -1




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
   
    
#  while ('r"""') in change:
#    position1 = change.find('"""')
#    before = change[:position1]
#    if change[position1+4:].find('"""') == -1:
#      change = before  
#    else:
#      position2 = change[position1+4:].find('"""')+position1+8
#      after = change[position2:]
#      change = before+after
  
#  while ('"""') in change:
#    position1 = change.find('"""')
#    before = change[:position1]
#    if change[position1+3:].find('"""') == -1:
#      change = before  
#    else:
#      position2 = change[position1+3:].find('"""')+position1+7
#      after = change[position2:]
#      change = before+after
#    
#  while ("'''") in change:
#    position1 = change.find("'''")
#    before = change[:position1]
#    if change[position1+3:].find("'''") == -1:
#      change = before  
#    else:
#      position2 = change[position1+3:].find("'''")+position1+7
#      after = change[position2:]
#      change = before+after
  
  withoutComments = change

  return withoutComments




  
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
  




def getBadpart(change):
  
  #print("\n")
  removal = False
  lines = change.split("\n")
  
#  if (len(lines) > 10 and len(change) > 800):
   # print("tooo long")
#    return None
  
  
  
  for l in lines:
    if len(l) > 0:
      if l[0] == "-":
        #print("a line is removed")
        removal = True
      
  
  if not removal:
    #print("There is no removal.")
    return None
  
  
  
 # print(change)
 # time.sleep(5)
  
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



def getblocksVisual(r,c,sourcecode, badpositions,commentareas, fulllength,step, nr,w2v_model):
  
  
      ypos = 0
      xpos = 0
      lines = (sourcecode.count("\n"))
      #print("lines: " + str(lines))
      img = Image.new('RGB', (2000, 11*(lines+1)))
      color = "white"
      
      
          
      
      
      
      blocks = []
       
      focus = 0
      lastfocus = 0
      
      string = ""
      
      trueP = False
      falseP = False
      
      while (True):
        if focus > len(sourcecode):
          break
        
        
        
        comment = False
        for com in commentareas:
          
          if (focus >= com[0] and focus <= com[1] and lastfocus >= com[0] and lastfocus < com[1]):
                focus = com[1]
                #print("within")
                comment = True
          if (focus > com[0] and focus <= com[1] and  lastfocus < com[0]):
              focus = com[0]
              #print("before")
              comment = False                   
          elif (lastfocus >= com[0] and lastfocus < com[1] and focus > com[1]):
              focus = com[1]
              #print("up to the end")
              comment = True
      
        #print([lastfocus,focus,comment, "["+sourcecode[lastfocus:focus]+"]"])
        focusarea = sourcecode[lastfocus:focus]
     
        if(focusarea == "\n"):
          string = string + "\n"
          
        else:
          if comment:
              color = "grey"
              string = string + colored(focusarea,'blue')
          else:
              
              
              middle = lastfocus+round(0.5*(focus-lastfocus))              
              context = getcontextPos(sourcecode,middle,fulllength)
              
              
              if context is not None:
              
                vulnerablePos = False
                for bad in badpositions:
                    if (context[0] > bad[0] and context[0] <= bad[1]) or (context[1] > bad[0] and context[1] <= bad[1]) or (context[0] <= bad[0] and context[1] >= bad[1]):
                      vulnerablePos = True
                      
                predictionWasMade = False
                text = sourcecode[context[0]:context[1]].replace("\n", " ")
                token = getTokens(text)
                if (len(token) > 1):                  
                  vectorlist = []                  
                  for t in token:
                    if t in word_vectors.vocab and t != " ":
                      vector = w2v_model[t]
                      vectorlist.append(vector.tolist())   
                      
                  if len(vectorlist) > 0:
                      p = predict(vectorlist)
                      if p >= 0:
                        predictionWasMade = True
                        
                      #  print(p)
                        if vulnerablePos:
                          if p > 0.5:
                            color = "royalblue"
                            string = string + colored(focusarea,'cyan')
                          else:
                            string = string + colored(focusarea,'magenta')
                            color = "violet"
                            
                        else:
                          
                        
                          if p > 0.9:
                            color = "darkred"
                          elif p > 0.8:
                            color = "red"
                          elif p > 0.7:
                            color = "darkorange"
                          elif p > 0.8:
                            color = "orange"
                          elif p > 0.5:
                            color = "gold"
                          elif p > 0.4:
                            color = "yellow"
                          elif p > 0.3:
                            color = "GreenYellow"
                          elif p > 0.2:
                            color = "LimeGreen"
                          elif p > 0.1:
                            color = "Green"
                          else:
                            color = "DarkGreen"
                
                          if p > 0.8:
                            string = string + colored(focusarea,'red')
                          elif p > 0.5:
                            string = string + colored(focusarea,'yellow')
                          else:
                            string = string + colored(focusarea,'green')
                            
                if not predictionWasMade:
                  string = string + focusarea
              else:
                string = string + focusarea
                
        
        
            
        try:
          if len(focusarea) > 0:
            d = ImageDraw.Draw(img)
#            print(list(focusarea))
            if focusarea[0] == "\n":
              ypos = ypos + 11
              xpos = 0
              d.text((xpos, ypos), focusarea[1:], fill=color)
              xpos = xpos + d.textsize(focusarea)[0]
            else:
              d.text((xpos, ypos), focusarea, fill=color)
              xpos = xpos + d.textsize(focusarea)[0]

        except Exception as e:
          o = 1
          #print(e)
#        ypos = ypos + 15
        
        

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

      
      #print("=============================")
      
      print(string)
      #img.save("images/" + mode + "/" + str(nr) + ".png")    
      return blocks


  
  

def findComments(sourcecode):
  commentareas = []
  
  inacomment = False
  bigcomment = False
  bigcomment2 = False
  commentstart = -1
  commentend = -1
  bigcommentstart = -1
  bigcommentend = -1
  bigcomment2start = -1
  bigcomment2end = -1
  
  
  for pos in range(len(sourcecode)):
    if sourcecode[pos] == "#":
      if not inacomment:
        commentstart = pos 
        inacomment = True
    
    if sourcecode[pos] == "\n":
      if inacomment:
        commentend = pos
        inacomment = False
    
    if commentstart >= 0 and commentend >= 0:
      t = [commentstart, commentend]
      commentareas.append(t)
      commentstart = -1
      commentend = -1

 #   if sourcecode[pos] == "'":      
 #     if pos < len(sourcecode) + 2:
 #       if sourcecode[pos+1] == "'" and sourcecode[pos+2] == "'":
 #         if not bigcomment:
 #           bigcomment = True
 #           bigcommentstart = pos 
 #         else:
 #           bigcomment = False
 #           bigcommentend = pos+3
 #   if bigcommentstart > 0 and bigcommentend > 0:
 #     t = [bigcommentstart, bigcommentend]
 #     commentareas.append(t)
 #     bigcommentstart = -1
 #     bigcommentend = -1#
#
#    if sourcecode[pos] == '"':      
#      if pos < len(sourcecode) + 2:
#        if sourcecode[pos+1] == '"' and sourcecode[pos+2] == '"':
#          if not bigcomment2:
#            bigcomment2 = True
#            bigcomment2start = pos 
#          else:
#            bigcomment2 = False
#            bigcomment2end = pos+3
#    if bigcomment2start > 0 and bigcomment2end > 0:
#      t = [bigcomment2start, bigcomment2end]
#      commentareas.append(t)
#      bigcomment2start = -1
#      bigcomment2end = -1

  return commentareas





#==========================================================================================================



mode = "sql"
nr = "1"

if (len(sys.argv) > 1):
  mode = sys.argv[1]
  if len(sys.argv) > 2:
    nr = sys.argv[2]

mode2 = mode + nr

now = datetime.now() # current date and time
nowformat = now.strftime("%H:%M")
print("time:", nowformat)


mincount = 10
iterationen = 300
s = 200
w2v = "word2vec_"+"withString"+str(mincount) + "-" + str(iterationen) +"-" + str(s)
w2vmodel = "w2v/" + w2v + ".model"
w2v_model = Word2Vec.load(w2vmodel)
word_vectors = w2v_model.wv
                
model = load_model('model/LSTM'+mode+'.h5',custom_objects={'f1_loss': f1_loss, 'f1':f1})



with open('examples/'+mode+"-"+nr+".py", 'r') as infile:
  sourcecodefull = infile.read()


commentareas = findComments(sourcecodefull)
getblocksVisual("","",sourcecodefull, [], commentareas, 200,5, 0, w2v_model)

