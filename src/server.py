import mysql.connector
from colorama import Fore, Style
from rich.prompt import Prompt, IntPrompt
<<<<<<< HEAD
from configparser import ConfigParser
import args
import sqlite3

=======
import logs

logger = logs.logger
>>>>>>> a5eeb747ff72fd0285948bd38544bc948ff29575

config = ConfigParser()

host = config.get("MySQL", "Host")
user = config.get("MySQL", "User")
password = config.get("MySQL", "Password")
database = config.get("MySQL", "Database")
liteDB = config.get("sqlite3", "Databse")


def connect(databse, host=None, user=None, password=None):

    def mysql_connect(host, user, password, databse):
        db = mysql.connector.connect(host=host,
                                     user=user,
                                     passwd=password,
                                     db=database)

        return db

    def sqlite_connect(databse):
        c = sqlite3.connect(liteDB)
        return c


# TODO: Change this into a class and define a cursor in that class
def create_tables(cursor, db):

    def create_pw(cursor, db):
        cursor.execute("""CREATE TABLE IF NOT EXISTS passwords (
                                            site VARCHAR(500) NOT NULL,
                                            username VARCHAR(500) NOT NULL,
                                            password VARCHAR(500) NOT NULL,
                                            id int PRIMARY KEY AUTO_INCREMENT
                                            )""")

        db.commit()

        print(Fore.MAGENTA + "Table passwords created!" + Style.RESET_ALL)

<<<<<<< HEAD
    def create_secrets(cursor, db):
        cursor.execute("""CREATE TABLE IF NOT EXISTS secrets (
                                            username VARCHAR(500) NOT NULL,
                                            email VARCHAR(100) NOT NULL,
                                            secret VARCHAR(500) NOT NULL,
                                            pass VARCHAR(500) NOT NULL,
                                            `key` VARCHAR(500),
                                            id int PRIMARY KEY AUTO_INCREMENT
                                            )""")

        db.commit()

        print(Fore.MAGENTA + "Table secrets created!" + Style.RESET_ALL)
=======
    logger.info("Passwords Table created")

    cursor.execute("""CREATE TABLE IF NOT EXISTS secrets (
                                        username VARCHAR(500) NOT NULL,
                                        email VARCHAR(100) NOT NULL,
                                        secret VARCHAR(500) NOT NULL,
                                        pass VARCHAR(500) NOT NULL,
                                        `key` VARCHAR(500),
                                        id int PRIMARY KEY AUTO_INCREMENT
                                        )""")
>>>>>>> a5eeb747ff72fd0285948bd38544bc948ff29575


<<<<<<< HEAD
    create_pw(cursor, db)
    create_secrets(cursor, db)
=======
    logger.info(Fore.MAGENTA + "Table secrets created!" + Style.RESET_ALL)
>>>>>>> a5eeb747ff72fd0285948bd38544bc948ff29575


def insert_password(c, site, user, passwd):
    c.execute(
        "INSERT INTO passwords (site, username, password) VALUES (%s,%s,%s)",
        (site, user, passwd),
    )
    db.commit()


def insert_master(c, user, email, password, secret):
    c.execute(
        "INSERT INTO secrets (username, email, pass, secret) VALUES (%s, %s, %s, %s)",
        (user, email, password, secret),
    )
    db.commit()


def delete(c, identify=None):
    everything = Prompt.ask("Would you like to delete all entries?",
                            choices=['yes', 'no'])
    if everything == 'no':
        identify = IntPrompt(
            "Enter the ID of the entry you would like to delete")
        c.execute("DELTE FROM password WHERE id=%", (identify, ))
        db.commit()
    elif everything == 'yes':
        c.execute("DELETE FROM passwords")
        db.commit()
