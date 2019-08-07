#!/usr/bin/env python3                                                                                
# -*- coding:utf-8 -*-
import csv
import speech_recognition as sr  
from polyglot.text import Text
from subprocess import call
import math
from nltk.corpus import wordnet

def exchanger(list1,list2,max_sim,part): #list1とlist2内の特定の単語の類似度がmより大きいとき、単語を入れ替える関数（聞かれた質問がlist1,用意した質問がlist2）
	max = 0
	i = 0
	global a
	a = [0]*len(list1)   #リストの長さを指定
	while i < len(list1):
		for word2 in list2:
			#print("=================")
			#print("聞かれた質問内の"+str(i+1)+"番目の"+part+"："+list1[i])
			#print("用意した質問内の各"+part+"："+word2)
			#print("=================")
			word2 = word2.lower()
			list1[i] = list1[i].lower()
			if list1[i] == "do" or list1[i] == "doing" or list1[i] == "did":
				a[i] = list1[i]
			else:
				if word2 != "do" and word2 != "doing" and word2 != "did":
					syns1 = wordnet.synsets(list1[i])
					syns2 = wordnet.synsets(word2)		
					for sense1 in syns1:
						for sense2 in syns2:
							sim = wordnet.wup_similarity(sense1, sense2)
							if sim != None:
								if max<sim:
									max = sim
									#print max
									if max>=max_sim:
										#print "類似度："+str(max)
										a[i] = word2
									else:a[i] = list1[i]
						
		#print "聞かれた質問の"+str(i+1)+"番目の動詞(とか):"+a[i].encode('utf-8')			
		max = 0					
		i += 1
	#以下２行でlist1=aとしたい
	list1.clear()
	list1.extend(a)
	#print(list1)

def calc_cos(A,B): #2つのリストのコサイン類似度を求める関数
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
	
'''def text_to_list(text,list_n,list_adj,list_v): #3つの品詞-のみ-を別々に抽出する関数
	for token in Text(text).pos_tags:
		#print(token)
		#特定の品詞のみ抽出
		if u'NOUN' in token:
	  		list_n.append(token[0])
		elif u'ADJ' in token:
	  		list_adj.append(token[0])
		elif u'VERB' in token:
	  		list_v.append(token[0])
	  	elif u'AUX' in token:
			list_v.append(token[0]) '''
def text_to_list(text,list_n,list_adj,list_v,list_other): #3つの品詞-とその他の品詞-を別々に抽出する関数
	for token in Text(text).pos_tags:
		#print(token)
		#特定の品詞のみ抽出
		if u'NOUN' in token:
	  		list_n.append(token[0])
		elif u'ADJ' in token:
	  		list_adj.append(token[0])
		elif u'VERB' in token:
	  		list_v.append(token[0]) 
		elif u'AUX' in token:
			list_v.append(token[0]) 
		else:list_other.append(token[0])
while 1:
	try:
		qa_dict = {}
		with open('../data/q&a.csv', 'r') as f: 
			for line in csv.reader(f):
				qa_dict.setdefault(str(line[0]), str(line[1]))
					
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

				#以下、list_品詞
				list1 = []
				list_n = []
				list_adj = []
				list_v = []
				list_other = []
				listi = []
				listi_n = []
				listi_adj = []
				listi_v = []
				listi_other = []
					
				#text_to_list(question,list_n,list_adj,list_v)
				#text_to_list(keys[i],listi_n,listi_adj,listi_v)
				text_to_list(question,list_n,list_adj,list_v,list_other)
				text_to_list(keys[i],listi_n,listi_adj,listi_v,listi_other)
				exchanger(list_n,listi_n,1.0,"名詞")
				exchanger(list_adj,listi_adj,0.75,"形容詞")
				exchanger(list_v,listi_v,0.75,"動詞")
				
				list1 = list_n+list_adj+list_v+list_other
				listi = listi_n+listi_adj+listi_v+listi_other

				cosAB = calc_cos(listi,list1)
				#print cosAB
				
				if cosAB > max:
					max = cosAB
					final_question = keys[i]
					final_listi=listi
				i += 1
			if max > 0.5:
				#print(max)
				#print(list1)
				#print(final_listi)
				print("\n-----------answer-----------\n",qa_dict[final_question],"\n----------------------------\n")
				if qa_dict[final_question] == "Ri-one":
					call(["espeak","Re-one"])
				else:call(["espeak",qa_dict[final_question]])
				
			else:
				responce = "I don't have answers. "
				print(responce)
				#call(["espeak",responce])
			

	except sr.UnknownValueError:
		print("Could not understand audio")
	except sr.RequestError as e:
		print("Could not request results; {0}".format(e))
