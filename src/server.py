from getpass import getpass
import mysql.connector
from configparser import ConfigParser
from colorama import Fore, Style
from rich.prompt import Prompt
import logs
import mail
import totp
import encrypt as cryptic

logger = logs.logger
key = cryptic.get_key()
config = ConfigParser()
config.read('config.ini')

host = config.get("MySQL", "Host")
user = config.get("MySQL", "User")
password = config.get("MySQL", "Password")
database = config.get("MySQL", "Database")

email = config.get("Email", "Email")
emailPass = config.get("Email", "Password")


def connect(host, user, password, database):
    db = mysql.connector.connect(host=host,
                                 user=user,
                                 passwd=password,
                                 db=database)

    return db


db = connect(host, user, password, database)
c = db.cursor()


def create_tables(cursor, db):
    cursor.execute("""CREATE TABLE IF NOT EXISTS secrets (
                                        username VARCHAR(500) NOT NULL,
                                        email VARCHAR(100) NOT NULL,
                                        secret VARCHAR(500) NOT NULL,
                                        pass VARCHAR(500) NOT NULL,
                                        `key` VARCHAR(500),
                                        id int PRIMARY KEY AUTO_INCREMENT
                                        )""")

    db.commit()

    logger.info(Fore.MAGENTA + "Table secrets created!" + Style.RESET_ALL)


def create_user_table(cursor, db, user):
    cursor.execute("""CREATE TABLE IF NOT EXISTS """ + user + """ (
                                        site VARCHAR(500) NOT NULL,
                                        username VARCHAR(500) NOT NULL,
                                        password VARCHAR(500) NOT NULL,
                                        id int PRIMARY KEY AUTO_INCREMENT
                                        )""")

    db.commit()

    print(Fore.MAGENTA + "Table passwords created!" + Style.RESET_ALL)

    logger.info("Passwords Table created")


def insert_password(cursor, site, user, passwd):
    cursor.execute(
        "INSERT INTO passwords (site, username, password) VALUES (%s,%s,%s)",
        (site, user, passwd),
    )
    db.commit()


def insert_master(cursor, user, email, password, secret):
    cursor.execute(
        "INSERT INTO secrets (username, email, pass, secret) VALUES (%s, %s, %s, %s)",
        (user, email, password, secret),
    )
    db.commit()


def delete(cursor):
    # TODO: change to use a menu which lists all passwords, then have the user choose from those
    everything = Prompt.ask("Would you like to delete all entries?",
                            choices=['yes', 'no'])
    if everything == 'no':
        identify = input("Enter the ID of the entry you would like to delete")
        cursor.execute("DELETE FROM password WHERE id=%", (identify, ))
        db.commit()
    elif everything == 'yes':
        cursor.execute("DELETE FROM passwords")
        db.commit()


def create_user(cursor, db):
    logger.info(Fore.GREEN + "Welcome to user setup." + Style.RESET_ALL)

    user = input("Please enter the username you would like to login as:")

    print(user)
    userEmail = input("Please enter your email: ")

    USERPASS = getpass(
        "Please enter the password you would like to login with: ")

    mail.send_test(email, userEmail, emailPass)

    secret = totp.generate_shared_secret()

    PASS = cryptic.encrypt(USERPASS, key)

    insert_master(cursor, user, userEmail, PASS, secret)
    create_user_table(cursor, db, user)

    db.commit()

    return user


def delete_user(cursor, db, user):
    # TODO: insert variable names in sql statement
    logger.debug(user)
    cursor.execute("DELETE FROM secrets WHERE username=%s", (user, ))
    db.commit()
    # del_table_sql = f"DROP TABLE {user}"
    # cursor.execute(del_table_sql)

    db.commit()
    logger.warn(Fore.RED + f"Deleted User {user}" + Style.RESET_ALL)
