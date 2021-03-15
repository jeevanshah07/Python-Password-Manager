from consolemenu import SelectionMenu


def createMenu(options):
    selection = SelectionMenu.get_selection(options)

    return selection


c = createMenu(['yes', 'no'])
print(c)
