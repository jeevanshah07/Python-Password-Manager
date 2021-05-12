from consolemenu import SelectionMenu


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


def createUserMenu(c):
    """
    Creates a selection menu based on a list of users

    Returns:
        str: The username of the selected user in a string form
    """

    users = ['Add Users']
    c.execute("SELECT username FROM secrets")

    for i in c:
        i = str(i).replace("(", "")
        i = i.replace(")", "")
        i = i.replace(",", "")
        i = i.replace("'", "")
        users.append(i)

    user = createMenu(users)
    return str(users[user])


def createPassMenu(c, username):
    """
    Creates a selection menu based on a list of websites

    Args:
        username (str): The username which is also the name of the table

    Returns:
        str: The id of the website choosen
    """

    websites = []

    c.execute("SELECT site FROM " + username)

    for i in c:
        i = str(i).replace("(", "")
        i = i.replace(")", "")
        i = i.replace(",", "")
        i = i.replace("'", "")
        websites.append(i)

    website = createMenu(websites)
    return str(websites[website])
