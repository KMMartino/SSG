import unittest

from block_functions import block_to_block_type
from block_functions import BlockType

class Testmd(unittest.TestCase):

    def test_headings(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEAD)
        self.assertEqual(block_to_block_type("###### Level 6"), BlockType.HEAD)
        self.assertEqual(block_to_block_type("####### Too Many"), BlockType.PAR)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PAR)

    def test_code_blocks(self):
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```code\n```"), BlockType.PAR)

    def test_quotes(self):
        self.assertEqual(block_to_block_type("> Single line"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Quote\nNot a quote"), BlockType.PAR)

    def test_unordered_lists(self):
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.UL)
        self.assertEqual(block_to_block_type("-Item No Space"), BlockType.PAR)
        self.assertEqual(block_to_block_type("* Asterisk not supported"), BlockType.PAR) 

    def test_ordered_lists(self):
        self.assertEqual(block_to_block_type("1. First\n2. Second"), BlockType.OL)
        self.assertEqual(block_to_block_type("1. First\n3. Skipped"), BlockType.PAR)
        self.assertEqual(block_to_block_type("2. Missed"), BlockType.PAR)

    def test_paragraphs(self):
        self.assertEqual(block_to_block_type("Just a normal sentence."), BlockType.PAR)
        self.assertEqual(block_to_block_type("  # Indented heading"), BlockType.PAR)


if __name__ == "__main__":
    unittest.main()