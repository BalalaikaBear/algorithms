import logging
from typing import Optional, Any, Iterable, Callable


class Node:
    def __init__(self, value: Any):
        self.data: Any = value
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.height: int = 1  # высота узла

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.data!r})"

    def __repr__(self) -> str:
        return f"<{self}>"


class AVLTree:
    def __init__(self,
                 data: Optional[Iterable] = None,
                 *,
                 key: Optional[Callable] = None,
                 rewrite: bool = False) -> None:
        self.root: Optional[Node] = None  # корень дерева
        self.rewrite = rewrite

    def insert(self, array: Iterable) -> None:
        """Добавление последовательности в дерево.

        :param array: Последовательность
        """
        for value in array:
            self.append(value)

    def append(self, value: int) -> None:
        """Добавление объекта в дерево.

        :param value: Любой объект, имеющий сравнивающие методы.
        """
        self.root = self._append(self.root, value)

    def _append(self, node: Optional[Node], value: int) -> Node:
        """Рекурсивная функция добавления объекта в дерево.

        :param node: Проверяемый узел.
        :param value: Добавляемый объект.
        :return: Возвращает корень дерева.
        """
        if not node:
            new_node = Node(value)
            logging.info("Создание узла {}".format(new_node))
            return new_node

        if self.rewrite and value == node.data:
            new_node = Node(value)
            logging.info("Перезаписывание значения в узел {}".format(new_node))
            return new_node
        elif value < node.data:
            node.left = self._append(node.left, value)
        else:
            node.right = self._append(node.right, value)

        return self._balance(node)

    def _balance(self, node: Node) -> Node:
        """Балансировка дерева

        :param node: Верхний узел дерева.
        :return: Возвращает новый верхний узел.
        """
        self._update_height(node)
        bf = self._balance_factor(node)

        # левый перекос
        if bf > 1:
            if self._balance_factor(node.left) < 0:
                logging.info("Левый поворот узла {}".format(node.left))
                node.left = self._rotate_left(node.left)  # большой правый поворот
            logging.info("Правый поворот узла {}".format(node))
            return self._rotate_right(node)

        # правый перекос
        if bf < -1:
            if self._balance_factor(node.right) > 0:
                logging.info("Правый поворот узла {}".format(node.right))
                node.right = self._rotate_right(node.right)  # большой левый поворот
            logging.info("Левый поворот узла {}".format(node))
            return self._rotate_left(node)

        return node

    def _update_height(self, node: Optional[Node]) -> None:
        """Обновление высоты узла

        :param node: Обновляемый узел.
        """
        if node:
            height = 1 + max(self._height(node.left), self._height(node.right))
            node.height = height

    @staticmethod
    def _height(node: Optional[Node]) -> int:
        """Определение высоты узла.

        :param node: Узел дерева.
        :return: Возвращает сохраненную высоту узла. Если узел не создан - возвращает 0.
        """
        return node.height if node else 0

    def _balance_factor(self, node: Optional[Node]) -> int:
        """Разница между высотой левого и правого поддерева у конкретного узла.

        :param node: Узел дерева.
        :return: Возвращает коэффициент балансировки.
        """
        return self._height(node.left) - self._height(node.right) if node else 0

    def _rotate_left(self, parent: Node) -> Node:
        """Левый поворот ветви дерева

        :param parent: Верхний узел дерева.
        :return: Возвращает новый верхний узел.
        """
        new_parent: Node = parent.right
        sub_branch: Optional[Node] = new_parent.left

        new_parent.left = parent
        parent.right = sub_branch

        self._update_height(parent)
        self._update_height(new_parent)

        return new_parent

    def _rotate_right(self, parent: Node) -> Node:
        """Правый поворот ветви дерева

        :param parent: Верхний узел дерева.
        :return: Возвращает новый верхний узел.
        """
        new_parent: Node = parent.left
        sub_branch: Optional[Node] = new_parent.right

        new_parent.right = parent
        parent.left = sub_branch

        self._update_height(parent)
        self._update_height(new_parent)

        return new_parent

    def print(self) -> None:
        """Удобное отображение дерева в командной строке"""
        self._print_recursion(self.root, 0)

    def _print_recursion(self, node, depth=0, prefix='\033[0mRoot: ') -> None:
        """Рекурсивная функция для удобного отображения дерева в командной строке"""
        if node is not None:
            print('\033[90m' + "|   " * (depth - 1) + prefix + '\033[92m' + str(node.data) + '\033[0m')
            if node.left or node.right:
                self._print_recursion(node.left, depth + 1, '├-- \033[0mL: ')
                self._print_recursion(node.right, depth + 1, '├-- \033[0mR: ')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        filemode='w',
                        filename='trees_log.txt',
                        encoding='UTF-8',
                        format='LOGGING_LEVEL: %(levelno)s - %(message)s')

    r = AVLTree(rewrite=True)
    list_ = [10, 20, 3, 7, 8, 9, 1, 1, 1, 1]

    r.insert(list_)
    r.print()
    print(r.root)
