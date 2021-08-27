class Foo():

    var = 1
    def __init__(self):
        self.var =

    def bar(self):
        self.var = 11
        print("bar")

    def repr(self, var):
        self.bar()
        print(f"var = {self.var}")

foo = Foo()
foo.repr(10)

