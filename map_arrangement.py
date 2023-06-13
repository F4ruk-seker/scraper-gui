from dataclasses import dataclass, fields


@dataclass
class ArrangementModel:
    __name: str
    __row: int

    def get_name(self):
        return self.__name

    def get_row(self):
        return self.__row


# @dataclass
class Arrangement:
    MOST_RELEVANT = ArrangementModel("en alakalı", 0)
    LATEST = ArrangementModel("en yeni", 1)
    TOP_RATED = ArrangementModel("en yüksek puanlı", 2)
    LOWEST_RATED = ArrangementModel("en düşük puanlı", 3)

    @staticmethod
    def get_arrangement_count() -> int:
        print("DEBUG : (get_arrangement_count): Temporarily returned the no.4 manually. when fixed del static func.")
        return 4

