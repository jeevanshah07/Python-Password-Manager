from getpass import getpass
import mysql.connector
from configparser import ConfigParser
from colorama import Fore, Style
from rich.prompt import Prompt
import logs
import mail
import totp
import encrypt as cryptic
from validation import validate

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
    """
    Connects to a remote MySQL server

    Args:
        host (str): The host IP address of the server
        user (str): The user to log into the server with
        password (str): The accompianing password for the user
        databse (str): The database to store/create tables in

    Returns:
        mysql.connector.connection.MySQLConnection
    """

    db = mysql.connector.connect(host=host,
                                 user=user,
                                 passwd=password,
                                 db=database)

    return db


db = connect(host, user, password, database)
c = db.cursor()
print(type(c))


def create_tables(cursor, db):
    """
    Creates the nessecary tables for the program to run

    Args:
        cursor (mysql.connector.cursor.MySQLCursor): The database cursor
        db (mysql.connector.connection.MySQLConnection): The database for storying data
    """

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
    """
    Creates the nessecary user tables for the program to run

    Args:
        cursor (mysql.connector.cursor.MySQLCursor): The database cursor
        db (mysql.connector.connection.MySQLConnection): The database for storying data
        user (str): The user to name the table after
    """

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
    # TODO: passwords need to be inserted into user tables
    """
    Inserts a password and the nessecary information needed into a table

    Args:
        cursor (mysql.connector.cursor.MySQLCursor): The databse cursor
        site (str): The site for the accompianing password
        user (str): The username for the accompianing password and website
        passwd (str): The password for the website and password

    Notes:
        No return value
    """
    cursor.execute(
        "INSERT INTO passwords (site, username, password) VALUES (%s,%s,%s)",
        (site, user, passwd),
    )
    db.commit()


def insert_master(cursor, user, email, password, secret):
    """
    Inserts the master password and the nessecary information needed into the secrets table

    Args:
        cursor (mysql.connector.cursor.MySQLCursor): The databse cursor
        email (str): The email the user entered during signup
        user (str): The username provided during user setup
        password (str): The password for the specific user
        secret (str): The unique secret for the user

    Notes:
        No return value
    """

    cursor.execute(
        "INSERT INTO secrets (username, email, pass, secret) VALUES (%s, %s, %s, %s)",
        (user, email, password, secret),
    )
    db.commit()


def delete(cursor):
    """
    Deletes a username, password, and website from the stored table

    Args:
        cursor (mysql.connector.cursor.MySQLCursor): The databse cursor

    Notes:
        No return value
    """

    # TODO: delete from the user table instead of the password
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
    """
    Creates a a user for the overall manager

    Args:
        cursor (mysql.connector.cursor.MySQLCursor): The databse cursor
        db (mysql.connector.connection.MySQLConnection): The database for storying data

    Returns:
        str: The selected username choosen
    """

    logger.info(Fore.GREEN + "Welcome to user setup." + Style.RESET_ALL)

    user = input("Please enter the username you would like to login as:")

    userEmail = input("Please enter your email: ")

    USERPASS = getpass(
        "Please enter the password you would like to login with: ")

    strong = validate(USERPASS)

    while strong is False:
        logger.warn(
            'Your password must be 8 characters long, contain one uppercase, one lowercase, and one of the following characters: [, ], @, $, #, !, &, *, (, ), ., ?, +, =, -'
        )

        USERPASS = getpass(
            "Please enter the password you would like to login with: ")

        strong = validate(USERPASS)

    mail.send_test(email, userEmail, emailPass)

    secret = totp.generate_shared_secret()

    PASS = cryptic.encrypt(USERPASS, key)

    insert_master(cursor, user, userEmail, PASS, secret)
    create_user_table(cursor, db, user)

    db.commit()

    return user


def delete_user(cursor, db, user):
    """
    Deletes a user from the list of active users

    Args:
        cursor (mysql.connector.cursor.MySQLCursor): The databse cursor
        db (mysql.connector.connection.MySQLConnection): The database for storying data
        user (str): The username to delete
    """
    # TODO: insert variable names in sql statement
    cursor.execute("DELETE FROM secrets WHERE username=%s", (user, ))
    db.commit()

    db.commit()
    logger.warn(Fore.RED + f"Deleted User {user}" + Style.RESET_ALL)
