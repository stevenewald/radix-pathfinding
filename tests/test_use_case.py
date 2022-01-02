import unittest
import time
import pyradix
from tqdm import tqdm
class testUseCase(unittest.TestCase):
    def test_usecase1(self):
        dict1 = pyradix.get_dict("C:/Users/steve/Desktop/wordgame_nongit/Dictionaries/english_large.txt")
        with tqdm(total=2) as pbar:
            pbar.set_description("Loading test trees")
            pbar.update(1)
            radix = pyradix.words_to_tree(dict1)
            pyradix.optimize_tree(radix)
            pbar.update(2)
            pbar.close()
        wordlist = "abcdefghijklmnop"
        words = pyradix.wordPathfinding(False, radix, wordlist)
        words = words[len(words)-15:len(words)]
        self.assertGreater(len(words), 10)
        nonradix = pyradix.words_to_tree(dict1)
        wordlistx = ["testing", "gjkajkgr", "sgrlkgsjns", "egjrgjrdgk", "w2rs", "1", "", "klgksl", "test", "something", "apdpdfn"]
        for word in wordlistx:
            pyradix.add_word(nonradix, word)
        for word in wordlistx:
            val = pyradix.check_if_word(nonradix, word, False)
            self.assertTrue(val)

            
if __name__ == '__main__':
    unittest.main()
