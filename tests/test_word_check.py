import unittest
import time
import pyradix
from tqdm import tqdm
class testWordCheck(unittest.TestCase):
    dict1 = pyradix.get_dict("C:/Users/steve/Desktop/wordgame_nongit/Dictionaries/english_large.txt")
    wordlistF = ["ttufpaepnerignss", "ponmlkjihgfedcba", "ciolmhrfefednslo", "abcdefghijklmnop"]
    with tqdm(total=3) as pbar:
        pbar.set_description("Generating test trees")
        nonradix = pyradix.words_to_tree(dict1)
        pbar.update(1)
        radix = pyradix.words_to_tree(dict1)
        pbar.update(1)
        pyradix.optimize_tree(radix)
        pbar.update(1)
        pbar.close()
    def test_testvalidity(self):
        self.assertGreater(len(self.dict1), 10000)
    def test_nonradix_word_equality(self):
        with tqdm(total=(len(self.dict1))) as pbar:
            pbar.set_description("Testing non-radix validity")
            for word in self.dict1:
                if(word==""):
                    continue
                val = pyradix.check_if_word(self.nonradix, word)
                self.assertTrue(val)
                pbar.update(1)
            pbar.close()
    def test_radix_word_equality(self):
        with tqdm(total=(len(self.dict1))) as pbar:
            pbar.set_description("Testing radix validity")
            for word in self.dict1:
                if(word==""):
                    continue
                val = pyradix.check_if_word(self.radix, word)
                self.assertTrue(val)
                pbar.update(1)
            pbar.close()
    def test_result_equality(self):
        with tqdm(total=len(self.wordlistF)) as pbar:
            pbar.set_description("Testing non-radix and radix equality")
            for wordlist in self.wordlistF:
                pw1 = pyradix.wordPathfinding(False, self.nonradix, wordlist)
                pw2 = pyradix.wordPathfinding(False, self.radix, wordlist)
                self.assertEqual(pw1, pw2)
                pbar.update(1)
            pbar.close()
    def test_trie_size(self):
        with tqdm(total=2) as pbar:
            pbar.set_description("Validating non-radix and radix size")
            size = pyradix.count_nodes(self.nonradix)
            pbar.update(1)
            size2 = pyradix.count_nodes(self.radix)
            pbar.update(1)
            self.assertEqual(size, 1027814)
            self.assertEqual(size2, 478056)
            pbar.close()
            
if __name__ == '__main__':
    unittest.main()