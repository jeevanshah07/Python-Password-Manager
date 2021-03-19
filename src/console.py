from consolemenu import SelectionMenu
import server


def createMenu(options: list):
	selection = SelectionMenu.get_selection(options)

	return selection


def createUserMenu():
	c = server.db.cursor()
	c.execute("SELECT username FROM secrets")

	for i in c:
		i = list(i)

	return createMenu(i)
