from dataclasses import dataclass


@dataclass
class BranchModel:
    id: str or None
    name: str
    url: str
    explanation: str

    def __init__(self, json: dict):
        if json:
            for k, v in json.items():
                setattr(self, k, v)

    def json(self):
        return self.__dict__

