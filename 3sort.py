'''
Если отвечать на вопрос серьезно, то лучше всего себя покажут встроенные
sorted() и .sort(). Timsort, разработанный Тимом Питерсом, разбивает массив
на набор подмножеств, сортирует и обьединяет их в несколько этапов.

Начиная с Python 3.11, данный алгоритм был доработан и получил название
Powersort. Он использует двоичные деревья поиска для адаптивной сортировки.
Определяет оптимальный порядок обьединения в процессе. Сохраняет среднюю
сложность Timsort O(n log n).

Однако, если требуется написать алгоритм самостоятельно, я выберу Quicksort.
Его легко реализовать и в сценариях, где данные случайны, он показывает себя
лучше Powersort и других алгоритмов слияния. Quicksort также требует меньше
памяти и времени для небольших массивов. Также обладает средней сложностью
O(n log n). Но в случае плохой стартовой позиции - O(n^2), чего мы попытаемся
избежать, определяя ее случайным образом. Стандартная библиотека C++ использует
Introsort, который опирается на Quicksort и Heapsort.

Работа быстрой сортировки заключается в следующем:
1) Выбирается некоторый опорный элемент массива;
2) Элементы меньше опорного перемещаются перед ним, большие - после;
3) Тоже самое рекурсивно выполняется для получившихся последовательностей.

Условие задачи - достижение лучшей скорости. Так что будем изменять отправленный
в функцию список, а не создавать новый. Отсутствие выделения новой памяти даст
нам дополнительные 10-20% производительности (сравнение скорости sort и sorted).
'''
import random


def quickSort(data: list[int], start: int = 0, stop: int = -1) -> None:
    # перевести значение для конца в положительный индекс
    if stop < 0:
        stop = len(data) + stop

    # уже отсортированные последовательности не обрабатываются
    if start >= stop:
        return

    # пытаемся угадать хорошую стартовую позиции
    pivot = data[random.randint(start, stop)]

    # разбиение на подпоследовательности
    substart, substop = start, stop

    while substart <= substop:
        # индексы "застревают", когда не выполняется условие
        while data[substart] < pivot:
            substart += 1
        while data[substop] > pivot:
            substop -= 1
        # Начало не догнало конец, значит между ними есть неотсортиванные
        # элементы. А так как сравнение происходит с другим элементом этого
        # же отрезка, застрявшие значения надо просто поменять местами.
        if substart <= substop:
            data[substart], data[substop] = data[substop], data[substart]
            # не застреваем на элементах равных опорному
            substart, substop = substart + 1, substop - 1

    # выбираем в полученных отрезках новые опорные точки и повторяем
    # пока все элементы массива не будут идти в порядке возрастания
    quickSort(data, start, substop)
    quickSort(data, substart, stop)


if __name__ == "__main__":

    # генерируем псевдослучайные данные
    data = []
    for i in range(100):
        data.append(random.randint(-500, 500))
    print(data, "\n")

    # сортируем
    quickSort(data)
    print(data)
