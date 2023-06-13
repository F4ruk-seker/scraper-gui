from multiprocessing import Process

from basic_db import Comment, get_session
from requests import api
from models import BranchModel
from config import API_HOST
import uuid


def create_branch(branch: BranchModel):
    path = API_HOST / "branch/create/"
    return api.post(path, branch.json)


    #  251632ee-351e-4949-84ae-8674e5670c51
def get_branch_from_uuid(uuid: str):
    path = API_HOST / "branch" / uuid
    response = api.get(path)

    if response.status_code == 200:
        return BranchModel(response.json())
    else:
        raise "bu uuid bir Branch getirmedi"

def is_uuid(uuid_input):
    try:
        uuid_obj = uuid.UUID(uuid_input)
        return True
    except ValueError:
        return False

def get_branch_from_user_input():
    try:
        branch = None
        name_or_uuid = input("Şube adı giriniz ve ya (uuid): ")

        if is_uuid(name_or_uuid):
            branch = get_branch_from_uuid(name_or_uuid)

        if branch is None:
            explanation = input("Açıklama girin ya da boş bırakın : ")
            url = input('url giriniz (şubenin yorumlar buttonuna tıkladıktan sonra url alınız): ')

            if name_or_uuid and url:
                branch = BranchModel(
                    {
                        "name": name_or_uuid,
                        "url": url,
                        "explanation": explanation
                    }
                )
                crb = create_branch(branch)

                if crb.status_code == 200:
                    return get_branch_from_uuid(crb.json().get('id', None))
                else:
                    print(crb.text)
                    return
            else:
                print("gerekli alanlar boş bırakılmış : name, url".upper())
                return
        return branch
    except:
        return


if __name__ == '__main__':

    branch_list: list[BranchModel] = []

    while True:
        if branch := get_branch_from_user_input():
            branch_list.append(branch)
        if input("keyıt eklemeye devam et (q:quit) : ").lower().strip() == 'q':
            break


    if branch_list and input('Veri çekmeyi başlat : Y/(q:quit) :').lower().strip() != 'q':
        print("işlem bitene kadar bekleyiniz: ")
        from map_manager_2 import ScraperManager

        scm = ScraperManager(branch_list)
        scp = Process(target=scm.multi_scrape, args=(None,))
        scp.run()
        scp.join()
        print("GÖREV TAMAMLANDI YORUMLAR VERİ TABANINA EKLENDİ")