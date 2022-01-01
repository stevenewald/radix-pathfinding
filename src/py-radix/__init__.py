import image_utils as iu
import tree_utils as tu
import radix_utils as ru
import wordcheck_utils as wordcheck #not used currently but useful
import time
#from english_words import english_words_lower_alpha_set
#from threading import Thread
import numpy as np
import cv2

def initArray(wordlist):
    u = 0
    arr = [[None]*4, [None]*4, [None]*4, [None]*4]
    for i in range(4):
        for z in range(4):
            arr[i][z]=wordlist[u:u+1]
            u+=1
    return arr

def minmax(num1, num2, moves):
    first = (not ((num1<0 or num1>3) or (num2<0 or num2>3)))
    second = (not ((num1,num2) in moves))
    return (first and second)

def possibleLetters(i, z, currentMoves):
    letterarray = []
    currentMoves.append((i,z))
    possibleMoves = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1)]
    for move in possibleMoves:
        if(minmax(i+move[0],z+move[1],currentMoves)):
            letterarray.append((i+move[0],z+move[1]))
    return letterarray

def validWords(it, tn, accumlet, accum, i, z, moves, accumpos, arr):
    PL = possibleLetters(i,z, moves.copy())
    for nodes in tn.subnodes:
        lett = nodes.type
        for let in PL:
            lettF = arr[let[0]][let[1]]
            if(lett[0:1]==lettF):
                tempmoves = moves.copy()
                tempmoves.append(let)
                pos = let
                if(len(lett)>1):
                    pos = returnComb(lett, possibleLetters(let[0], let[1], tempmoves), 1, tempmoves, arr)
                if(pos[0]>-1 and pos[1]>-1):
                    if(nodes.isword):
                        accum.append(accumlet+lett)
                        if(len(accumlet+lett)>2):
                            accumpos.append((tempmoves, accumlet+lett))
                    validWords(it-1, nodes, accumlet+lett, accum, pos[0], pos[1], tempmoves, accumpos, arr)
    return (accum, accumpos)

def returnComb(word, PL, it, moves, arr):
    if(it>(len(word))):
        return (-1, -1)
    lett_to_find = word[it:it+1]
    for let in PL:
        newL = arr[let[0]][let[1]]
        if(newL==lett_to_find):
            moves.append(let)
            if(it==(len(word)-1)):
                return let
            else:
                return returnComb(word, possibleLetters(let[0], let[1], moves), it+1, moves, arr)
    return (-1, -1)
def sortByLen(e):
    return len(e[1])
def finalWords(showImages, wordlist): #alphabet array
    arr = initArray(wordlist)
    if(showImages):
        bg = iu.create_imgs(wordlist)
    words = []
    frames = []
    wordl = []
    for reps in range(16):
        i2 = int(reps % 4)
        z2 = int((reps - (reps % 4))/4)
        (v, uv) = validWords(100, topnode, "", [], i2, z2, [], [], arr)
        for uvi in uv:
            if(showImages):
                uvi[0].append((i2,z2))
                var = iu.create_arrows(bg, uvi[0], uvi[1])
                if(wordl.count(var[1])<1):
                    frames.append((var[0], var[1]))
                wordl.append(var[1])
        if(not(v==None)):
            words+=v
    otl = []
    k = 0
    if(showImages):
        frames.sort(key=sortByLen)
        frames.reverse()
        if(len(frames)>15):
            frames = frames[0:15]
        for frame in frames:
            cv2.imshow("Word", frame[0])
            cv2.waitKey(0)
    for i3 in range(len(words)):
        if(not(words[i3] in otl) and isinstance(words[i3], str)):
            otl.append(words[i3])
        else:
            k+=1
    otl = np.unique(otl).tolist()
    otl.sort(key=len)
    if(len(otl)>15): # reduce length of list
        otl = otl[len(otl)-15:len(otl)]
        
    return otl