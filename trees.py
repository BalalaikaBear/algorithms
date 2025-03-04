import logging
from typing import Optional, Any, Iterable, Callable, Generator


class Node:
    """Узел для АВЛ-дерева"""

    def __init__(self, value: Any):
        self.data: Any = value
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.height: int = 1  # высота узла

    def __hash__(self) -> int:
        return hash((self.data, self.left, self.right))

    def __bool__(self) -> bool:
        return True if self.data is not None else False

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.data!r})"

    def __repr__(self) -> str:
        return f"<{self}>"


class AVLTree:
    """Сбалансированное по высоте двоичное дерево поиска"""

    def __init__(self,
                 data: Optional[Iterable] = None,
                 *,
                 key: Optional[Callable] = None,
                 rewrite: bool = False) -> None:
        self.root: Optional[Node] = None  # корень дерева
        self.rewrite = rewrite
        self._len: int = 0

        if data:
            self.insert(data)

    def insert(self, iterable: Iterable) -> None:
        """Добавление последовательности в дерево.

        :param iterable: Последовательность
        """
        for value in iterable:
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
        :return: Возвращает корневой узел дерева.
        """
        if not node:
            new_node = Node(value)
            logging.info("Создание узла {}".format(new_node))
            self._len += 1
            return new_node

        if self.rewrite and value == node.data:
            node.data = value
            logging.info("Перезаписывание значения в узел {}".format(node))
            return node
        elif value < node.data:
            node.left = self._append(node.left, value)
        else:
            node.right = self._append(node.right, value)

        return self._balance(node)

    def _balance(self, node: Node) -> Node:
        """Балансировка дерева

        :param node: Узел дерева.
        :return: Возвращает узел ``node`` со сбалансированными ветвями.
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
        :return: Возвращает новый верхний узел ``node``.
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
        :return: Возвращает новый верхний узел ``node``.
        """
        new_parent: Node = parent.left
        sub_branch: Optional[Node] = new_parent.right

        new_parent.right = parent
        parent.left = sub_branch

        self._update_height(parent)
        self._update_height(new_parent)

        return new_parent

    def delete(self, value: Any) -> None:
        """Удалить объект из дерева.

        :param value: Объект для удаления из дерева
        """
        self.root = self._delete(self.root, value)

    def _delete(self, node: Optional[Node], value: Any) -> Node:
        """Рекурсивная функция удаления узла из дерева по введенному значению.

        :param node: Проверяемый узел.
        :param value: Значение для удаления из дерева.
        :return: Возвращает перезаписанный (корневой) узел ``node``.
        """
        if node is None:
            raise ValueError(f'value {value} is not in {self}')

        if value < node.data:
            node.left = self._delete(node.left, value)
        elif value > node.data:
            node.right = self._delete(node.right, value)
        else:
            # узел с одним ребенком
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # замена найденного значения минимальным значением из правого поддерева
            new_node = self._min_value_node(node.right)
            node.data = new_node.data
            logging.info("Удаление значения {0}. Замена {0} на {1}".format(value, node.data))
            node.right = self._delete(node.right, node.data)
            self._len -= 1

        return self._balance(node)

    def __contains__(self, item: Any) -> bool:
        """Поиск объекта/значения в дереве.

        :param item: Объект/значение для поиска.
        :return: Возвращает ``True`` при наличии объекта в дереве, иначе возвращает ``False``.
        """
        try:
            self._find_value(self.root, item)
            return True
        except ValueError:
            return False

    def _find_value(self, node: Optional[Node], value: Any) -> Node:
        """Рекурсивный поиск объекта/значения в дереве.

        :param node: Узел, в котором осуществляется поиск.
        :param value: Объект/значение для поиска.
        :raise ValueError: Значение не найдено.
        :return: Узел ``node`` с необходимым значением.
        """
        if node is None:
            raise ValueError(f'value {value} is not in {self}')

        if value < node.data:
            self._find_value(node.left, value)
        elif value > node.data:
            self._find_value(node.right, value)
        else:
            logging.info("Значение {} найдено".format(value))
            return node

    def min_value(self) -> Any:
        """Минимальное значение в дереве.

        :return: Возвращает минимальное значение.
        """
        return self._min_value_node(self.root).data

    def max_value(self) -> Any:
        """Максимальное значение в дереве.

        :return: Возвращает максимальное значение.
        """
        return self._max_value_node(self.root).data

    @staticmethod
    def _min_value_node(node: Node) -> Node:
        """Поиск минимального значения.

        :param node: Узел начала поиска.
        :return: Узел ``node`` с минимальным значением.
        """
        while node.left:
            node = node.left
        return node

    @staticmethod
    def _max_value_node(node: Node) -> Node:
        """Поиск максимального значения.

        :param node: Узел начала поиска.
        :return: Узел ``node`` с максимальным значением.
        """
        while node.right:
            node = node.right
        return node

    def clear(self) -> None:
        """Очистка дерева"""
        self.root = None
        self._len = 0

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

    def __iter__(self) -> Generator[Any, None, None]:
        """Обход элементов дерева в порядке возрастания.

        :return: ``Generator`` элементов дерева в порядке возрастания.
        """
        yield from self._in_order(self.root)

    def _in_order(self, node: Optional[Node]) -> Generator[Any, None, None]:
        """Рекурсивный обход элементов дерева в порядке возрастания.

        :param node: Узел начала обхода.
        :return: ``Generator`` элементов дерева в порядке возрастания.
        """
        if node:
            yield from self._in_order(node.left)
            yield node.data
            yield from self._in_order(node.right)

    def reversed(self) -> Generator[Any, None, None]:
        """Обход элементов дерева в порядке убывания.

        :return: ``Generator`` элементов дерева в порядке убывания.
        """
        return self.__reversed__()

    def __reversed__(self) -> Generator[Any, None, None]:
        """Обход элементов дерева в порядке убывания.

        :return: ``Generator`` элементов дерева в порядке убывания.
        """
        yield from self._in_reverse_order(self.root)

    def _in_reverse_order(self, node: Optional[Node]) -> Generator[Any, None, None]:
        """Рекурсивный обход элементов дерева в порядке убывания.

        :param node: Узел начала обхода.
        :return: ``Generator`` элементов дерева в порядке убывания.
        """
        if node:
            yield from self._in_reverse_order(node.right)
            yield node.data
            yield from self._in_reverse_order(node.left)

    def __hash__(self) -> int:
        return hash(self.root)

    def __bool__(self) -> bool:
        return bool(self.root)

    def __len__(self) -> int:
        return self._len

    def __str__(self) -> str:
        return f"{type(self).__name__}({str(list(self))[1:-1]})"

    def __repr__(self) -> str:
        return f"<{type(self).__name__}({self._len})>"


if __name__ == '__main__':
    import random

    logging.basicConfig(level=logging.INFO,
                        filemode='w',
                        filename='trees_log.txt',
                        encoding='UTF-8',
                        format='LOGGING_LEVEL: %(levelno)s - %(message)s')

    random_list = [random.randint(-20, 100) for _ in range(10)]
    problem_cases = [
        [-17, -12, -12, 6, 14, 66, 75, 85, 94, 95],
        [-15, -3, 4, 4, 14, 48, 54, 55, 59, 70],
        [3, 3, 5, 13, 26, 46, 46, 53, 65, 80]
    ]
    random_list = problem_cases[0]
    print('random_list: ', sorted(random_list))
    r = AVLTree(random_list, rewrite=True)
    print('list_in_tree:', list(r))
    r.print()
    r.delete(-12)
    r.print()
