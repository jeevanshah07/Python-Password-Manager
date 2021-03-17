import mysql.connector
from configparser import ConfigParser


def connect():
    config = ConfigParser()
    config.read('config.ini')

    host = config.get("MySQL", "Host")
    user = config.get("MySQL", "User")
    password = config.get("MySQL", "Password")
    database = config.get("MySQL", "Database")
    db = mysql.connector.connect(host=host,
                                 user=user,
                                 passwd=password,
                                 db=database)

    cursor = db.cursor
    return cursor, db


c, db = connect()


def create_tables(cursor, db):

    c.execute("""CREATE TABLE passwords IF NOT EXISTS (
                                        site VARCHAR(500) NOT NULL,
                                        username VARCHAR(500) NOT NULL,
                                        password VARCHAR(500) NOT NULL,
                                        PRIMARY KEY id AUTO_INCREMENT NOT NULL
                                        )""")

    db.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS secrets (
                                        username VARCHAR(500) NOT NULL,
                                        email VARCHAR(100) NOT NULL,    pass VARCHAR(500) NOT NULL,
                                        secret VARCHAR(500) NOT NULL,
                                        key VARCHAR(200),
                                        PRIMARY KEY id AUTO_INCREMENT NOT NULL
                                        )""")

    db.commit()
