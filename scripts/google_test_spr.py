#!/usr/bin/env python3                                                                                
# -*- coding:utf-8 -*-

import speech_recognition as sr  
from polyglot.text import Text
from subprocess import call
import math


while 1:
	try:
		qa_dict = {}
		with open('english.txt', 'r') as f: 
				qa_list = f.readlines()
				for qa in qa_list:
					qa = qa.rstrip().split(',') 
					qa_dict[qa[0]] = qa[1]
					
		# get audio from the microphone                                                                       
		r = sr.Recognizer()
		mic = sr.Microphone()                                                                               
		with mic as source:  
			r.adjust_for_ambient_noise(source)                                                                     
			print("tell me your question:")                                                                                   
			audio = r.listen(source)  
			question = r.recognize_google(audio) 
			t = question
			print("\n-------your question--------\n",question,"\n----------------------------\n")
			tokens = Text(t)
			list1 = []
			#for token in t.tokenize(text): 
				#print token
			for token in tokens.pos_tags:
				#print(token)
				#特定の品詞のみ抽出
				"""
				if u'NOUN' in token:
			  		list1.append(token[0])
				elif u'ADJ' in token:
			  		list1.append(token[0])
				elif u'VERB' in token:
			  		list1.append(token[0]) 
			  	"""
				list1.append(token[0])
			  	#print list1

			def calc_cos(A,B):
				lengthA = math.sqrt(len(A))
				lengthB = math.sqrt(len(B))
				match = 0
				for a in A:
					if a in B:
						match += 1
				
				if (lengthA != 0 and lengthB != 0):
					cos = match/(lengthB*lengthA)
				else:cos = match/100        #とりあえずcosを小さくする

				return cos

			i = 0
			max = 0
			keys = []
			for qa in qa_dict.keys():
				keys.append(qa)
				listi = []
				#print(keys)
				for token in Text(keys[i]).pos_tags:
					"""
					if u'NOUN' in token:
						listi.append(token[0])
					elif u'ADJ' in token:
						listi.append(token[0])
					elif u'VERB' in token:
						listi.append(token[0]) 
					"""
					listi.append(token[0])
				cosAB = calc_cos(listi,list1)
				#print cosAB
				#print(listi)
				if cosAB > max:
					max = cosAB
					question = keys[i]
				i += 1
			if max > 0.5:
				#print(max)
				print("\n-----------answer-----------\n",qa_dict[question],"\n----------------------------\n")
				call(["espeak",qa_dict[question]])
			else:
				responce = "I don't have answers. "
				print(responce)
				#call(["espeak",responce])
			

	except sr.UnknownValueError:
		print("Could not understand audio")
	except sr.RequestError as e:
		print("Could not request results; {0}".format(e))
