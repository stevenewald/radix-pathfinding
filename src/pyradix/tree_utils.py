import copy
import pyradix.radix_utils as ru
class node:
    def __init__(self, type, isword, subnodes):
        self.type = type
        self.subnodes = subnodes
        self.isword = isword

    def copy(self):
        copied = copy.deepcopy(self)
        return copied

def words_to_tree(dict):
    topnode = node(str,False,[])
    for word in dict:
        if(word==""):
            continue
        topnode.subnodes = create_new_node(word, 1, topnode.subnodes)
    return topnode

def add_word(topnode, word): #verify if this works with radix tree, could complicate things. hard to tell
    if(len(word)>0):
        topnode.subnodes = create_new_node(word, 1, topnode.subnodes)

#def delete_word(topnode, word):
#    if(len(word)>0):
#        delete_word_sub(topnode, word)

def create_new_node(word, letters, subnodes):
    sub2 = ru.find_index(subnodes,word, letters)
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

# deprecated
# insignifigantly more efficient than universal version
def find_index_nonradix(subnodes, word, endIdx):
    num = 0
    for node in subnodes:
        if(node.type==word[endIdx-1:endIdx]):
            return num
        num+=1
    return -1

def get_dict(file_location):
    file = open(file_location, "r") #or use english3.txt for smaller dictionary
    content = file.read()
    dict = content.split("\n")
    file.close()
    return dict

def count_nodes(topnode):
    val = 0
    for node in topnode.subnodes:
        val+=1
        val+=count_nodes(node)
    return val
    