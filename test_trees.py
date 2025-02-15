import random
import unittest

from trees import AVLTree


class TestAVLTree(unittest.TestCase):
    def test_append(self):
        tree = AVLTree()
        tree.append(40)
        tree.append(30)
        tree.append(20)
        tree.append(0)

        self.assertEqual(tree.root.data, 30)
        self.assertEqual(tree.root.left.data, 20)
        self.assertEqual(tree.root.right.data, 40)
        self.assertEqual(tree.root.left.left.data, 0)

    def test_insert(self):
        tree = AVLTree()
        tree.insert([10, 20, 3, 7, 8, 9, 1])

        self.assertEqual(tree.root.data, 8)
        self.assertEqual(tree.root.left.data, 3)
        self.assertEqual(tree.root.left.left.data, 1)
        self.assertEqual(tree.root.left.left.left, None)
        self.assertEqual(tree.root.left.left.right, None)
        self.assertEqual(tree.root.left.right.data, 7)
        self.assertEqual(tree.root.left.right.left, None)
        self.assertEqual(tree.root.left.right.right, None)
        self.assertEqual(tree.root.right.data, 10)
        self.assertEqual(tree.root.right.left.data, 9)
        self.assertEqual(tree.root.right.left.left, None)
        self.assertEqual(tree.root.right.left.right, None)
        self.assertEqual(tree.root.right.right.data, 20)
        self.assertEqual(tree.root.right.right.left, None)
        self.assertEqual(tree.root.right.right.right, None)

    def test_list(self):
        tested_list = [-321, 23, 44, 0, 100, -8]
        sorted_list = sorted(tested_list)
        reversed_list = sorted(tested_list, reverse=True)

        tree = AVLTree()
        tree.insert(tested_list)

        self.assertEqual(list(tree), sorted_list)
        self.assertEqual(list(tree.reversed()), reversed_list)
        self.assertEqual(list(reversed(tree)), reversed_list)

    def test_tuple(self):
        tested_tuple = (-1, -2, -3, 5.2, 3 / 5, 0.000001, 9)
        sorted_tuple = tuple(sorted(tested_tuple))
        reversed_tuple = tuple(sorted(tested_tuple, reverse=True))

        tree = AVLTree()
        tree.insert(tested_tuple)

        self.assertEqual(tuple(tree), sorted_tuple)
        self.assertEqual(tuple(tree.reversed()), reversed_tuple)
        self.assertEqual(tuple(reversed(tree)), reversed_tuple)

    def test_init(self):
        tested_list = [3.1415, 10_000_020, 1.0, 1.0001, -999]
        sorted_list = sorted(tested_list)
        reversed_list = sorted(tested_list, reverse=True)

        tree = AVLTree(tested_list)

        self.assertEqual(list(tree), sorted_list)
        self.assertEqual(list(tree.reversed()), reversed_list)
        self.assertEqual(list(reversed(tree)), reversed_list)

    def test_find(self):
        # целые числа
        integer_set_A = {random.randint(-10_000_000, 10_000_000) for _ in range(100)}
        integer_set_B = {random.randint(-10_000_000, 10_000_000) for _ in range(50)}
        difference_integer_set = integer_set_B - integer_set_A

        tree = AVLTree(rewrite=True)
        tree.insert(integer_set_A)

        for i, value in enumerate(integer_set_A):
            self.assertTrue(value in tree, f'iteration {i}: {value} should be in {tree}')

        for i, value in enumerate(difference_integer_set):
            self.assertFalse(value in tree, f"iteration {i}: {value} shouldn't be in {tree}")

        # числа с плавающей точкой
        float_set_A = {random.random() * 10_000_000 for _ in range(100)}
        float_set_B = {random.random() * 10_000_000 for _ in range(50)}
        difference_float_set = float_set_B - float_set_A

        tree = AVLTree(rewrite=True)
        tree.insert(float_set_A)

        for i, value in enumerate(float_set_A):
            self.assertTrue(value in tree, f'iteration {i}: {value} should be in {tree}')

        for i, value in enumerate(difference_float_set):
            self.assertFalse(value in tree, f"iteration {i}: {value} shouldn't be in {tree}")


if __name__ == '__main__':
    unittest.main()
