from dataclasses import dataclass


@dataclass
class CommentModel:
    id: str
    name: str
    url: str

    def __init__(self, json: dict):
        for k, v in json.items():
            setattr(self, k, v)

    @property
    def json(self):
        return self.__dict__
