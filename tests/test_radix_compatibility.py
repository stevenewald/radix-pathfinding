import unittest
import time
import pyradix
from tqdm import tqdm
class testUseCase(unittest.TestCase):
    def test_radix_compatibility(self):
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
        with tqdm(total=len(dict1)*2) as pbar:
            pbar.set_description("Testing radix compatibility")
            for word in dict1:
                val = pyradix.check_if_word(nonradix, word)
                self.assertTrue(val)
                pbar.update(1)
            for word in dict1:
                val = pyradix.check_if_word(radix, word)
                self.assertTrue(val)
                pbar.update(1)
            pbar.close()

            
if __name__ == '__main__':
    unittest.main()
