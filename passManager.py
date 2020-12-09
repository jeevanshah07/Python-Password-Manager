import os
import pickle
from getpass import getpass

import mysql.connector
from colorama import Back, Fore, Style

import encrypt
import mail
import totp

db = mysql.connector.connect(
    host="localhost", user="root", passwd="r@j@71!", db="passwordManager"
)

c = db.cursor()

cipher = encrypt.RSA_Cipher()
cipher.generate_key(2048)

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


MASTERPASS = ""
USERPASS = ""
empty = False

with open("masterpass.pickle", "r+b") as f:
    if os.path.getsize("masterpass.pickle") == 0:
        empty = True
        f.close()


if empty == True:
    MASTERPASS = input(
        Fore.LIGHTCYAN_EX
        + "Welcome. To use this program you must first set a master password for you account. This master password must contain at leat 1 lowercase, 1 uppercase, 1 number, and 1 special character. Your password must also be at least 8 characters long. Make sure this is something you can remember as you cannot change this later. Please enter your password here: "
        + Style.RESET_ALL
    )
    print("Welcome to user setup.")
    user = input("Please enter the username you would like to login as:")
    email = input("Please enter your email: ")
    USERPASS = input("Please enter the password you would like to login with: ")
    mail.send_test("throwawaydev307@gmail.com", email, "EMAIL PASS")

    secret = totp.generate_shared_secret()
    print(
        Fore.RED
        + Back.WHITE
        + "THIS IS VERY IMPORTANT! YOU MUST SAVE THIS KEY AS IT ALLOWS YOU TO USE THE MANAGER. SAVE THIS KEY SOMEWHERE: "
        + secret
        + Style.RESET_ALL
    )

    print("Welcome to user setup.")
    user = input("Please enter the username you would like to login as:")
    email = input("Please enter your email: ")
    USERPASS = input("Please enter the password you would like to login with: ")
    mail.send_test("dev87460@gmail.com", email, "EMAIL PASS")

    USERPASS = cipher.encrypt(str(USERPASS))
    secret = cipher.encrypt(str(secret))

    c.execute(
        "INSERT INTO secrets (username, email, pass, secret) VALUES (%s, %s, %s, %s)",
        (user, email, USERPASS, secret),
    )
    db.commit()

    if validate(MASTERPASS) == True:
        with open("masterpass.pickle", "r+b") as f:
            pickle.dump(MASTERPASS, f)
            f.close()

    elif validate(MASTERPASS) == False:
        while True:
            MASTERPASS = input(
                Fore.LIGHTCYAN_EX
                + "Welcome. To use this program you must first set a master password. This master password must contain at leat 1 lowercase, 1 uppercase, 1 number, and 1 special character. Your password must also be at least 8 characters long. Please enter your password here: "
                + Style.RESET_ALL
            )

            if validate(MASTERPASS) == True:
                with open("masterpass.pickle", "r+b") as f:
                    pickle.dump(MASTERPASS, f)
                    f.close()
                break

            else:
                print(
                    Fore.RED
                    + "\nTry Again! Make sure your password is at least 8 charaters long and contaions 1 lowercase, 1 uppercase, 1 number, and 1 special character. \n"
                    + Style.RESET_ALL
                )

if empty == False or MASTERPASS is not None:
    with open("masterpass.pickle", "r+b") as f:
        MASTERPASS = pickle.load(f)
        f.close()

log = getpass()

if log == MASTERPASS:
    loginUser = input("Enter your username: ")

    c.execute("SELECT username FROM secrets WHERE username=%s", (loginUser,))

    for x in c:
        dataUser = x

    loginUser_ = f"('{loginUser}',)"

    if str(loginUser_) == str(dataUser):
        c.execute("SELECT pass FROM secrets WHERE username='marvelman3284'")

        for x in c:
            dataPass = x
        
        dataPass = cipher.decrypt(dataPass)

        loginPass = input("Enter your password: ")
        loginPass_ = f"('{loginPass}',)"

        if str(loginPass_) == str(dataPass):
            c.execute("SELECT email FROM secrets WHERE username=%s", (loginUser,))

            for x in c:
                dataEmail = x

            c.execute("SELECT secret FROM secrets WHERE username=%s", (loginUser,))

            for y in c:
                secret = str(y)

            secret = cipher.decrypt(secret)

            secret = secret.replace('(', '') 
            secret = secret.replace(')', '') 
            secret = secret.replace("'", '') 
            secret = secret.replace(",", '') 

            tbotp = totp.generate_totp(secret)
            mail.send_secret("dev87460@gmail.com", dataEmail, "EMAIL PASS", tbotp)
            enterTotp = input("Enter the code that was emailed to you: ")

            if tbotp == enterTotp:
                validation = totp.validate_totp(enterTotp, secret)

                if validate:
                    print("Your code is valid, proceed on!")

                else:
                    print("Sorry your code is not valid :(")

else:
    for i in range(2):
        i += 1
        log = getpass("Try again:")

        if log == MASTERPASS:
            break

    print(Fore.RED + "Sorry, wrong password" + Style.RESET_ALL)
    exit()

while True:
    what = input(
        "What would you like to do? \n1.Add information \n2.Get information \n3.Delete information \n4.Exit \nEnter a number 1, 2, 3, or 4: "
    )
    valid = [1, 2, 3, 4]
    try:
        i = int(what)
        if i in valid:
            break

    except ValueError:
        print(Fore.RED + "You didn't enter a number" + Style.RESET_ALL)

    if int(what) == 1:
        site = input("Enter the site (include 'https://'): ")
        user = input("Enter the username: ")
        passwd = input("Enter the password: ")
        c.execute(
            "INSERT INTO passwords (site, username, password) VALUES (%s,%s,%s)",
            (site, user, passwd),
        )
        db.commit()
        print(Fore.GREEN + "Successfully inserted data into table!" + Style.RESET_ALL)

        stop = input(
            "Would you like to do more operations? (Y for yes | Any other key for no):"
        )
        if stop == "Y" or "Yes" or "y" or "yes":
            continue
        else:
            exit()

    elif int(what) == 2:
        c.execute("SELECT * FROM passwords")
        for x in c:
            print(x)

        stop = input(
            "Would you like to do more operations? (Y for yes | Any other key for no):"
        )
        if stop == "Y" or "Yes" or "y" or "yes":
            continue
        else:
            exit()

    elif int(what) == 3:
        delete = input("What would you like to delete(Enter the id):")
        code = """DELETE FROM passwords WHERE id = %s"""
        id_ = int(delete)
        c.execute(code, (id_,))
        db.commit()
        print("Succesfully deleted!")

        stop = input(
            "Would you like to do more operations? (Y for yes | Any other key for no):"
        )
        if stop == "Y" or "Yes" or "y" or "yes":
            continue
        else:
            exit()

    elif int(what) == 4:
        exit()
