import os
from time import sleep
import pickle
from configparser import ConfigParser
from getpass import getpass
from validation import validate
from colorama import Fore, Style
import console
import encrypt as cryptic
import mail
import server
import totp
import logs
from rich.prompt import Confirm

key = cryptic.get_key()

logger = logs.logger

config = ConfigParser()
config.read('config.ini')

email = config.get("Email", "Email")
emailPass = config.get("Email", "Password")

host = config.get("MySQL", "Host")
user = config.get("MySQL", "User")
password = config.get("MySQL", "Password")
database = config.get("MySQL", "Database")

db = server.connect(host, user, password, database)
c = db.cursor()
MASTERPASS = ""
USERPASS = ""
empty = False
valid = False

with open("data/save.pickle", "r+b") as f:
    if os.path.getsize("data/save.pickle") == 0:
        empty = True
        f.close()

if empty is True:
    while valid is False:
        MASTERPASS = input(
            Fore.LIGHTCYAN_EX +
            "Welcome. To use this program you must first set a master password for you account. This master password must contain at leat 1 lowercase, 1 uppercase, 1 number, and 1 special character. Your password must also be at least 8 characters long. Make sure this is something you can remember as you cannot change this later. Please enter your password here: "
            + Style.RESET_ALL)

        if validate(MASTERPASS) is True:
            with open("data/save.pickle", "r+b") as f:
                pickle.dump(MASTERPASS, f)
                f.close()

            valid = True

        elif validate(MASTERPASS) is False:
            while True:
                logger.warn(
                    Fore.RED +
                    "\nTry Again! Make sure your password is at least 8 charaters long and contaions 1 lowercase, 1 uppercase, 1 number, and 1 special character. \n"
                    + Style.RESET_ALL)

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
                    logger.warn(
                        Fore.RED +
                        "\nTry Again! Make sure your password is at least 8 charaters long and contaions 1 lowercase, 1 uppercase, 1 number, and 1 special character. \n"
                        + Style.RESET_ALL)

    server.create_user(c, db)

if empty is False or MASTERPASS is not None:
    with open("data/save.pickle", "r+b") as f:
        MASTERPASS = pickle.load(f)

log = getpass("Master Password:")

if log == MASTERPASS:

    user = console.createUserMenu()

    if user == 'Add Users':
        user = server.create_user(c, db)

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

            if validation:
                logger.info(Fore.LIGHTYELLOW_EX +
                            "Your code is valid, proceed on!" +
                            Style.RESET_ALL)

            else:
                logger.critical(Fore.RED + "Invalid Code!" + Style.RESET_ALL)
                exit()

        else:
            logger.critical(Fore.RED + "Wrong Code!" + Style.RESET_ALL)
            exit()

    else:
        logger.critical(Fore.RED + "Wrong Password!" + Style.RESET_ALL)
        exit()

else:
    logger.critical(Fore.RED + "Wrong Master Password!" + Style.RESET_ALL)
    exit()

while True:
    menu = console.createMenu([
        'Add information', 'Get information', 'Delete information',
        'Delete User'
    ])

    if menu == 0:
        site = input("Enter the site (include 'https://'): ")
        user = input("Enter the username: ")
        passwd = input("Enter the password: ")
        server.insert_password(c, site, user, passwd)
        logger.info(Fore.GREEN + "Successfully inserted data into table!" +
                    Style.RESET_ALL)

    elif menu == 1:
        c.execute("SELECT * FROM passwords")
        for x in c:
            logger.info(x)

    elif menu == 2:
        server.delete(c)
        logger.warn("Succesfully deleted!")

    elif menu == 3:
        logger.debug('menu option 4 - delete user')
        # c.execute("SELECT secret FROM secrets WHERE username=%s", (user, ))
        # for y in c:
        #     secret = str(y)

        # c.execute("SELECT email FROM secrets WHERE username=%s", (user, ))

        # for x in c:
        #     dataEmail = x

        tbotp = totp.generate_totp(secret)
        mail.send_secret(email, dataEmail, emailPass, tbotp)

        enterTotp = input(
            "Please enter the code that was emailed to you for verifaction:")

        validation = totp.validate_totp(enterTotp, secret)

        if validation:
            logger.info(Fore.LIGHTYELLOW_EX +
                        "Your code is valid, proceed on!" + Style.RESET_ALL)

        delUser = console.createUserMenu()
        confirm = Confirm.ask(
            f'Are you sure you want to delete user {delUser}?')

        log = getpass("Master Password:")

        if log == MASTERPASS:
            server.delete_user(cursor=c, db=db, user=delUser)
        sleep(1)
    elif menu == 4:
        logger.info(Fore.LIGHTMAGENTA_EX + "Bye!")
        exit()
