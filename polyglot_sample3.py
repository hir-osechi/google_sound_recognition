#!/usr/bin/env python
# -*- coding:utf-8 -*-
from polyglot.detect import Detector
from polyglot.text import Text
import os
from espeak import espeak
from subprocess import call
from pocketsphinx import LiveSpeech

#t = "Hi ! My favorite food is apple!"
#tokens = Text(t)
#for token in tokens.pos_tags:
#    print(token)

qa_dict = {} 
import math
import sys

args = sys.argv

#t = args[1]
for phrase in LiveSpeech():
	print(phrase)
	t = phrase
	t = str(t)
	with open('../data/q_list2.txt', 'r') as f: 
            qa_list = f.readlines()
        for qa in qa_list:
            qa = qa.rstrip().split(',') 
            qa_dict[qa[0]] = qa[1] 

        tokens = Text(t)
        list1 = []
        #for token in t.tokenize(text): 
	        #print token
        for token in tokens.pos_tags:
            #print(token)
	    if u'NOUN' in token:
  		list1.append(token[0])
	    elif u'ADJ' in token:
  		list1.append(token[0])
	    elif u'VERB' in token:
  		list1.append(token[0])

        def calc_cos(A,B):
	    lengthA = math.sqrt(len(A))
	    #print len(A)
	    lengthB = math.sqrt(len(B))
	    #print len(B)
	    match = 0.0 
       	    for a in A:
		if a in B:
		    match += 1
		    #print match
	    cos = match/(lengthB*lengthA)
	    return cos

        i = 0
        max = 0
        for qa in qa_dict.keys():
	    listi = []
	    for token in Text(qa_dict.keys()[i]).pos_tags:
		if u'NOUN' in token:
	            listi.append(token[0])
		elif u'ADJ' in token:
  		    listi.append(token[0])
		elif u'VERB' in token:
  	            listi.append(token[0])	
	    cosAB = calc_cos(listi,list1)
	    #print cosAB
	    #print listi
	    if cosAB > max:
		max = cosAB
                text = qa_dict.keys()[i]
	    i += 1
        if max > 0.25:
	    print(max)
	    print(qa_dict[text])
	    espeak.synth(qa_dict[text] )
            speech=qa_dict[text]
            call(["espeak",speech])
        else:
	    print("I don't have answers. ")
	    speech="I don't have answers. "
            call(["espeak",speech])
