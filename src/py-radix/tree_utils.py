class node:
    def __init__(self, type, isword, subnodes):
        self.type = type
        self.subnodes = subnodes
        self.isword = isword

def words_to_tree(file_location):
    topnode = node(str,False,[])
    dict = get_dict(file_location)
    for word in dict:
        if(word==""):
            continue
        topnode.subnodes = create_new_node(word, 1, topnode.subnodes)
    return topnode

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

def get_dict(file_location):
    file = open(file_location, "r") #or use english3.txt for smaller dictionary
    content = file.read()
    dict = content.split("\n")
    return dict

def count_nodes(topnode):
    val = 0
    for node in topnode.subnodes:
        val+=1
        val+=count_nodes(node)
    return val
    