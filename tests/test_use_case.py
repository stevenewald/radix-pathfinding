import unittest
import time
import pyradix
from tqdm import tqdm
class testUseCase(unittest.TestCase):
    def test_usecase1(self):
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
        wordlist = "abcdefghijklmnop"
        words = pyradix.wordPathfinding(False, radix, wordlist)
        words = words[len(words)-15:len(words)]
        self.assertGreater(len(words), 10)
        wordlistx = ["testing", "gjkajkgr", "sgrlkgsjns", "egjrgjrdgk", "w2rs", "1", "", "klgksl", "test", "something", "apdpdfn"]
        with tqdm(total=len(wordlistx)*2) as pbar:
            pbar.set_description("Testing non-radix word addition")
            for word in wordlistx:
                pyradix.add_word(nonradix, word)
                pbar.update(1)
            for word in wordlistx:
                val = pyradix.check_if_word(nonradix, word)
                val2 = pyradix.check_if_word(nonradix, word, False)
                self.assertTrue(val)
                self.assertTrue(val2)
                pbar.update(1)
            pbar.close()
        with tqdm(total=len(wordlistx)*2) as pbar:
            pbar.set_description("Testing radix word addition")
            for word in wordlistx:
                pyradix.add_word(radix, word)
                pbar.update(1)
            for word in wordlistx:
                val = pyradix.check_if_word(radix, word)
                val2 = pyradix.check_if_word(radix, word, True)
                self.assertTrue(val)
                self.assertTrue(val2)
                pbar.update(1)
            pbar.close()

            
if __name__ == '__main__':
    unittest.main()
