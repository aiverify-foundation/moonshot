from io import TextIOWrapper

import ijson


class GeneratorIO:
    def __init__(self, file: TextIOWrapper, item_path: str):
        self.file = file
        self.generator = ijson.items(self.file, item_path)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self.generator)
        except StopIteration:
            self.file.close()
            raise StopIteration
