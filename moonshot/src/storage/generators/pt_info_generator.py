from moonshot.src.storage.generators.info_generator import InfoGenerator


class PromptTemplateInfoGenerator(InfoGenerator):
    """
    This class is used to generate prompt template information from a given file. It extends the InfoGenerator class and
    uses the ijson library to parse and generate items from the JSON file. The class is iterable and each iteration
    returns the next item from the JSON file.

    Attributes:
        file (TextIOWrapper): The file object of the prompt template file.
        generator (generator): The ijson generator object.

    Methods:
        __iter__(): Returns the iterator object (self).
        __next__(): Returns the next item from the JSON file. If there are no more items, it closes the file and
                    raises StopIteration.
    """

    def __init__(self, pt_filepath: str):
        super().__init__(pt_filepath, "template")
