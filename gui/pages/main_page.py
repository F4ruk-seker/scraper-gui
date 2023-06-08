import time
from nicegui import ui, app
from nicegui import events
from models import BranchModel
import requests
from api_service import branch

API_HOST = "http://127.0.0.1:8000/api/"

branch_list: list[dict] = []


bar = 0
@app.get('/random/{max}')
def generate_random_number(max: int):
    thd.text = max
    thd.update()
    return



@ui.refreshable
def user_bar():
    ui.label("test p")

def create_branch(e):
    new_branch = BranchModel({
         "name": new_branch_name.value,
         "url": new_branch_url.value,
         "explanation": new_branch_explanation.value
     })
    new_branch_name_dialog.close()
    request = branch.create_branch(new_branch)
    if request.status_code == 201:
        ui.notify("Created")
        new_branch_name.value = ''
        new_branch_url.value = ''
        new_branch_explanation.value = ''
    else:
        ui.notify(f"Problem : {request.text}")

def get_branch_opt_query(query=''):
    branch_wait.set_visibility(True)
    global branch_list
    request = branch.get_branch_opt_query(query.value) if query else branch.get_branch_opt_query()
    branch_list.clear()
    for __branch in request:
        branch_list.append(__branch.__dict__)
    branch_table.update()
    branch_wait.set_visibility(False)

def remove_selected_branch():
    pass

def branch_select(x):
    # if len(x.selection) > 0:
    pass


thd = ui.label('Branch create')

with ui.dialog().classes('w-full ') as new_branch_name_dialog, ui.card():
    ui.label('Branch create')

    new_branch_name = ui.input(placeholder='Name').classes('w-full text-lg block')
    new_branch_url = ui.input(placeholder='Url').classes('w-full text-lg block')
    new_branch_explanation = ui.input(placeholder='Explanation').classes('w-full text-lg block')

    ui.button('Save', on_click=create_branch)

with ui.column().classes('container mx-auto relative'):
    with ui.row().classes('absolute right-0'):
        ui.button('Create Branch', on_click=new_branch_name_dialog.open).classes("ease-in duration-700")
        with ui.link().classes('no-underline text-black').style("text-decoration:none;").on('click',lambda: user_menu.open()).props('icon=menu'):
            with ui.row():
                ui.icon('person', size='lg')
                ui.label('person').classes("m-auto")
                ui.icon('expand_more').classes('m-auto')

            result = ui.label().classes('mr-auto')

            with ui.menu() as user_menu:
                ui.menu_item('Menu item 1', lambda: result.set_text('Selected item 1'))
                ui.menu_item('Menu item 2', lambda: result.set_text('Selected item 2'))
                ui.menu_item('Menu item 3 (keep open)', auto_close=False)
                ui.separator()
                ui.menu_item('Close', on_click=user_menu.close)

with ui.column().classes('justify-center items-center container mx-auto mt-5'):
    ui.input(placeholder='Search', on_change=lambda q: get_branch_opt_query(q)).classes('w-full text-lg block')
    # ui.separator()

with ui.column().classes('container mx-auto mt-0') as branch_option_menu:
    with ui.dialog().classes('w-full ') as remove_selected_branch_dialog, ui.card():
        ui.label('250 silince')
        with ui.row():
            ui.button('Sil', on_click=create_branch).props("color=red")
            ui.button('iptal', on_click=create_branch)

    with ui.row().classes():
        ui.button("Düzenle").classes("button-white")
        ui.button("Perfonmans")
        ui.button("sil", on_click=remove_selected_branch_dialog.open).props("color=red")

with ui.column().classes('justify-center items-center container mx-auto mt-0'):
    columns = [
        {'name': 'name', 'label': 'Name', 'field': 'name', 'sortable': True, 'align': 'left'},
        {'name': 'url', 'label': 'url', 'field': 'url', 'sortable': False, 'align': 'left'},
        {'name': 'explanation', 'label': 'explanation', 'field': 'explanation', 'sortable': False, 'align': 'left'},
        {'name': 'id', 'label': 'id', 'field': 'id', 'required': False, 'align': 'left', "selectable": True},
    ]
    branch_wait = ui.spinner(size='lg')
    branch_table = ui.table(columns=columns, rows=branch_list, row_key='id', selection='multiple',
                            on_select=branch_select).classes('w-full').style("max-height:68vh;")

    get_branch_opt_query()




app.native.window_args['resizable'] = True
app.native.start_args['debug'] = False
ui.run(native=True, window_size=(1280, 720), fullscreen=False, title="F4 |", favicon="🚀")
