from consolemenu import SelectionMenu
import server


def createMenu(options: list):
    """
    Creates a selection menu based on a list

    Args:
        options (list): A list of all the different options for the menu

    Returns:
        int: The integer index of the selected value.
    """

    selection = SelectionMenu.get_selection(options)

    return selection


def createUserMenu():
    """
    Creates a selection menu based on a list of users

    Returns:
        str: The username of the selected user in a string form
    """

    users = ['Add Users']
    c = server.db.cursor()
    c.execute("SELECT username FROM secrets")

    for i in c:
        i = str(i).replace("(", "")
        i = i.replace(")", "")
        i = i.replace(",", "")
        i = i.replace("'", "")
        users.append(i)

    user = createMenu(users)
    return str(users[user])
