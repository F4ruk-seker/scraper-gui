from dataclasses import dataclass


@dataclass
class ProgresModel:
    name: str
    id: int
    tick_count: int or 0
    percent: int or 0

    status: bool or False
    has_problem: bool or False

    def __init__(self, json: dict):
        for k, v in json.items():
            setattr(self, k, v)

    def create_get_method_path(self):
        return f"{self.id}/{self.tick_count}/{self.percent}/{self.status}/{self.has_problem}"
