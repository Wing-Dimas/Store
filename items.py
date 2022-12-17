class Items():
    __items = []
    __bayar = 0
    @staticmethod
    def getItems()->list[list]:
        return Items.__items

    @staticmethod
    def clear():
        Items.__items.clear()

    @staticmethod
    def add(item:list):
        Items.__items.append(item)

    @staticmethod
    def replace(ind: int, data: list):
        Items.__items[ind] = data

    @staticmethod
    def remove(ind: int):
        Items.__items.pop(ind)

    @staticmethod
    def show():
        print(Items.__items)

    @staticmethod
    def getBayar():
        return Items.__bayar
    
    @staticmethod
    def setBayar(bayar):
        Items.__bayar = bayar


