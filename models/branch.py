from dataclasses import dataclass


@dataclass
class BranchModel:
    id: str or None
    name: str
    url: str
    explanation: str
    comments: list = None

    def __init__(self, json: dict):
        self.json.update(json)
        # for k, v in json.items():
        #     setattr(self, k, None)
        # for k, v in json.items():
        #     setattr(self, k, v)

    @property
    def json(self):
        return self.__dict__

