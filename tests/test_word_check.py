topnode = tu.words_to_tree("C:/Users/steve/Desktop/wordgame_nongit/Dictionaries/english_small.txt")
wordlist = "abcdefghijklmnop"
triesize = str(tu.count_nodes(topnode))
startTime = time.time()
pw1 = finalWords(False, wordlist)
endTime = time.time()
topnode = ru.optimize_tree(topnode)
st2 = time.time()
pw2 = finalWords(True, wordlist)
et2 = time.time()
nodes2 = tu.count_nodes(topnode)
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
    print(len(pw1))
    print(len(pw2))