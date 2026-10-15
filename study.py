"""Кольцевой дек фиксированной вместимости и интерактивное меню."""

class Deque:
    def __init__(self, size):
        if size <= 0:
            raise ValueError("Размер дека должен быть положительным")
        self.max_size = size
        self.array = [None] * size
        self.head = 0
        self.tail = 0
        self.count = 0
    
    def is_empty(self):
        return self.count == 0
    
    def is_full(self):
        return self.count == self.max_size
    
    def push_front(self, value):
        if self.is_full():
            print("Дек переполнен!")
            return
        
        self.head = (self.head - 1) % self.max_size
        self.array[self.head] = value
        self.count += 1
        print(f"Добавлено {value} в начало")
    
    def push_back(self, value):
        if self.is_full():
            print("Дек переполнен!")
            return
        
        self.array[self.tail] = value
        self.tail = (self.tail + 1) % self.max_size
        self.count += 1
        print(f"Добавлено {value} в конец")
    
    def pop_front(self):
        if self.is_empty():
            print("Дек пуст!")
            return None
        
        value = self.array[self.head]
        self.array[self.head] = None
        self.head = (self.head + 1) % self.max_size
        self.count -= 1
        print(f"Удалено {value} из начала")
        return value
    
    def pop_back(self):
        if self.is_empty():
            print("Дек пуст!")
            return None
        
        self.tail = (self.tail - 1) % self.max_size
        value = self.array[self.tail]
        self.array[self.tail] = None
        self.count -= 1
        print(f"Удалено {value} из конца")
        return value
    
    def get(self, index):
        if index < 0 or index >= self.count:
            print("Неверный индекс!")
            return None
        
        real_index = (self.head + index) % self.max_size
        return self.array[real_index]
    
    def show(self):
        if self.is_empty():
            print("Дек пуст")
            return
        
        elements = []
        for i in range(self.count):
            idx = (self.head + i) % self.max_size
            elements.append(str(self.array[idx]))
        
        print("Дек: [" + ", ".join(elements) + "]")
        print(f"Размер: {self.count}/{self.max_size}")

def menu():
    print("1. Добавить в начало")
    print("2. Добавить в конец")
    print("3. Удалить из начала")
    print("4. Удалить из конца")
    print("5. Посмотреть по индексу")
    print("6. Показать дек")
    print("0. Выйти")


def main():
    size = int(input("Введите размер дека: "))
    dq = Deque(size)
    print(f"Дек создан на {size} элементов\n")
    
    while True:
        menu()
        choice = input("Выберите действие: ")
        
        if choice == "0":
            print("До свидания!")
            break
        
        elif choice == "1":
            val = int(input("Число: "))
            dq.push_front(val)
        
        elif choice == "2":
            val = int(input("Число: "))
            dq.push_back(val)
        
        elif choice == "3":
            dq.pop_front()
        
        elif choice == "4":
            dq.pop_back()
        
        elif choice == "5":
            idx = int(input("Индекс: "))
            res = dq.get(idx)
            if res is not None:
                print(f"Элемент: {res}")
        
        elif choice == "6":
            dq.show()
        
        else:
            print("Неверный выбор!")
        
        input("\nНажмите Enter...")


if __name__ == "__main__":
    main()
