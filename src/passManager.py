import os
import pickle
from configparser import ConfigParser
from getpass import getpass

from colorama import Fore, Style

import console
import encrypt as cryptic
import mail
import server
import totp

key = cryptic.get_key()

config = ConfigParser()
config.read('config.ini')

email = config.get("Email", "Email")
emailPass = config.get("Email", "Password")

db = server.db
c = db.cursor()
MASTERPASS = ""
USERPASS = ""
empty = False


def validate(s):
    """
	Credit to Sci Prog on stackoverflow for the code.
	https://stackoverflow.com/questions/35857967/python-password-requirement-program
	"""
    SPECIAL = "@$#!&*()[].,?+=-"

    Cap, Low, Num, Spec, Len = False, False, False, False, False
    for i in s:
        if i.isupper():
            Cap = True
        elif i.islower():
            Low = True
        elif i.isdigit():
            Num = True
        elif i in SPECIAL:
            Spec = True
    if len(s) >= 8:
        Len = True

    if Cap and Low and Num and Spec and Len:
        return True
    else:
        return False


with open("data/save.pickle", "r+b") as f:
    if os.path.getsize("data/save.pickle") == 0:
        empty = True
        f.close()

if empty is True:
    MASTERPASS = input(
        Fore.LIGHTCYAN_EX +
        "Welcome. To use this program you must first set a master password for you account. This master password must contain at leat 1 lowercase, 1 uppercase, 1 number, and 1 special character. Your password must also be at least 8 characters long. Make sure this is something you can remember as you cannot change this later. Please enter your password here: "
        + Style.RESET_ALL)

    print("Welcome to user setup.")
    user = input("Please enter the username you would like to login as:")
    userEmail = input("Please enter your email: ")
    USERPASS = input(
        "Please enter the password you would like to login with: ")
    mail.send_test(email, userEmail, emailPass)

    secret = totp.generate_shared_secret()

    PASS = cryptic.encrypt(USERPASS, key)

    c.execute(
        "INSERT INTO secrets (username, email, pass, secret) VALUES (%s, %s, %s, %s)",
        (user, userEmail, PASS, secret),
    )
    db.commit()

    if validate(MASTERPASS) is True:
        with open("data/save.pickle", "r+b") as f:
            pickle.dump(MASTERPASS, f)
            f.close()

    elif validate(MASTERPASS) is False:
        while True:
            MASTERPASS = input(
                Fore.LIGHTCYAN_EX +
                "Welcome. To use this program you must first set a master password. This master password must contain at leat 1 lowercase, 1 uppercase, 1 number, and 1 special character. Your password must also be at least 8 characters long. Please enter your password here: "
                + Style.RESET_ALL)

            if validate(MASTERPASS) is True:
                with open("data/save.pickle", "r+b") as f:
                    pickle.dump(MASTERPASS, f)
                    f.close()
                break

            else:
                print(
                    Fore.RED +
                    "\nTry Again! Make sure your password is at least 8 charaters long and contaions 1 lowercase, 1 uppercase, 1 number, and 1 special character. \n"
                    + Style.RESET_ALL)

if empty is False or MASTERPASS is not None:
    with open("data/save.pickle", "r+b") as f:
        MASTERPASS = pickle.load(f)

log = getpass("Master Password:")

if log == MASTERPASS:

    user = console.createUserMenu()

    c.execute("SELECT pass FROM secrets WHERE username=%s", (user, ))

    for x in c:
        dataPass = str(x)

    dataPass = cryptic.decrypt(dataPass, key)

    loginPass = getpass("Enter your password: ")
    loginPass = bytes(str(loginPass), 'utf8')

    if loginPass == dataPass:
        c.execute("SELECT email FROM secrets WHERE username=%s", (user, ))

        for x in c:
            dataEmail = x

        c.execute("SELECT secret FROM secrets WHERE username=%s", (user, ))

        for y in c:
            secret = str(y)

        tbotp = totp.generate_totp(secret)
        mail.send_secret(email, dataEmail, emailPass, tbotp)
        enterTotp = input("Enter the code that was emailed to you: ")

        if tbotp == enterTotp:
            validation = totp.validate_totp(enterTotp, secret)

            if validate:
                print("Your code is valid, proceed on!")

            else:
                print(Fore.RED + "Invalid Code!" + Style.RESET_ALL)
                exit()

        else:
            print(Fore.RED + "Wrong Code!" + Style.RESET_ALL)
            exit()

    else:
        print(Fore.RED + "Wrong Password!" + Style.RESET_ALL)
        exit()

else:
    print(Fore.RED + "Wrong Master Password!" + Style.RESET_ALL)
    exit()

while True:
    menu = console.createMenu(
        ['Add information', 'Get information', 'Delete information'])

    if menu == 0:
        site = input("Enter the site (include 'https://'): ")
        user = input("Enter the username: ")
        passwd = input("Enter the password: ")
        c.execute(
            "INSERT INTO passwords (site, username, password) VALUES (%s,%s,%s)",
            (site, user, passwd),
        )
        db.commit()
        print(Fore.GREEN + "Successfully inserted data into table!" +
              Style.RESET_ALL)

    elif menu == 1:
        c.execute("SELECT * FROM passwords")
        for x in c:
            print(x)

    elif menu == 2:
        delete = input("What would you like to delete(Enter the id):")
        code = """DELETE FROM passwords WHERE id = %s"""
        id_ = int(delete)
        c.execute(code, (id_, ))
        db.commit()
        print("Succesfully deleted!")

    elif menu == 3:
        print(Fore.LIGHTMAGENTA_EX + "Bye!")
        exit()
