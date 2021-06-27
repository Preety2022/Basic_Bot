
pip install nltk

pip install newspaper3k

from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')
#nltk.download()

from flask import Flask
from flask import render_template

nltk.download('punkt',quiet=True)

article= Article('https://www.webmd.com/lung/coronavirus')
article.download()
article.parse()
article.nlp()
corpus = article.text

print(corpus)

text = corpus

# tokenization  = word tokenization
word_list= nltk.word_tokenize(text)
print(word_list)

#text = corpus
sentence_list = nltk.sent_tokenize(text)                          #A list of sentences

print(sentence_list)

# punctuation removal

import re
exp = re.compile('[%s]' % re.escape(string.punctuation))     

tokenized_no_punctuation_docs = []

for review in word_list:                                             
  new_review=[]
  for token in review:
    new_token = exp.sub(u'',token)
    if not new_token == u'':
      new_review.append(new_token)                                 # if not punctuatuion marks then append

  tokenized_no_punctuation_docs.append(new_review)

print(tokenized_no_punctuation_docs)

# A function to return a random greeting response to a users greeting
def greeting_response(text):
  text=text.lower()

  #Bots greeting response
  bot_greetings= ['hi','hey','hello','hey there']
  #users greeting
  user_greetings= ['hi','hello','hey there','hola','hey']

  for word in text.split():
    if word in user_greetings:
      return random.choice(bot_greetings)

def index_sort(list_var):
  length= len(list_var)
  list_index= list(range(0, length))

  x= list_var
  for i in range(length):
    for j in range(length):
      if x[list_index[i]] > x[list_index[j]]:
        #Swap
        temp = list_index[i]
        list_index[i] = list_index[j]
        list_index[j] =temp
  return list_index

#Create bots response

def bot_response(user_input):
  user_input= user_input.lower()
  sentence_list.append(user_input)
  bot_response='' # empty response  for the bot
  cm= CountVectorizer().fit_transform(sentence_list)
  similarity_scores = cosine_similarity(cm[-1], cm) #the last sentence the users input(-1) and compares it to rest of the count matrix
  similarity_scores_list= similarity_scores.flatten()
  index = index_sort(similarity_scores_list) # index will contain the list of indexes sorted of the highest values and the similarity scores and plcing at the lowest idex in the list
  index= index[1:]
  response_flag = 0     # this var acknowledging if there is response back to the user i.e., if the query matches any sentence based on the similarity_scores_list

  j= 0
  for i in range(len(index)):
    if similarity_scores_list[index[i]] > 0.0: # > 0.0 means we find something which is related to user's query
      bot_response= bot_response +' '+sentence_list[index[i]]
      response_flag=1 # found a response
      j= j+1     # j let's us know that how many scores we have that are above 0
      #if j>2:
       # break      # to limit the reponse statement given back to user so that there are  not many reponses
      
  if response_flag==0:
    bot_response= bot_response+' '+"I apologize, I don't understand."

  sentence_list.remove(user_input)

  return bot_response

#  start the conversation

print('Bot: Hey there, I am here to help you, Please ask me about covid-19 infection, I will try to answer as per my knowledge.')

# a list that tells the loop to start
exit_list =['exit','see you later','bye', 'quit','break']

while(True):
  user_input = input()
  if user_input.lower() in exit_list:
    print('Bot: Thank you for giving me a chance, see you!')
    break
  
  else:
    if greeting_response(user_input) != None:
      print('Bot: '+greeting_response(user_input))
    else:
      print('Bot:' +bot_response(user_input))

