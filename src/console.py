from consolemenu import SelectionMenu


def createMenu(options: list):
    selection = SelectionMenu.get_selection(options)

    return selection
