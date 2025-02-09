import logging
from typing import Any, Optional, Iterable, Callable


class BinaryTree:
    """Бинарная древовидная структура данных."""

    class BinaryNode:
        """Тип данных, хранящий значение, и информацию о детях."""

        def __init__(self, value: Any) -> None:
            self.data = value
            self.l_child = None
            self.r_child = None
            self.balance_factor: int = 0  # коэффициент балансировки

        def __str__(self) -> str:
            return f"{type(self).__name__}({self.data!r})"

        def __repr__(self) -> str:
            return f"<{self}>"

    def __init__(self,
                 data: Optional[Iterable] = None,
                 key: Optional[Callable] = None) -> None:
        self.root = None

    def append(self, value: Any) -> None:
        """Добавление значения в дерево.

        :param value: Любой объект, имеющий сравнивающие методы.
        """
        if self.root is None:
            self.root = self.BinaryNode(value)
            logging.info("Запись значения в корневую ноду {}".format(self.root))
        else:
            try:
                self._add_recursion(self.root, value)
            except ValueError:
                pass

    def _add_recursion(self,
                       parent: Optional[BinaryNode],
                       value: Any) -> None:
        """Рекурсивная функция для добавления значения в свободное место.

        :param parent: Проверяемая нода в дереве.
        :param value: Любой объект, имеющий сравнивающие методы.
        """
        if value < parent.data:  # левый ребенок
            direction_attribute = 'l_child'
            balance_change = -1
        elif value > parent.data:  # правый ребенок
            direction_attribute = 'r_child'
            balance_change = 1
        else:  # совпадение значения
            raise ValueError('Object {} is already exist in {}'.format(value, type(self).__name__))

        child = getattr(parent, direction_attribute)

        if child is None:
            setattr(parent, direction_attribute, self.BinaryNode(value))
            parent.balance_factor += balance_change
            logging.info("Запись значения в ноду {} родителя {}".format(getattr(parent, direction_attribute), parent))
        else:
            self._add_recursion(child, value)
            parent.balance_factor += balance_change
            if parent.balance_factor > 1 or parent.balance_factor < -1:
                logging.info("Балансировка дерева в ноде {}. Замена Родителя на {}".format(parent,
                                                                                           getattr(parent,
                                                                                                   direction_attribute)))

    def print(self) -> None:
        """Удобное отображение дерева в командной строке"""
        self._print_recursion(self.root, 0)

    def _print_recursion(self, node, depth=0, prefix='\033[0mRoot: ') -> None:
        """Рекурсивная функция для удобного отображения дерева в командной строке"""
        if node is not None:
            print('\033[90m' + "|   " * (depth - 1) + prefix + '\033[92m' + str(node.data) + '(BF={})'.format(
                node.balance_factor) + '\033[0m')
            if node.l_child or node.r_child:
                self._print_recursion(node.l_child, depth + 1, '├-- \033[0mL: ')
                self._print_recursion(node.r_child, depth + 1, '├-- \033[0mR: ')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        filemode='w',
                        filename='trees_log.txt',
                        encoding='UTF-8',
                        format='LOGGING_LEVEL: %(levelno)s - %(message)s')

    r = BinaryTree()
    r.append(10)
    r.append(11)
    r.append(3)
    r.append(7)
    r.append(8)
    r.append(9)
    r.append(9)
    r.print()
