import sys

from dumpobj.formatter.color_formatter import ColorFormatter

from dumpobj import dump, Dump

if __name__ == "__main__":
    class A(object):
        class B:
            ...

        Prop1 = 1

        def __init__(self):
            self.a = 1
            self.b = 1+3j
            self.c = object()
            self.d = A
            self.e = Ellipsis


    d = Dump()
    d.set_formatter(ColorFormatter())
    for i in d.dump(A()):
        print(i)
