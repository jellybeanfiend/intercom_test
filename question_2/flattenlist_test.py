import unittest
import flattenlist

class TestFlattenList(unittest.TestCase):

    def test_empty_list(self):
        self.assertListEqual([], flattenlist.flatten_list([[], []]))

    def test_flat_list(self):
        input_list = [1, 2, 3]
        self.assertListEqual(flattenlist.flatten_list(input_list), input_list)

    def test_depth_one(self):
        input_list = [1, [1, 2], 3]
        expected_output = [1, 1, 2, 3]
        self.assertListEqual(flattenlist.flatten_list(input_list),
                             expected_output)

    def test_depth_two(self):
        input_list = [1, [2, [3], 4], 5]
        expected_output = [1, 2, 3, 4, 5]
        self.assertListEqual(flattenlist.flatten_list(input_list),
                             expected_output)

    def test_depth_three(self):
        input_list = [[[[1]]]]
        expected_output = [1]
        self.assertListEqual(flattenlist.flatten_list(input_list),
                             expected_output)

    def test_different_types(self):
        input_list = [1, ['a', 2], 'b']
        expected_output = [1, 'a', 2, 'b']
        self.assertListEqual(flattenlist.flatten_list(input_list),
                             expected_output)

if __name__ == "__main__":
    unittest.main()
