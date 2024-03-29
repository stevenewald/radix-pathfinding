#import enchant
import time
#from english_words import english_words_lower_alpha_set
from threading import Thread
import numpy as np
import cv2
#out = cv2.VideoWriter('C:\Users\steve\Desktop\\test.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, (560, 560))

def create_img(letter):
    image = np.ones((140, 140, 3), np.uint8)
    image[:] = (255, 255, 255)
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = letter
    fontsize = 4
    textsize = cv2.getTextSize(text, font, fontsize, 2)[0]
    textX = int((image.shape[1] - textsize[0]) / 2)
    textY = int((image.shape[0] + textsize[1]) / 2)
    cv2.putText(image, text, (textX, textY ), font, fontsize, (0, 0, 0), 2)
    return image

def create_imgs(text):
    u = 0
    fullimg = np.ones((560,560,3), np.uint8)
    for i in range(4):
        tempimg = np.ones((140, 560, 3), np.uint8)
        for z in range (4):
            img = create_img(text[u:u+1])
            tempimg[:,z*140:z*140+140] = img
            u+=1
        fullimg[i*140:i*140+140, :] = tempimg
    return fullimg

def create_arrows_sub(src2, moves2, word):
    frames = []
    currentImg = np.zeros((560, 560, 3), np.uint8)
    moves = moves2.copy()
    lastPoint = moves[0]
    moves = moves[1:len(moves)-1]
    src = src2.copy()
    hasFalseYet = False
    for move in moves:
        if(move[1]):
            arrowedLine = cv2.arrowedLine(src, (lastPoint[0][1]*140+70, lastPoint[0][0]*140+70), (move[0][1]*140+70, move[0][0]*140+70), (0, 255, 0), 5)
        else:
            if(False):
                continue
            hasFalseYet = True
            arrowedLine = cv2.arrowedLine(src, (lastPoint[0][1]*140+70, lastPoint[0][0]*140+70), (move[0][1]*140+70, move[0][0]*140+70), (0, 0, 255), 5)
        currentImg = cv2.addWeighted(src, 0, arrowedLine, 1, 0)
        lastPoint = move
    wordlen = word[0:len(moves2)-1]
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = wordlen
    fontsize = 2
    textsize = cv2.getTextSize(text, font, fontsize, 2)[0]
    textX = int((currentImg.shape[1] - textsize[0]) / 2)
    textY = int((currentImg.shape[0] + textsize[1]) / 2)
    cv2.putText(currentImg, text, (textX, textY ), font, fontsize, (0, 0, 0), 2)
    frames.append(currentImg)
    #if(currentImg.shape[0]==560):
        #cv2.imshow("test", currentImg)
        #cv2.waitKey(0)
    #if(len(moves)>1):
        #frames = frames+create_arrows_sub(src2, moves2[0:len(moves2)-1], word)
    return frames

wordl = []
def create_arrows(src, moves, word):
    var = create_arrows_sub(src, moves, word)
    #var.append(src)
    #var.reverse()
    return (var, word)

file = open("C:/Users/steve/Desktop/wordgame_nongit/english3.txt", "r") #or use english3.txt for smaller dictionary
content = file.read()
dict = content.split("\n")
#d = enchant.Dict("en_US")
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
    sub2 = find_index(subnodes,word, letters)
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


topnode = words_to_tree()
print("Tree Loaded")

#wordlist = input("Enter letters: ")
#wordlist = "abcdefghijklmnop"
#wordlist = "ciolmhrfefednslo"
wordlist = "ttufpaepnerignss"
bg = create_imgs(wordlist)


def check_if_word(word, radix):
    return check_if_word_sub(word, topnode, 1, radix)

def check_if_word_sub(word, node, letters, radix): #actually not used in new version, but useful regardless
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
    second = (not (((num1,num2), True) in moves))
    return (first and second)

def possibleLetters(i, z, currentMoves):
    letterarray = []
    currentMoves2 = currentMoves.copy()
    currentMoves2.append(((i,z), False))
    possibleMoves = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1)]
    for move in possibleMoves:
        if(minmax(i+move[0],z+move[1],currentMoves2)):
            letterarray.append((i+move[0],z+move[1]))
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

def possibleRL(posList):
    arrv = []
    for pos in posList:
        arrv.append(arr[pos[0]][pos[1]])
    return arrv
bigwordl = []
def validWords(it, tn, accumlet, accum, i, z, moves, accumpos):
    global bigwordl
    PL = possibleLetters(i,z, moves.copy())
    for nodes in tn.subnodes:
        lett = nodes.type
        for let in PL:
            lettF = arr[let[0]][let[1]]
            tempmoves = moves.copy()
            if(lett[0:1]==lettF):
                tempmoves.append((let, True))
                pos = (let, True)
                if(len(lett)>1):
                    pos = returnComb(lett, possibleLetters(let[0], let[1], tempmoves), 1, tempmoves)
                if(pos[0][0]>-1 and pos[0][1]>-1):
                    if(nodes.isword):
                        accum.append(accumlet+lett)
                        if(len(accumlet+lett)>4):
                            accumpos.append((tempmoves, accumlet+lett))
                            bigwordl.append(accumlet+lett)
                    validWords(it-1, nodes, accumlet+lett, accum, let[0], let[1], tempmoves, accumpos)
            else:
                tempmoves.append((let, False))
                #tempmoves.append(((i, z), False))
                accumpos.append((tempmoves, accumlet+lett))
                #moves = moves
    return (accum, accumpos)

def returnComb(word, PL, it, moves):
    if(it>(len(word))):
        return ((-1, -1), False)
    lett_to_find = word[it:it+1]
    for let in PL:
        newL = arr[let[0]][let[1]]
        if(newL==lett_to_find):
            moves.append((let, True))
            if(it==(len(word)-1)):
                return (let, True)
            else:
                return returnComb(word, possibleLetters(let[0], let[1], moves), it+1, moves)
    return ((-1, -1), False)

def __draw_label(img, text, pos, bg_color):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    scale = .75
    color = (0, 0, 0)
    thickness = cv2.FILLED
    margin = 2

    txt_size = cv2.getTextSize(text, font_face, scale, thickness)

    end_x = pos[0] + txt_size[0][0] + margin
    end_y = pos[1] - txt_size[0][1] - margin

    cv2.putText(img, text, pos, font_face, scale, bg_color, 1, cv2.LINE_AA)
    return img

bwl2 = []
def finalWords(radix, export):
    global bigwordl
    global bwl2
    words = []
    frames = []
    wordl = []
    for reps in range(16):
        i2 = int(reps % 4)
        z2 = int((reps - (reps % 4))/4)
        (v, uv) = validWords(100, topnode, "", [], i2, z2, [], [])
        xz = 0
        for uvi in uv:
            if(len(bwl2)>27):
                continue
            if((xz%100)==0):
                print(reps)
            if(export):
                if(False):
                    continue
                uvi[0].append(((i2,z2), True))
                var = create_arrows(bg, uvi[0], uvi[1])
                isLong = False
                if(wordl.count(var[1])<1):
                    if(len(var[1])>5 and (var[1] in bigwordl) and (not (var[1] in bwl2))):
                        bwl2.append(var[1])
                        isLong = True
                    text = ""
                    for word in bwl2:
                        text = text+word+"\n"
                    for f2 in var[0]:
                        y0, dy = 20, 20
                        for i, line in enumerate(text.split('\n')):
                            y = y0 + i*dy
                            f2 = __draw_label(f2, line, (0, y), (0,0,255))
                        #f2 = __draw_label(f2, text, (0,250), (0,0,255))
                        #cv2.imshow("t", f2)
                        #cv2.waitKey(0)
                    frames = frames + var[0]
                    if(False): #isLong
                        for j in range(0):
                            frames = frames + var[0]
                wordl.append(var[1])
                xz+=1
                #print(xz)
        if(not(v==None)):
            words+=v
    otl = []
    k = 0
    if(export):
        #out = cv2.VideoWriter('C:/Users/steve/Desktop/test.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, (560, 560))
        out = cv2.VideoWriter('C:/Users/steve/Desktop/test.mp4',-1, 60, (560, 560))
        for frame in frames:
            if(frame[0][0][0]>0):
                out.write(frame)
        out.release()
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

print("Performing tree operations\n")
triesize = str(count_nodes(topnode))
startTime = time.time()
export_frames = True
pw1 = finalWords(False, False)
endTime = time.time()
topnode = optimize_tree(topnode)
st2 = time.time()
pw2 = finalWords(True, export_frames)
et2 = time.time()
nodes2 = count_nodes(topnode)
ext1 = ((endTime-startTime)*1000)
ext2 = ((et2-st2)*1000)
sizechange = abs(10000*(nodes2-int(triesize))/int(triesize))
timechange = (10000*(ext2-ext1)/ext1)
print("Trie vertices: " + triesize)
print("Trie execution time: " + str(round(ext1)/1000) + " seconds")
print("=========================")
print("Radix tree vertices: " + str(nodes2))
print("Radix tree execution time: " + str(round(ext2)/1000) + " seconds")
print("=========================")
print("Changes from implementing radix tree")
print("Reduction in size: -" + str(round(sizechange)/100) + "%")
if(timechange>0):
    print("Increase in execution time: +" + str(round(abs(timechange))/100) + "%")
else:
    print("Decrease in execution time: -" + str(round(abs(timechange))/100) + "%")
print("=========================")
print(pw1)
if(False): #only if testing words
    numvw = 0
    for word in dict:
        word2 = word + "e"
        check1 = word2 in dict
        check2 = check_if_word(word2, True)
        if(check1 and (not check2)):
            print(word)
        elif((not check1) and check2):
            print(word)
        numvw+=1
        if(numvw%1000==0):
            print(numvw)
    print("Word check done")
if(not(pw1==pw2)):
    print("ERROR: TRIE AND RADIX TREE UNEQUAL")