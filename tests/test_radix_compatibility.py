import unittest
import time
import pyradix
from tqdm import tqdm
class testUseCase(unittest.TestCase):
    dict1 = pyradix.get_dict("C:/Users/steve/Desktop/wordgame_nongit/Dictionaries/english_large.txt")
    with tqdm(total=3) as pbar:
        pbar.set_description("Generating test trees")
        nonradix = pyradix.words_to_tree(dict1)
        pbar.update(1)
        radix = pyradix.words_to_tree(dict1)
        pbar.update(1)
        pyradix.optimize_tree(radix)
        pbar.update(1)
        pbar.close()
    def test_radix_compatibility(self):
        with tqdm(total=len(self.dict1)*2) as pbar:
            pbar.set_description("Testing radix compatibility")
            for word in self.dict1:
                val = pyradix.check_if_word(self.nonradix, word)
                self.assertTrue(val)
                pbar.update(1)
            for word in self.dict1:
                val = pyradix.check_if_word(self.radix, word)
                self.assertTrue(val)
                pbar.update(1)
            pbar.close()
    def recursive_node_sub(self, topnode, pbar):
        for subnode in topnode.subnodes:
            self.assertEqual(pyradix.find_index_nonradix(topnode.subnodes, subnode.type, 1), pyradix.find_index(topnode.subnodes, subnode.type, 1))
            self.recursive_node_sub(subnode, pbar)
            pbar.update(1)

    def test_recursive_idx_equality(self):
        with tqdm(total=(pyradix.count_nodes(self.nonradix))) as pbar:
            pbar.set_description("Testing index equality")
            self.recursive_node_sub(self.nonradix, pbar)
            pbar.close()

            
if __name__ == '__main__':
    unittest.main()
