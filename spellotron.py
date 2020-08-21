#both american-english.txt and keyboard-letters.txt are required for this program
"""
Author: Nguyen Dinh Van Pham <vnp7514@rit.edu>
File: spellotron.py
Purpose: to create a program that corrects spelling
Assignment: Project
Language: Python3.7
"""
import sys
import time, re

#################################################################################
#GLOBAL FILES
#################################################################################
LEGAL_WORD_FILE = "american-english.txt"
KEY_ADJACENCY_FILE = "keyboard-letters.txt"

#################################################################################
#MAIN
#################################################################################
def main():
    
    if len(sys.argv) > 1 and len(sys.argv) < 4:
        if sys.argv[1] == "words" or sys.argv[1] == "lines":
            lst = []
            if len(sys.argv) == 2:
                text_source = sys.stdin
                lst += text_source.readline().strip(" ").split(" ")
            else:
                text_source = open(sys.argv[2])
                for line in text_source:
                    lst += line.strip(" ").split(" ")
            if sys.argv[1] == "words":
                words(lst)
            else:
                lines(lst)
                
            if text_source != sys.stdin:
                text_source.close()
            
        else:
            print( "Usage: python3.7 spellotron.py words/lines [filename]", \
                   file=sys.stderr ) 
    else:
        print( "Usage: python3.7 spellotron.py words/lines [filename]", \
               file=sys.stderr )

#################################################################################
#LIBRARY OF ENGLISH WORDS AND THE ALPHABET
#################################################################################
def alphabet():
    """
Pre-conditions: keyboard-letters.txt is included
Post-conditions: None
This creates a dictionary where keys are the letters and the values are
the adjacent letters. For example:
dct['a'] = ['q','w','s','z', 'a']
    """
    dct = dict()
    for line in open(KEY_ADJACENCY_FILE):
        lst = line.strip().split()
        dct[lst[0]] = lst[1:]
        dct[lst[0]].append(lst[0])
    return dct
    
def library():
    """
Pre-conditions: american-english.txt is included
Post-conditions: None
A set is created containing all the english words
    """
    lib = set()
    for word in open(LEGAL_WORD_FILE, encoding = "utf-8"):
        word = word.strip()
        lib.add(word)
    return lib
#################################################################################
#TWO METHODS OF REPORTING THE SPELLCHECKING PROCESS
#################################################################################
def words(lst):
    """
Pre-conditions: lst is a list of strings
Post-conditions: Any new line or '' is removed from lst
This function prints a list of words on which fixes were attempted.
    Then it prints the number of words read, the number of and a list of
    each of the following, the corrected words, and the unknown words.
    """
    while '\n' in lst:
        lst.remove('\n')
    while '' in lst:
        lst.remove('')
    correct, unknown, output = spell_check(lst)
    for word in correct:
        correct1, unknown1, output1 = spell_check([word])
        print(word, ' -> ', output1[0])
    print('\n')
    print(len(lst), " words read from file.\n")
    correct.sort()
    unknown.sort()
    print(len(correct),' Corrected Words', '\n', correct, '\n')
    print(len(unknown),' Unknown Words', '\n', unknown)

def lines(lst):
    """
Pre-conditions: lst is a list of strings
Post-conditions: Any new line or '' is removed from lst
This function prints the corrected text in its entirety.
    Then it prints the number of words read, the number of and a list of
    each of the following, the corrected words, and the unknown words.
    """
    while '\n' in lst:
        lst.remove('\n')
    while '' in lst:
        lst.remove('')
    correct, unknown, output = spell_check(lst)
    print(combine_words(output))
    print('\n')
    print(len(lst), " words read from file.\n")
    correct.sort()
    unknown.sort()
    print(len(correct),' Corrected Words', '\n', correct, '\n')
    print(len(unknown),' Unknown Words', '\n', unknown)

#################################################################################
#SPELLCHECK
#################################################################################
def spell_check(lst):
    """
Pre-conditions: lst is a list of strings
Post-conditions: a list of three lists: correct, unknown, and output is returned
This function spell checks each element of the lst then put
    them in the appropriate lists (correct, unknown, output).
    """
    lib = library()
    alpha = alphabet()
    naked = "" #This is w
    correct = []
    unknown = []
    output = []
    punctuation = dict()
    for word in lst: #these raw words still have punctuations in them
        if word.isdigit():
            output.append(word)
        else:
            punctuation, naked = punctuation_removal(word)
            if naked in lib: #step 4
                output.append(word)
            elif lower(naked) in lib:
                output.append(punctuation_addition(punctuation,\
                                                       naked))
            else:
                new = naked # w'
                new = adjacency(new, lib, alpha)#step 6a
                new = missing(new, lib, alpha)#step 6a
                new = extra(new, lib, alpha)
                if new in lib:
                    correct.append(remove_newline_and_tab(word))
                    output.append(punctuation_addition(punctuation, \
                                                       new))
                else:
                    #step 6b
                    new = lower(new)# w'
                    new = adjacency(new, lib, alpha)
                    new = missing(new, lib, alpha)
                    new = extra(new, lib, alpha)
                    if new in lib:
                        correct.append(remove_newline_and_tab(word))
                        output.append(punctuation_addition(punctuation, \
                                                       upper(new)))
                    else:
                        unknown.append(remove_newline_and_tab(word))
                        output.append(word)
    return (correct, unknown, output)

#################################################################################
#MAKING THE FIRST LETTER OF A WORD UPPERCASE OR LOWERCASE
#################################################################################
def lower(word):
    """
Pre-conditions: combine_letters() function exists
Post-conditions: None
This function returns a word where the first letter of the word is lower-cased
    """
    if word == '':
        return ''
    lst = []
    lst += str(word)
    lst[0] = lst[0].lower()
    return combine_letters(lst)

def upper(word):
    """
Pre-conditions: combine_letters() function exists
Post-conditions: None
This function returns a word where the first letter of the word is upper-cased
    """
    if word == '':
        return ''
    lst = []
    lst += word
    lst[0] = lst[0].upper()
    return combine_letters(lst)

#################################################################################
#PUNCTUATION RELATED FUNCTIONS
#################################################################################

def punctuation_addition(punctuation, word):
    """
Pre-conditions: punctuation is a dictionary where the punctuation is the key
                    and the index is the value
                word is str
Post-conditions: a string with punctuation added to the word
This function adds the punctuations to the word
    """
    front = ''
    back = ''
    if len(punctuation) >2:
        print("There is an extra punctuation"\
                  , file = sys.stderr)
    for key in punctuation:
        for index in punctuation[key]:
            if index == 0:
                front = key
            else:
                back = key
    return str(front) + str(word) + str(back)
                                  
def punctuation_removal(word):
    """
Pre-conditions: word is a string
Post-conditions: a dictionary of punctuations is returned and
                the word without punctuations is returned
This function removes punctuations from the front and the back of the word
including the new line character and tab
    """
    punctuation = dict()
    result =''
    limit_check = False
    zero_check = False
    lst = re.split(r'(\W+)', word)
    while "" in lst:
        lst.remove("")
    if len(lst) == 1:
        result = word
    else:
        while zero_check == False or limit_check == False:
            if lst[len(lst) -1][0] in '_-[]{}()@#^&,.!?:;"' \
                 or lst[len(lst) -1][0] in "'*+=/" \
                 or lst[len(lst) -1][0] == '\t' \
                 or lst[len(lst) -1][0] == '\n'\
                 or lst[len(lst) -1][0] == '\\':
                if limit_check == False:
                    punctuation[lst[len(lst) -1]] = [len(lst) -1]
                    lst.pop(len(lst) -1)
                limit_check = True
            elif lst[0][0] in '_-[]{}()@#^&,.!?:;"' or lst[0][0] in "'*+=/"\
                       or lst[0][0] == '\t' or lst[0][0] == '\n'\
                       or lst[0][0] == '\\':
                if zero_check == False:
                    if lst[0] in punctuation:
                        punctuation[lst[0]].append(0)
                        lst.pop(0)
                    else:
                        punctuation[lst[0]] = [0]
                        lst.pop(0)
                    zero_check = True
            else:
                break
    return (punctuation, combine_letters(lst))

def remove_newline_and_tab(word):
    """
Pre-conditions: word is a str
                combine_letters(lst) is needed
Post-conditions: a string without the newline character and the tab
                character is returned
This function removes the newline character and the tab character
    """
    lst = list()
    lst += word
    while '\t' in lst:
        lst.remove('\t')
    while '\n' in lst:
        lst.remove('\n')
    return combine_letters(lst)

#################################################################################
#THREE MAIN WAYS TO CORRECT A MISSPELLED WORDS
#################################################################################
def adjacency(word, lib, alpha):
    """
Pre-conditions: word is a string
                lib is the library of legal words
                alpha is the alphabet with adjacent keys
Post-conditions: None
This function checks whether the user accidentally hits an key adjacent to the
    intended one instead of the intended one.
    """
    result = word
    if word in lib:
        return word
    else:
        temp = ""
        lst = list()
        lst += word
        for i in range(len(lst)): # attempts to change each character into
        # an adjacent character
            if lst[i] in alpha:
                for e in alpha[lst[i]]: # a list of adjacent characters
                    if temp in lib:
                        result = temp
                        break
                    else:
                        lst[i] = e
                        temp = combine_letters(lst)
            else:
                return word
    if result != word:
        return result
    return word

def missing(word, lib, alpha):
    """
Pre-conditions: word is a string
                lib is the library of legal words
                alpha is the alphabet with adjacent keys
Post-conditions: None
This function checks for mispelling due to failing to type one key
    """
    result = word
    if word in lib:
        return word
    else:
        temp = ""
        lst = list()
        lst += word
        for i in range(len(lst)+1):
            if temp in lib:
                break
            for a in alpha.keys():
                lst.insert(i, a)
                temp = combine_letters(lst)
                if temp in lib:
                    result = temp
                    break
                else:
                    lst.pop(i)
    if result != word:
        return result
    return  word

def extra(word, lib, alpha):
    """
Pre-conditions: word is a string
                lib is the library of legal words
                alpha is the alphabet with adjacent keys
Post-conditions: None
This function checks whether a key was accidentally typed
    """
    result = word
    if word in lib:
        return word
    else:
        temp = ''
        lst = list()
        lst += word
        for i in range(len(lst)):
            remove = lst.pop(i)
            temp = combine_letters(lst)
            if temp in lib:
                result = temp
                break
            else:
                lst.insert(i, remove)
    if word != result:
        return result
    return word

#################################################################################
#COMBINING ELEMENTS IN A STRING INTO A STRING
#################################################################################
def combine_letters(lst):
    """
Pre-conditions: lst is a list
Post-conditions: None
Combining each element of the lst into a string
    """
    temp = ""
    for each in lst:
        temp = temp + str(each)
    return temp

def combine_words(lst):
    """
Pre-conditions: lst is a list
Post-conditions: None
Combining words of a list into a sentence with white spaces between each word.
    """
    temp = ""
    for i in range(len(lst)):
        if i == len(lst) -1:
            temp = temp + str(lst[i])
        elif '\n' in lst[i] or '\t' in lst[i]:
            temp = temp + str(lst[i])
        else:
            temp = temp + str(lst[i]) + " "    
    return temp

if __name__ == '__main__':
    main()
