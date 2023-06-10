from config import GUI_LOCAL_HOST
from models import ProgresModel
from requests import api


def send_progres_status(progres: ProgresModel):
    path = GUI_LOCAL_HOST / "scraper/status/"
    print(path)
    response = api.post(path, progres.__dict__)
    print(response.text)
data = ProgresModel("test",1,5,6,True,False)

print(data.__dict__)