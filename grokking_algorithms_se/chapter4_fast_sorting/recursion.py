def summ(_list: list) -> int:
    """Рекурсивная функция, суммирующая элементы в списке"""
    if not _list:  # if _list == []:
        return 0
    else:
        return _list[0] + summ(_list[1:])


def count(_list: list) -> int:
    """Рекурсивная функция, возвращающая количество элементов в списке"""
    if not _list:
        return 0
    else:
        return 1 + count(_list[1:])


def maximum(_list: list) -> int | None:
    """Рекурсивная функция, возвращающая максимальное """
    if not _list:
        return None
    else:
        _max = _list[0]
        _max_in_list = maximum(_list[1:])
        if _max_in_list and _max_in_list > _max:
            _max = _max_in_list
        return _max


def bin_search(sorted_list: list, number_to_find: int) -> True:
    """Рекурсивная функция бинарного поиска числа"""
    if sorted_list[0] == number_to_find:
        return True
    elif len(sorted_list) == 1 and sorted_list[0] != number_to_find:
        return False
    else:
        middle = sorted_list[len(sorted_list) // 2]
        if middle == number_to_find:
            return True
        elif middle < number_to_find:
            return bin_search(sorted_list[len(sorted_list) // 2:], number_to_find)
        else:
            return bin_search(sorted_list[:len(sorted_list) // 2], number_to_find)


if __name__ == '__main__':
    print(summ([1, 2, 3, 10, -2]))
    print(count([1, 3, 4, 1]))
    print(maximum([-3, -2, -1]))
    print(bin_search([1, 2, 4, 6, 11, 13, 58, 192], 192))
