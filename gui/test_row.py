from test_gen import TEST_DATA

from nicegui import ui

with ui.card():
    with ui.row():
        ui.label("test")
        ui.label("test")
        ui.button("test")
        ui.button("test")
        ui.label("test")

    with ui.row():
        ui.label("a")
        ui.label("2")
        ui.label("4")
        ui.knob(10)


ui.run()