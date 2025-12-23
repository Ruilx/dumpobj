import sys

print(sys.path)

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


    print("\n".join(dump(A())))
