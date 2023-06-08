from requests import api
from models import BranchModel
from config import API_HOST


def create_branch(branch: BranchModel):
    path = API_HOST / "branch/add-branch/"
    return api.post(path, branch.json())


def get_branch_opt_query(query: str = '') -> list:
    path = API_HOST / "branch/get-branch/?search=" + query
    data = api.get(path)
    result = []
    for branch in data.json():
        result.append(
            BranchModel(branch)
        )
    return result


def remove_selected_branch():
    pass