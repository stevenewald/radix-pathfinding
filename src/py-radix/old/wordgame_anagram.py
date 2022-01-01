import enchant
import itertools
import time
from english_words import english_words_lower_alpha_set
from threading import Thread
import numpy as np

file = open("C:/Users/steve/Desktop/wordgame/english3.txt", "r") #or use english3.txt for smaller dictionary
content = file.read()
dict = content.split("\n")
d = enchant.Dict("en_US")
class node:
    def __init__(self, type, isword, subnodes):
        self.type = type
        self.subnodes = subnodes
        self.isword = isword

def words_to_tree():
    topnode = node(str,False,[])
    for word in dict:
        if(word==""):
            continue
        topnode.subnodes = create_new_node(word, 1, topnode.subnodes)
    return topnode


# optimizes the tree
# transforms it from a trie to a radix tree
def optimize_tree(tree):
    anyReduxed = False
    for nodeb in tree.subnodes:
        if(len(nodeb.subnodes)==1 and not(nodeb.isword)):
            anyReduxed = True
            nodeb.type = nodeb.type+nodeb.subnodes[0].type
            nodeb.isword = nodeb.subnodes[0].isword
            nodeb.subnodes = nodeb.subnodes[0].subnodes.copy()
        node.subnodes = optimize_tree(nodeb)
    if(anyReduxed):
        return optimize_tree(tree)
    else:
        return tree

def count_nodes(topnode):
    val = 0
    for node in topnode.subnodes:
        val+=1
        val+=count_nodes(node)
    return val
    


def create_new_node(word, letters, subnodes):
    sub2 = find_index_radix(subnodes,word, letters)
    if(len(word)==letters):
        if(sub2<=0):
            subnodes.append(node(word[letters-1:letters], True, []))
        else:
            subnodes[sub2].isword = True
        return subnodes
    elif(sub2>=0):
        subnodes[sub2].subnodes = create_new_node(word,letters+1,subnodes[sub2].subnodes)
        return subnodes
    else:
        subnodes.append(node(word[letters-1:letters],False,[]))
        subnodes[sub2].subnodes = create_new_node(word, letters+1, subnodes[sub2].subnodes)
        return subnodes



def find_index(subnodes, word, endIdx):
    num = 0
    for node in subnodes:
        if(node.type==word[endIdx-1:endIdx]):
            return num
        num+=1
    return -1

def find_index_radix(subnodes, word, endIdx):
    num = 0
    for node in subnodes:
        extra = min(len(word), endIdx+len(node.type)-1)
        if(node.type==word[endIdx-1:extra]):
            return num
        num+=1
    return -1


def check_if_word(word, radix):
    return check_if_word_sub(word, topnode, 1, radix)

def check_if_word_sub(word, node, letters, radix):
    sub1 = 0
    sub2 = 0
    if(radix):
        sub2 = find_index_radix(node.subnodes, word, letters)
        if(sub2>=0 and len(node.subnodes[sub2].type)+letters>len(word)):
            sub1 = find_index_radix(node.subnodes, word, len(word)+1-len(node.subnodes[sub2].type))
        else:
            sub1 = find_index_radix(node.subnodes, word, len(word))
    else:
        sub1 = find_index(node.subnodes, word, len(word))
        sub2 = find_index(node.subnodes, word, letters)
    if(sub2>=0 and len(node.subnodes[sub2].type)+letters>len(word) and radix):
        val = letters==len(word)+1-len(node.subnodes[sub2].type)
    else:
        val = len(word)==letters
    if(sub1>=0 and node.subnodes[sub1].isword and val):
        return True
    elif(sub2>=0):
        return check_if_word_sub(word, node.subnodes[sub2], letters+len(node.subnodes[sub2].type), radix)
    else:
        return False
        

def allCombinations(l1, l2):
    if(len(l2)==0):
        return l1
    combined = []
    for first in l1:
        for second in l2:
            for third in second:
                combined.append(first+third)
    return combined

def RWS(tree, chars, word_accum, prevchars):
    # search for potential words by going through tree, allow for errors, get fuzzy matches
    # efficiency should be O(log(m)) rather than O(log(m^2)) if brute force
    # uses tree-shaped fuzzy pathfinding
    word_accum = []
    if(len(chars)==0):
        return word_accum
    for i in range(len(chars)):
        charlist = chars[0:i] + chars[i+1:len(chars)]
        firstchar = chars[i:i+1]
        if(len(prevchars)>2):
            word_accum+=checkChar(tree.subnodes, firstchar, prevchars)
        idx = find_index_radix(tree.subnodes, firstchar, 1)
        if(idx>=0):
            word_accum+=RWS(tree.subnodes[idx], charlist, word_accum, prevchars+firstchar)
    return word_accum


def checkChar(subnodes, firstchar, prevchars):
    accum = []
    for tn in subnodes:
        if(tn.type==firstchar and tn.isword):
            accum.append(prevchars+firstchar)
    return accum

def anagram_finder(node, charlist):
    words = RWS(node, charlist, "", "")
    words = np.unique(words).tolist()
    words.sort(key=len)
    return words

topnode = words_to_tree() # not radix
topnode = optimize_tree(topnode) # turn into radix
print("Radix tree Loaded")
wordlist = input("Enter letters: ")
#wordlist = "abcdef"
st = time.time()
print(anagram_finder(topnode, wordlist))
et = time.time()
timeelapsed = round((et-st)*1000)/1000
print("Time elapsed: " + str(timeelapsed))
