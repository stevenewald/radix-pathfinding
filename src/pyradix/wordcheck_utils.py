import pyradix.tree_utils as tu
import pyradix.radix_utils as ru
# if non-radix and radix=false, slightly more efficient than radix=true
# if radix and radix=false, will break
def check_if_word(node, word, radix=True):
    if(word==""):
        return True
    return check_if_word_sub(word, node, 1, radix)

def check_if_word_sub(word, node, letters, radix): #actually not used for optimized pathfinding, but useful regardless
    sub1 = 0
    sub2 = 0
    if(radix):
        sub2 = ru.find_index(node.subnodes, word, letters)
        if(sub2>=0 and len(node.subnodes[sub2].type)+letters>len(word)):
            sub1 = ru.find_index(node.subnodes, word, len(word)+1-len(node.subnodes[sub2].type))
        else:
            sub1 = ru.find_index(node.subnodes, word, len(word))
    else:
        sub1 = ru.find_index(node.subnodes, word, len(word))
        sub2 = ru.find_index(node.subnodes, word, letters)
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