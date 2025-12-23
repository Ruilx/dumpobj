import sys

print(sys.path)

from dumpobj import dump, Dump

if __name__ == "__main__":
    print("\n".join(dump(None)))
