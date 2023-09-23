import sys
import argparse
import os

from nltk.parse.stanford import StanfordParser
from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger
from nltk.tokenize.stanford import StanfordTokenizer
from nltk.tree import *
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

from moviepy.editor import VideoFileClip, concatenate_videoclips

import time

import cv2
import numpy as np

# eng_sentence = input("Enter a string:")

def english_to_isl(eng_sentence):
    start_time = time.time()

    java_path = r"C:\Program Files\Android\Android Studio\jre\bin"
    os.environ['JAVAHOME'] = java_path

    os.environ['CLASSPATH'] = r"txt2sign\stanford-parser-full-2020-11-17"

    parser = StanfordParser(model_path=r'txt2sign\jars\edu\stanford\nlp\models\lexparser\englishPCFG.ser.gz')

    englishtree = [tree for tree in parser.parse(eng_sentence.split())]
    parsetree = englishtree[0]
    dict = {}

    # "***********subtrees**********"
    parenttree= ParentedTree.convert(parsetree)
    for sub in parenttree.subtrees():
        dict[sub.treeposition()]=0

    #"----------------------------------------------"
    isltree=Tree('ROOT',[])
    i=0
    # print("**************************************************************************************************************")
    # print("printing parsed tree:",parenttree)
    #reordering (SOV to SVO)
    for sub in parenttree.subtrees():
        if(sub.label()=="NP" and dict[sub.treeposition()]==0 and dict[sub.parent().treeposition()]==0):
            dict[sub.treeposition()]=1
            isltree.insert(i,sub)
            i=i+1
        if(sub.label()=="VP" or sub.label()=="PRP"):
            for sub2 in sub.subtrees():
                if((sub2.label()=="NP" or sub2.label()=='PRP')and dict[sub2.treeposition()]==0 and dict[sub2.parent().treeposition()]==0):
                    dict[sub2.treeposition()]=1
                    isltree.insert(i,sub2)
                    i=i+1

    for sub in parenttree.subtrees():
        for sub2 in sub.subtrees():
            if(len(sub2.leaves())==1 and dict[sub2.treeposition()]==0 and dict[sub2.parent().treeposition()]==0):
                dict[sub2.treeposition()]=1
                isltree.insert(i,sub2)
                i=i+1

    #parsed_sent is a list containg all the words after parsing
    parsed_sent = isltree.leaves()

    words = parsed_sent
    # print("********************************************************************************************************")
    # print("Reordered sentense:",words)
    #words to removed from final ISL sentence (conjunctions,articles,linking verbs)
    to_remove = ['for','and','nor','but','or','yet','so','a','an','the','am','are','is','was','were']

    lemmatizer = WordNetLemmatizer()
    ps = PorterStemmer()
    lemmatized_words=[]

    txt = ""
    for word in parsed_sent:
        txt = txt + word + " "

    #tokenizing the parsed words
    tokenized = sent_tokenize(txt)
    for i in tokenized:
        wordsList = nltk.word_tokenize(i)
        tagged = nltk.pos_tag(wordsList)
    # print(tagged)

    #lammetizing according to verb,adjective,adverb and nouns
    lemmatizer = WordNetLemmatizer()

    for w in tagged:
        if w[1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ','VP']:
            lemmatized_words.append(lemmatizer.lemmatize(w[0],pos='v'))
        elif w[1] in ['RB', 'RBR', 'RBS']:                             #adverb
            lemmatized_words.append(lemmatizer.lemmatize(w[0],pos='r'))
        elif w[1] in ['JJ', 'JJR', 'JJS'] :                           #adjective
            lemmatized_words.append(lemmatizer.lemmatize(w[0],pos='a'))
        else:                                              #default noun
            lemmatized_words.append(lemmatizer.lemmatize(w[0]))
    # print("**************************************************************************************************")
    # print("After lammetizing:",lemmatized_words)
    islsentence = ""

    vdo_lst = []
    for w in lemmatized_words:
        if w not in to_remove:
            vdo_lst.append(w)
            islsentence+=w
            islsentence+=" "

    print("ISL :",islsentence)


    arg_array=[]
    new_lst = []
    files_and_directories = os.listdir(r"txt_sign")

    for text in vdo_lst:
        if text+".mp4" in files_and_directories:
            new_lst.append(text)
        else:
            for letter in list(text):
                new_lst.append(letter)

    for words in new_lst:
        arg_array.append(VideoFileClip("txt_sign\\"+words+".mp4"))
        print(words+".mp4")

    final_clip = concatenate_videoclips(arg_array,method='compose')
    final_clip.write_videofile(r"static\my_concatenation.mp4")
    end_time = time.time()
    total_time = end_time - start_time
    print("Time: ", total_time)
    return islsentence

#Grammar rules being followed
#1. Subject-object-verbs ---> Subject-verb-object
#2. root words only present as ISL doesn't support past,future tense of same wordsList
#3. removing conjunctions, articles and linking verbs
#4. words which are absent in video directory will be spelled using letters
