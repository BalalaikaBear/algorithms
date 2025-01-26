def summ(array: list) -> int:
    """Рекурсивная функция, суммирующая элементы в списке"""
    if not array:  # if _list == []:
        return 0
    else:
        return array[0] + summ(array[1:])


def count(array: list) -> int:
    """Рекурсивная функция, возвращающая количество элементов в списке"""
    if not array:
        return 0
    else:
        return 1 + count(array[1:])


def maximum(array: list) -> int | None:
    """Рекурсивная функция, возвращающая максимальное """
    if not array:
        return None
    else:
        _max = array[0]
        _max_in_list = maximum(array[1:])
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


def quick_sort(array: list) -> list:
    """Рекурсивная функция сортировки списка (быстрая сортировка)"""
    if len(array) < 2:
        return array
    else:
        pivot = array[0]
        less = [i for i in array[1:] if i < pivot]
        greater = [i for i in array[1:] if i > pivot]
        return quick_sort(less) + [pivot] + quick_sort(greater)


if __name__ == '__main__':
    print(summ([1, 2, 3, 10, -2]))
    print(count([1, 3, 4, 1]))
    print(maximum([-3, -2, -1]))
    print(bin_search([1, 2, 4, 6, 11, 13, 58, 192], 192))
    print(quick_sort([4, 12, -48, 0, 1]))
