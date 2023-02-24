#!/usr/bin/env python
# coding: utf-8

# In[20]:


with open("sowpods.txt","r") as infile:
    raw_input = infile.readlines()
    data = [datum.strip('\n') for datum in raw_input]


# In[21]:


print(data[0:6])


# In[32]:


def run_scrabble(run):
    import datetime # For script timer
from wordscore import score_word
import string
import sys
import re


# In[36]:


def valid_word(input_word):
    '''Returns valid words from the text file as a list'''
    
    words=[]
    for word in data:
        input_word_list = list(input_word)
        for i, letter in enumerate(word):
            if letter in input_word_list:
                input_word_list.remove(letter)
            else:
                break
            if i == len(word)-1:
                words.append(word)
    return words

def wildcards(input_word):
    '''To handle inputs with wildcard characters'''
    
    words = valid_word(input_word.replace('?','').replace('*',''))
    words_scores = [(score_word(word),word.lower()) for word in words]
    n = len(words)
    
    if '?' in input_word:
        for letter in list(string.ascii_uppercase):
            score_letter = score_word(letter)
            new_word = input_word.replace('?',letter)
            if '*' in input_word:
                for next_letter in list(string.ascii_uppercase):
                    new_word = input_word.replace('?',letter).replace('*',next_letter)
                    score_next_letter = score_letter + score_word(next_letter)
                    word_set_list = [(score_word(word)-score_next_letter,word.lower()) for word in valid_word(new_word) if word not in words]
                    words.extend(valid_word(new_word))
                    words=list(set(words))
                    words_scores.extend(word_set_list)
            else:
                words_scores.extend([(score_word(word)-score_letter,word.lower()) for word in valid_word(new_word) if word not in words])
                words.append(new_word)
        return words_scores
    elif '*' in input_word:
        for letter in list(string.ascii_uppercase):
            score_letter = score_word(letter)
            new_word = input_word.replace('*',letter)
            words_scores.extend([(score_word(word)-score_letter,word.lower()) for word in valid_word(new_word) if word not in words])
        return words_scores

if __name__=='__main__':
    
    input_word = sys.argv[1].upper()
    
    if len(input_word) < 2:
        
        print("Input too short, number of characters must be greater than 2.")

    elif len(input_word) > 7:
        
        print("Input too big, number of characters must be less than 7.")
        
    elif (input_word.count('?') > 2) or  (input_word.count('*') > 2):
        
        print("Too many wild card character, only 2 allowed.")
        
    elif re.match(r'^[\?\*A-Z]*$',input_word):
        
        words_scores = []
        
        if re.match('[A-Z]*[\?\*]+[A-Z]*',input_word):
            
            words_scores = wildcards(input_word)
            
        else:
            
            words_scores = [(score_word(word), word.lower()) for word in valid_word(input_word)]
            
        output = words_scores
        output = sorted(output, key = lambda x : x[1]) # first sorting the words in alphabetical order
        output = sorted(output, key = lambda x : x[0], reverse=True) # then sorting the word score in descending order
        for word in output:
            print(word)
        print("Total number of words:",len(output))
        
    else:
        
        print("Invalid input. Input should only contain alpahabets and ?,* wildcards")


# In[ ]:




