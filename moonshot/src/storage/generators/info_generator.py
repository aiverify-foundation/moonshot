from abc import ABC

import ijson


class InfoGenerator(ABC):
    """
    This class is a superclass for generating information from a given file. It uses the ijson library to parse and
    generate items from the JSON file. The class is iterable and each iteration returns the next item from the
    JSON file.

    Attributes:
        file (TextIOWrapper): The file object of the dataset file.
        generator (generator): The ijson generator object.

    Methods:
        __iter__(): Returns the iterator object (self).
        __next__(): Returns the next item from the JSON file. If there are no more items, it closes the file and
                    raises StopIteration.
    """

    def __init__(self, filepath: str, item_path: str):
        self.file = open(filepath, "r", encoding="utf-8")
        self.generator = ijson.items(self.file, item_path)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self.generator)
        except StopIteration:
            self.file.close()
            raise StopIteration
