import mysql.connector
from colorama import Fore, Style
from rich.prompt import Prompt, IntPrompt
from configparser import ConfigParser
import args
import sqlite3

config = ConfigParser()

config.read('config.ini')

host = config.get("MySQL", "Host")
user = config.get("MySQL", "User")
password = config.get("MySQL", "Password")
database = config.get("MySQL", "Database")
liteDB = config.get("sqlite3", "Database")


def mysql_connect(host, user, password, databse):
    db = mysql.connector.connect(host=host,
                                 user=user,
                                 passwd=password,
                                 db=database)

    return db


def sqlite_connect(database):
    c = sqlite3.connect(database)
    return c


def create_tables(host, user, password, database):

    if not args.sql:
        cursor = sqlite_connect(liteDB)

    elif args.sql:
        db = mysql_connect(database, host, user, password)
        cursor = db.cursor()

    def create_pw(cursor, db):
        cursor.execute("""CREATE TABLE IF NOT EXISTS passwords (
                                            site VARCHAR(500) NOT NULL,
                                            username VARCHAR(500) NOT NULL,
                                            password VARCHAR(500) NOT NULL,
                                            id int PRIMARY KEY AUTO_INCREMENT
                                            )""")

        db.commit()

        print(Fore.MAGENTA + "Table passwords created!" + Style.RESET_ALL)

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

    create_pw(cursor, db)
    create_secrets(cursor, db)

    return cursor, db


def insert_password(c, site, user, passwd, db):
    c.execute(
        "INSERT INTO passwords (site, username, password) VALUES (%s,%s,%s)",
        (site, user, passwd),
    )
    db.commit()


def insert_master(c, user, email, password, secret, db):
    c.execute(
        "INSERT INTO secrets (username, email, pass, secret) VALUES (%s, %s, %s, %s)",
        (user, email, password, secret),
    )
    db.commit()


def delete(c, db, identify=None):
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


c, db = create_tables(host, user, password, database)
