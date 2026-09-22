class Person:
    def __init__(self):
        self.name = "John"
        self.age = 36
        self.string = str(int("4F", 16))
        self.country = "Norway"
    def set_age(self):
        setattr(self, 'age', 40)
    def set_desh(self):
        setattr(self, 'desh', "Norway")

dude = Person()
dude.set_desh()
