import pyradix.tree_utils as tu

def optimize_tree(tree):
    anyReduxed = False
    for nodeb in tree.subnodes:
        if(len(nodeb.subnodes)==1 and not(nodeb.isword)):
            anyReduxed = True
            nodeb.type = nodeb.type+nodeb.subnodes[0].type
            nodeb.isword = nodeb.subnodes[0].isword
            nodeb.subnodes = nodeb.subnodes[0].subnodes.copy()
        tu.node.subnodes = optimize_tree(nodeb)
    if(anyReduxed):
        return optimize_tree(tree)
    else:
        return tree

def find_index(subnodes, word, endIdx): #works for both radix and non-radix
    num = 0
    for node in subnodes:
        extra = min(len(word), endIdx+len(node.type)-1)
        if(node.type==word[endIdx-1:extra]):
            return num
        num+=1
    return -1