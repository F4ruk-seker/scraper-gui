import tkinter

from nicegui import ui, app

app.native.window_args['resizable'] = True
app.native.start_args['debug'] = False


from pages import main_page




# ui.dark_mode().enable()

ui.run(native=True, window_size=(1280, 720), fullscreen=False, title="F4 |", favicon="🚀")

