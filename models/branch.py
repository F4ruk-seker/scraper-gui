from dataclasses import dataclass


@dataclass
class BranchModel:
    id: str or None
    name: str
    url: str
    explanation: str
    comments: list or None

    def __init__(self, json: dict):
        for k, v in json.items():
            setattr(self, k, v)

    @property
    def json(self):
        return self.__dict__

