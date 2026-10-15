import contextlib
import io
import random
import unittest
from collections import deque

from structures import Array, LinkedList, AVLTree
from study import Deque
from sorting import bubble_sort, quick_sort


class ArrayTests(unittest.TestCase):
    def test_operations(self):
        a = Array(4)
        a.append(2)
        a.insert(0, 1)
        a.insert(2, 4)
        a.insert(2, 3)
        self.assertEqual(list(a), [1, 2, 3, 4])
        a[1] = 20
        self.assertEqual(a[1], 20)
        self.assertEqual(a.pop(1), 20)
        self.assertEqual(a.pop(), 4)
        self.assertEqual(list(a), [1, 3])
        self.assertEqual(len(a), 2)

    def test_boundaries(self):
        for size in (0, -1):
            with self.assertRaises(ValueError):
                Array(size)
        a = Array(1)
        with self.assertRaises(IndexError):
            a.pop()
        a.append(1)
        with self.assertRaises(OverflowError):
            a.append(2)
        for index in (-1, 1):
            with self.assertRaises(IndexError):
                _ = a[index]
            with self.assertRaises(IndexError):
                a[index] = 3
        with self.assertRaises(IndexError):
            a.insert(2, 3)
        self.assertEqual(a.pop(), 1)
        a.append(9)
        self.assertEqual(list(a), [9])


class ListTests(unittest.TestCase):
    def test_operations(self):
        items = LinkedList()
        items.prepend(2)
        items.prepend(1)
        items.append(3)
        items.append(2)
        self.assertEqual(list(items), [1, 2, 3, 2])
        self.assertEqual(items.get(2), 3)
        items.remove(2)
        self.assertEqual(list(items), [1, 3, 2])
        items.remove(1)
        items.remove(2)
        items.remove(3)
        self.assertEqual(len(items), 0)
        self.assertIsNone(items.head)
        self.assertIsNone(items.tail)
        items.append(4)
        self.assertEqual(list(items), [4])

    def test_errors(self):
        items = LinkedList()
        with self.assertRaises(ValueError):
            items.remove(1)
        for index in (-1, 0):
            with self.assertRaises(IndexError):
                items.get(index)


class DequeTests(unittest.TestCase):
    def test_wraparound_and_boundaries(self):
        with contextlib.redirect_stdout(io.StringIO()):
            for capacity in (1, 2, 7):
                actual, expected = Deque(capacity), deque()
                rng = random.Random(42)
                for _ in range(300):
                    operation = rng.choice(('push_front', 'push_back', 'pop_front', 'pop_back'))
                    if operation.startswith('push'):
                        value = rng.randrange(-100, 100)
                        getattr(actual, operation)(value)
                        if len(expected) < capacity:
                            (expected.appendleft if operation == 'push_front' else expected.append)(value)
                    else:
                        result = getattr(actual, operation)()
                        wanted = (expected.popleft() if operation == 'pop_front' else expected.pop()) if expected else None
                        self.assertEqual(result, wanted)
                    self.assertEqual(actual.count, len(expected))
                    self.assertEqual([actual.get(i) for i in range(actual.count)], list(expected))
                    self.assertEqual(actual.is_empty(), not expected)
                    self.assertEqual(actual.is_full(), len(expected) == capacity)
                self.assertIsNone(actual.get(-1))
                self.assertIsNone(actual.get(actual.count))
                actual.show()

    def test_invalid_size(self):
        for size in (0, -2):
            with self.assertRaises(ValueError):
                Deque(size)


class AVLTests(unittest.TestCase):
    def assert_tree(self, tree, expected):
        self.assertEqual(list(tree), sorted(expected))
        def check(node, lower=None, upper=None):
            if node is None:
                return 0
            if lower is not None:
                self.assertGreater(node.key, lower)
            if upper is not None:
                self.assertLess(node.key, upper)
            left = check(node.left, lower, node.key)
            right = check(node.right, node.key, upper)
            self.assertLessEqual(abs(left - right), 1)
            self.assertEqual(node.height, 1 + max(left, right))
            return node.height
        check(tree.root)

    def test_all_rotation_types(self):
        for sequence in ([3, 2, 1], [1, 2, 3], [3, 1, 2], [1, 3, 2]):
            with self.subTest(sequence=sequence):
                tree = AVLTree()
                for key in sequence:
                    tree.insert(key)
                self.assertEqual(tree.root.key, 2)
                self.assert_tree(tree, {1, 2, 3})

    def test_insert_delete_and_duplicates(self):
        tree, expected = AVLTree(), set()
        rng = random.Random(17)
        values = list(range(150))
        rng.shuffle(values)
        for key in values:
            tree.insert(key)
            tree.insert(key)
            expected.add(key)
            self.assertIn(key, tree)
            self.assert_tree(tree, expected)
        self.assertNotIn(-1, tree)
        with self.assertRaises(KeyError):
            tree.remove(-1)
        self.assert_tree(tree, expected)
        rng.shuffle(values)
        for key in values:
            tree.remove(key)
            expected.remove(key)
            self.assertNotIn(key, tree)
            self.assert_tree(tree, expected)
        with self.assertRaises(KeyError):
            tree.remove(0)


class SortingTests(unittest.TestCase):
    def test_examples_and_random_data(self):
        rng = random.Random(7)
        cases = [[], [1], [2, 1], [3] * 50, list(range(100)), list(range(100, -1, -1)), [3, -2, 0, 3, -2], ['b', 'a', 'c']]
        cases += [[rng.randrange(-20, 21) for _ in range(n)] for n in range(80)]
        for sort in (bubble_sort, quick_sort):
            for values in cases:
                with self.subTest(sort=sort.__name__, size=len(values)):
                    original = values.copy()
                    self.assertEqual(sort(values), sorted(values))
                    self.assertEqual(values, original)
                    self.assertEqual(sort(iter(values)), sorted(values))

    def test_quick_sort_large_inputs(self):
        for values in (list(range(5000)), list(range(5000, -1, -1)), [1] * 5000):
            self.assertEqual(quick_sort(values), sorted(values))


if __name__ == '__main__':
    unittest.main()
