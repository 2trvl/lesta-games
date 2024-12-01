'''
В задаче не сказано для каких данных используется буфер.
Предположим, это целые числа.

Первый класс использует стандартный список. Получение элемента
по индексу O(1), как и ожидается. Можно хранить числа любого размера.

Недостатком является то, что Питоновские списки являются динамическими
массивами. Для оптимизации скорости аллокации количество созданных ячеек
всегда больше реального числа элементов.

Преимуществом данной вариации является синхронизация перезаписи.
Перезаписывание элемента приводит к обновлению позиции чтения. Это может
использоваться для задач, в которых поток данных непрерывен, что приводит к
частому переполнению буфера. Например, асинхронное приложение, отображающее
динамический график шума, котировок криптовалюты, веса нейронной модели и тд.
'''
class CircularList():

    def __init__(self, size: int):
        self.size = size
        self.head = self.tail = -1
        self.data = [None] * self.size
        self.sync = False

    def put(self, value: int) -> None:
        # значение позиций актуально в момент операции
        self.tail += 1
        if self.tail == self.size:
            self.tail = 0
            # чтение уже не в первый раз не успевает за записью
            if self.sync:
                self.head = 0
            else:
                self.sync = True
        # элемент будет перезаписан, читаем следующую ячейку
        if self.sync and self.tail > self.head:
            self.head = (self.head + 1) % self.size
        self.data[self.tail] = value

    def get(self) -> int | None:
        head = self.head + 1
        value = self.data[head % self.size]
        # значение не пустое, перемещаемся на эту позицию
        if value is not None:
            self.head = head % self.size
            self.data[self.head] = None
            # чтение самостоятельно вернулось в начало
            if head == self.size:
                self.sync = False
        else:
            return None
        # чтение догнало запись, возвращаемся к началу буфера
        if self.head == self.tail:
            self.head = self.tail = -1
        return value


'''
Другой класс использует Питоновские массивы. Значение одного числа определяется
архитектурой/компилятором согласно 5.2.4.2.1 C99 (обычно как минимум 16 бит).
Создание происходит быстрее, занято в 2 раза меньше оперативной памяти, чем list.

Позиции больше не начинаются с -1, они актуальны до вызова методов.
Не синхронизируется перезапись: переполнение буфера приводит к потере данных.
Чтение ориентируется на позицию записи, не может читать дальше. Также чтение
не удаляет значения из буфера.

Такое решение лучше подойдет в ситуациях, когда:
* память ограничена;
* размер/точность данных предсказуемы;
* буфер используется одним рабочим процессом;
* важна скорость и нужен простой кольцевой контейнер.

Пример: хранение текущих настроек или показателей датчиков на микроконтроллере.
'''
from array import array


class CircularArray():

    def __init__(self, size: int):
        self.size = size
        self.head = self.tail = 0
        self.data = array("i", (0, ) * self.size)

    def put(self, value: int) -> None:
        # переполнение, пересоздаем буфер и переходим к его началу
        if self.tail == self.size:
            self.tail = self.head = 0
            self.data = array("i", (0, ) * self.size)
        self.data[self.tail] = value
        self.tail += 1

    def get(self) -> int | None:
        # пока что нечего читать
        if self.head == self.tail:
            return None
        value = self.data[self.head]
        self.head += 1
        return value


if __name__ == "__main__":
    # список
    queue = CircularList(3)

    # массив
    #queue = CircularArray(3)
    #queue.sync = None

    # начало тестирования
    print("PUT (1)")
    queue.put(1)
    print(queue.data)
    print(f"head: {queue.head}, tail: {queue.tail}\n")

    print("PUT (2)")
    queue.put(2)
    print(queue.data)
    print(f"head: {queue.head}, tail: {queue.tail}\n")

    print("PUT (3)")
    queue.put(3)
    print(queue.data)
    print(f"head: {queue.head}, tail: {queue.tail}\n")

    # запись обгоняет чтение
    print("PUT (4)")
    queue.put(4)
    print(queue.data)
    print(f"head: {queue.head}, tail: {queue.tail}")
    print(f"sync: {queue.sync}\n")

    print("PUT (5)")
    queue.put(5)
    print(queue.data)
    print(f"head: {queue.head}, tail: {queue.tail}\n")

    # дважды
    print("PUT (6)")
    queue.put(6)
    print(queue.data)
    print(f"head: {queue.head}, tail: {queue.tail}\n")

    # CircularArray: прочитает значение с начала
    # CircularList: вернется в начало, отключит синхронизацию
    print(f"GET ({queue.get()})")
    print(queue.data)
    print(f"head: {queue.head}, tail: {queue.tail}")
    print(f"sync: {queue.sync}\n")

    # CircularArray: массив пересоздан, чтение установлено в начало
    # CircularList: теперь запись догоняет, но продолжает следить,
    # чтобы чтение не отстало
    print("PUT (7)")
    queue.put(7)
    print(queue.data)
    print(f"head: {queue.head}, tail: {queue.tail}")
    print(f"sync: {queue.sync}\n")

    # последовательные чтение и запись
    print(f"GET ({queue.get()})")
    print(queue.data)
    print(f"head: {queue.head}, tail: {queue.tail}\n")

    print("PUT (8)")
    queue.put(8)
    print(queue.data)
    print(f"head: {queue.head}, tail: {queue.tail}\n")

    print(f"GET ({queue.get()})")
    print(queue.data)
    print(f"head: {queue.head}, tail: {queue.tail}\n")

    print(f"GET ({queue.get()})")
    print(queue.data)
    print(f"head: {queue.head}, tail: {queue.tail}\n")

    print("PUT (9)")
    queue.put(9)
    print(queue.data)
    print(f"head: {queue.head}, tail: {queue.tail}\n")

    print(f"GET ({queue.get()})")
    print(queue.data)
    print(f"head: {queue.head}, tail: {queue.tail}\n")

    # дочитываем все доступные значения
    print(f"GET ({queue.get()})")
    print(queue.data)
    print(f"head: {queue.head}, tail: {queue.tail}")
    print(f"sync: {queue.sync}\n")

    # проверяем, что чтение пустых значений не будет менять позицию
    print(f"GET ({queue.get()})")
    print(queue.data)
    print(f"head: {queue.head}, tail: {queue.tail}\n")

    print(f"GET ({queue.get()})")
    print(queue.data)
    print(f"head: {queue.head}, tail: {queue.tail}\n")
