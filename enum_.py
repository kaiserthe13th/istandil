class Enum:
    def __init__(self, *args):
        self.i = 0
        for i in args:
            setattr(self, i, self.auto())

    def auto(self):
        self.i += 1
        return self.i - 1

    def __getitem__(self, a):
        return getattr(self, a)
