import time
from nicegui import ui, app
from nicegui import events
from models import BranchModel
import requests
from api_service import Branch
import re
from models import ProgresModel
from models import BranchModel

API_HOST = "http://127.0.0.1:8000/api/"

branch_list: list[dict] = []


def start_scrape(scrape_branch_list: list):
    format_branch_list: list = []
    for branch in scrape_branch_list:
        format_branch_list.append(BranchModel(branch))


@ui.refreshable
def user_bar():
    ui.label("test p")

def remove_selected_branch():
    pass


class MainPage:

    def __init__(self):
        self.branch_list: list = []
        self.ui = ui
        self.gui()
        self.branch_select_list: list = []
        self.get_branch_opt_query()

    def set_branch_select_list(self, select_list: list):
        self.branch_select_list = select_list

    def call_scrapers(self):
        start_scrape(self.branch_select_list)

    def create_branch(self):
        branch = BranchModel({
                    "name": self.new_branch_name.value,
                    "url": self.new_branch_url.value,
                    "explanation": self.new_branch_explanation.value
                })
        self.new_branch_name_dialog.close()
        request = Branch.create_branch(branch)
        if request.status_code == 201:
            self.ui.notify("Created")
            self.new_branch_name.value = ''
            self.new_branch_url.value = ''
            self.new_branch_explanation.value = ''
        else:
            self.ui.notify(f"Problem : {request.text}")

    def get_branch_opt_query(self, query=''):
        self.branch_wait.set_visibility(True)

        request = Branch.get_branch_opt_query(query.value) if query else Branch.get_branch_opt_query()
        self.branch_list.clear()
        for __branch in request:
            self.branch_list.append(__branch.json)
        self.branch_table.update()
        self.branch_wait.set_visibility(False)


    def gui(self):
        thd = self.ui.label('Branch create')

        with self.ui.dialog().classes('w-full ') as self.new_branch_name_dialog, self.ui.card():
            self.ui.label('Branch create')

            self.new_branch_name = self.ui.input(placeholder='Name').classes('w-full text-lg block')
            self.new_branch_url = self.ui.input(placeholder='Url').classes('w-full text-lg block')
            self.new_branch_explanation = self.ui.input(placeholder='Explanation').classes('w-full text-lg block')

            self.ui.button('Save', on_click=lambda x: self.create_branch())

        with self.ui.column().classes('container mx-auto relative'):
            with self.ui.row().classes('absolute right-0'):
                self.ui.button('Create Branch', on_click=self.new_branch_name_dialog.open).classes("ease-in duration-700")
                with self.ui.link().classes('no-underline text-black').style("text-decoration:none;").on('click',
                                                                                                         lambda: user_menu.open()).props(
                    'icon=menu'):
                    with self.ui.row():
                        self.ui.icon('person', size='lg')
                        self.ui.label('person').classes("m-auto")
                        self.ui.icon('expand_more').classes('m-auto')

                    result = self.ui.label().classes('mr-auto')

                    with self.ui.menu() as user_menu:
                        self.ui.menu_item('Menu item 1', lambda: result.set_text('Selected item 1'))
                        self.ui.menu_item('Menu item 2', lambda: result.set_text('Selected item 2'))
                        self.ui.menu_item('Menu item 3 (keep open)', auto_close=False)
                        self.ui.separator()
                        self.ui.menu_item('Close', on_click=user_menu.close)

        with self.ui.column().classes('justify-center items-center container mx-auto mt-5'):
            self.ui.input(placeholder='Search', on_change=lambda q: self.get_branch_opt_query(q)).classes(
                'w-full text-lg block')
            # self.ui.separator()

        with self.ui.column().classes('container mx-auto mt-0') as branch_option_menu:
            with self.ui.dialog().classes('w-full ') as remove_selected_branch_dialog, self.ui.card():
                self.ui.label('250 silince')
                with self.ui.row():
                    self.ui.button('Sil', on_click=self.create_branch).props("color=red")
                    self.ui.button('iptal', on_click=self.create_branch)

            with self.ui.row().classes():
                self.ui.button("Veri Çek", on_click=self.call_scrapers).classes("button-white")
                self.ui.button("Düzenle").classes("button-white")
                self.ui.button("Perfonmans")
                self.ui.button("sil", on_click=remove_selected_branch_dialog.open).props("color=red")

        columns = [
            {'name': 'name', 'label': 'Name', 'field': 'name', 'sortable': True, 'align': 'left', 'select': True},
            {'name': 'url', 'label': 'url', 'field': 'url', 'sortable': False, 'align': 'left', 'max':10},
            {'name': 'explanation', 'label': 'explanation', 'field': 'explanation', 'sortable': False,
             'align': 'left'},
            # {'name': 'id', 'label': 'id', 'field': 'id', 'reqself.uired': False, 'align': 'left', "selectable": True},
        ]
        with self.ui.column().classes('justify-center items-center container mx-auto mt-0'):
            self.branch_wait = self.ui.spinner(size='lg')
            self.branch_table = self.ui.table(columns=columns, rows=self.branch_list, row_key='id', selection='multiple',
                                              on_select=lambda x: self.set_branch_select_list(x.selection)).classes('w-full').style("max-height:68vh;")

MainPage()

app.native.window_args['resizable'] = True
app.native.start_args['debug'] = False
# self.ui.dark_mode().enable()
ui.run(native=True, window_size=(1280, 720), fullscreen=False, title="F4 |", favicon="🚀", reload=True)
