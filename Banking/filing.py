import json


class FileMaking:
    """
    FILING FUNCTIONS
    FileMaking: This class is responsible for
    loading and dumping data to a JSON file (my_history.json).
    It has methods load_file() to load the data from the file
    and dump_file() to save the data back to the file.
    """

    def __init__(self):
        self.content = {}

    def load_file(self):
        try:
            with open("my_history.json", "r", encoding="UTF-8") as f:
                self.content = json.load(f)
        except FileNotFoundError:
            print("File not found.")
            self.content = None
        except PermissionError:
            print("Permission denied.")
            self.content = None

    def dump_file(self):
        with open("my_history.json", "w") as f:
            json.dump(self.content, f)
