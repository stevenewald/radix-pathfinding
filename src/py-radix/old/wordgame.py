import enchant
import itertools
import time
from english_words import english_words_lower_alpha_set
from threading import Thread
import numpy as np

file = open("C:/Users/steve/Desktop/wordgame/english3.txt", "r")
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
#def optimize_tree(tree):

def count_nodes(topnode):
    val = 0
    for node in topnode.subnodes:
        val+=1
        val+=count_nodes(node)
    return val
    


def create_new_node(word, letters, subnodes):
    sub2 = find_index(subnodes,word[letters-1:letters])
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



def find_index(subnodes, word):
    num = 0
    for node in subnodes:
        if(node.type==word):
            return num
        num+=1
    return -1


topnode = words_to_tree()
print("Tree Loaded")

#wordlist = input("Enter letters: ")
wordlist = "abcdefghijklmnop"


def check_if_word(word):
    return check_if_word_sub(word, topnode, 1)

def check_if_word_sub(word, node, letters):
    sub1 = find_index(node.subnodes, word[len(word)-1:len(word)])
    sub2 = find_index(node.subnodes, word[letters-1:letters])
    if(sub1>=0 and node.subnodes[sub1].isword and len(word)==letters):
        return True
    elif(sub2>=0):
        return check_if_word_sub(word, node.subnodes[sub2], letters+1)
    else:
        return False
           

arr = [[None]*4, [None]*4, [None]*4, [None]*4]
def initArray():
    u = 0
    for i in range(4):
        for z in range(4):
            arr[i][z]=wordlist[u:u+1]
            u+=1
initArray()

def minmax(num1, num2, moves):
    first = (not ((num1<0 or num1>3) or (num2<0 or num2>3)))
    second = (not ((num1,num2) in moves))
    return (first and second)

def possibleLetters(i, z, nt, currentMoves):
    if(nt==0):
        return []
    letterarray = []
    word=arr[i][z]
    currentMoves.append((i,z))
    possibleMoves = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1)]
    for move in possibleMoves:
        if(minmax(i+move[0],z+move[1],currentMoves)):
            letterarray.append(allCombinations(word, possibleLetters(i+move[0],z+move[1],nt-1,currentMoves.copy())))
    return letterarray

def allCombinations(l1, l2):
    if(len(l2)==0):
        return l1
    combined = []
    for first in l1:
        for second in l2:
            for third in second:
                combined.append(first+third)
    return combined

def letterwords(num, results, idx):
    i = idx % 4
    z = (idx - (idx % 4))/4
    i = int(i)
    z = int(z)
    val = (possibleLetters(i,z,num,[]))
    results[idx] = val
    

def letterwordsthreads(num):
    threads = [None] * 16
    results = [None] * 16
    for i in range(len(threads)):
        threads[i] = Thread(target=letterwords, args=(num, results, i))
        threads[i].start()
    
    for i in range(len(threads)):
        threads[i].join()
    return results

def flatten(t):
    return list(itertools.chain.from_iterable(t))

def validWords(maxNum):
    returnArray = []
    tra = []
    returnArray = letterwordsthreads(maxNum)
    for u in range(2):
        returnArray = flatten(returnArray)
    returnArray = np.unique(returnArray).tolist()
    for word in returnArray:
        if(check_if_word(word)):
            tra.append(word)
    return tra

def finalWords():
    words = []
    for i in range(4, 8):
        words+=validWords(i)
    words = np.unique(words).tolist()
    words.sort(key=len)
    return words


print("Trie size: " + str(count_nodes(topnode)))
startTime = time.time()
print(finalWords())
endTime = time.time()
print("Execution time: " + str(endTime-startTime))