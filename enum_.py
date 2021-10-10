class EnumHolder:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self): return self.name
    def __eq__(self, a): return self.value == a

class Enum:
    def __init__(self, *args):
        self.i = 0
        for i in args:
            setattr(self, i, EnumHolder(i, self.auto()))

    def auto(self):
        self.i += 1
        return self.i - 1

    def __getitem__(self, a):
        return getattr(self, a)
