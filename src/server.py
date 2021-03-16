import mysql.connector
from configparser import ConfigParser

config = ConfigParser()
host = config.get("MySQL", "Host")
user = config.get("MySQL", "User")
password = config.get("MySQL", "Password")
database = config.get("MySQL", "Database")

db = mysql.connector.connect(host=host,
                             user=user,
                             passwd=password,
                             db=database)

c = db.cursor()

c.execute("""CREATE TABLE passwords (
	site VARCHAR(500) NOT NULL,
	username VARCHAR(500) NOT NULL,
	password VARCHAR(500) NOT NULL,
	PRIMARY KEY id AUTO_INCREMENT NOT NULL
	)""")

db.commit()

c.execute("""CREATE TABLE secrets (
	username VARCHAR(500) NOT NULL,
	email VARCHAR(100) NOT NULL,
	pass VARCHAR(500) NOT NULL,
	secret VARCHAR(500) NOT NULL
	)""")

db.commit()
