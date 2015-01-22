import json


class Sentence:
    def __init__(self, author="", text="", language=""):
        self.author = author
        self.text = text
        self.language = language
        return

    def to_json(self):
        data = {'class': self.__class__.__name__,
                'object': {'author': self.author,
                           'text': self.text,
                           'language': self.language}
                }
        return json.dumps(data)
