

class Component:
    def __init__(self, name):
        self.name = name


    def mut(self, property : str, value):
        vars(self)[property]=value
        