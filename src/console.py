from consolemenu import SelectionMenu
import server


def createMenu(options: list):
    selection = SelectionMenu.get_selection(options)

    return selection


def createUserMenu():
    users = []
    c = server.db.cursor()
    c.execute("SELECT username FROM secrets")

    for i in c:
        i = str(i).replace("(", "")
        i = i.replace(")", "")
        i = i.replace(",", "")
        users.append(i)

    return createMenu(users)
