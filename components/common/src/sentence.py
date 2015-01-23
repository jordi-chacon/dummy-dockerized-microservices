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

    def from_json(self, json_str):
        data = json.loads(json_str)
        self.author = data['object']['author']
        self.text = data['object']['text']
        self.language = data['object']['language']

    def get_author(self):
        return self.author

    def get_language(self):
        return self.language

    def get_text(self):
        return self.text

    def set_author(self, author):
        self.author = author

    def set_language(self, language):
        self.language = language

    def set_text(self, text):
        self.text = text
