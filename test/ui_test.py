from ui_elements.loadui import loadUiType, loadStyleSheet


uiFile = pathjoin('test.ui')
ui_form, ui_base = loadUiType(uiFile)


class Test():
    def __init__(self):
        s