from __future__ import print_function


class House(object):
    def __init__(self):
        self._house_id = 0
        self._house_name = None

    @property
    def house_id(self):
        print("House get method")
        return self._house_id

    @house_id.setter
    def house_id(self, house_id):
        print("House set method")
        self._house_id = house_id


class Item(House):

    def __init__(self):
        House.__init__(self)
        self._house_id = 2

    @property
    def house_id(self):
        print("override House get method")
        return self._house_id

    @house_id.setter
    def house_id(self, house_id):
        print("override House set method")
        self._house_id = house_id


house = House()
item = Item()
print(house.__dict__)
print(item.__dict__)
hp = house.__dict__
for p in hp:
    if hasattr(item, p):
        print(getattr(item, p, 'y'))

