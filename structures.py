"""Учебные реализации массива, связного списка и АВЛ-дерева."""
from dataclasses import dataclass


class Array:
    """Массив фиксированной вместимости; допустимые индексы: 0..len-1."""

    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("Вместимость должна быть положительной")
        self._data = [None] * capacity
        self._size = 0

    def __len__(self):
        return self._size

    def _check(self, index):
        if not 0 <= index < self._size:
            raise IndexError("Индекс вне массива")

    def __getitem__(self, index):
        self._check(index)
        return self._data[index]

    def __setitem__(self, index, value):
        self._check(index)
        self._data[index] = value

    def __iter__(self):
        for i in range(self._size):
            yield self._data[i]

    def append(self, value):
        self.insert(self._size, value)

    def insert(self, index, value):
        if not 0 <= index <= self._size:
            raise IndexError("Индекс вне массива")
        if self._size == len(self._data):
            raise OverflowError("Массив заполнен")
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1

    def pop(self, index=None):
        if index is None:
            index = self._size - 1
        self._check(index)
        value = self._data[index]
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._size -= 1
        self._data[self._size] = None
        return value


@dataclass
class _ListNode:
    value: object
    next: object = None


class LinkedList:
    """Односвязный список с добавлением с обоих концов."""

    def __init__(self):
        self.head = self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

    def append(self, value):
        node = _ListNode(value)
        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self._size += 1

    def prepend(self, value):
        self.head = _ListNode(value, self.head)
        if self.tail is None:
            self.tail = self.head
        self._size += 1

    def get(self, index):
        if not 0 <= index < self._size:
            raise IndexError("Индекс вне списка")
        node = self.head
        for _ in range(index):
            node = node.next
        return node.value

    def remove(self, value):
        """Удалить первое вхождение; ValueError, если значения нет."""
        previous, node = None, self.head
        while node is not None:
            if node.value == value:
                if previous is None:
                    self.head = node.next
                else:
                    previous.next = node.next
                if node is self.tail:
                    self.tail = previous
                self._size -= 1
                return
            previous, node = node, node.next
        raise ValueError("Значение не найдено")


@dataclass
class _AVLNode:
    key: object
    left: object = None
    right: object = None
    height: int = 1


def _height(node):
    return node.height if node else 0


def _update(node):
    node.height = 1 + max(_height(node.left), _height(node.right))


def _rotate_right(node):
    root = node.left
    node.left = root.right
    root.right = node
    _update(node)
    _update(root)
    return root


def _rotate_left(node):
    root = node.right
    node.right = root.left
    root.left = node
    _update(node)
    _update(root)
    return root


def _balance(node):
    _update(node)
    factor = _height(node.left) - _height(node.right)
    if factor > 1:
        if _height(node.left.left) < _height(node.left.right):
            node.left = _rotate_left(node.left)
        return _rotate_right(node)
    if factor < -1:
        if _height(node.right.right) < _height(node.right.left):
            node.right = _rotate_right(node.right)
        return _rotate_left(node)
    return node


class AVLTree:
    """Сбалансированное дерево уникальных сравнимых ключей."""

    def __init__(self):
        self.root = None

    def insert(self, key):
        def visit(node):
            if node is None:
                return _AVLNode(key)
            if key < node.key:
                node.left = visit(node.left)
            elif key > node.key:
                node.right = visit(node.right)
            else:
                return node
            return _balance(node)
        self.root = visit(self.root)

    def __contains__(self, key):
        node = self.root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def __iter__(self):
        def walk(node):
            if node:
                yield from walk(node.left)
                yield node.key
                yield from walk(node.right)
        return walk(self.root)

    def remove(self, key):
        """Удаление ключа; KeyError, если ключ отсутствует."""
        def visit(node, target):
            if node is None:
                raise KeyError(target)
            if target < node.key:
                node.left = visit(node.left, target)
            elif target > node.key:
                node.right = visit(node.right, target)
            else:
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                successor = node.right
                while successor.left:
                    successor = successor.left
                node.key = successor.key
                node.right = visit(node.right, successor.key)
            return _balance(node)
        self.root = visit(self.root, key)
