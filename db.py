
#imports
import mysql.connector  as mc
from mysql.connector import errorcode
import os


def Create_connect_database(cursor , DB_NAME):
    try :
        cursor.execute('drop database if exits {};'.format(DB_NAME))
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8' ;".format(DB_NAME ))
    except mc.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

def main(*args , **kwargs):
    TABLES = {}
    # Name is a useless column just for test
    table_Creation = '''Create Table emails(
            email varchar(128) NOT NULL ,
            Name   varchar(14) NOT NULL ,
            PRIMARY KEY (email)
    ) ENGINE=InnoDB '''

    TABLES['emails'] = table_Creation
    config = {
    'user': 'root',
    'password': os.environ.get("database_password"),
    'host': '127.0.0.1',
    }
    # software test maybe  !
    DB_NAME = 'AzmoonNarm'
    cnx = mc.connect(**config)
    cursor = cnx.cursor(buffered=True)
    try:
        cursor.execute("USE {}".format(DB_NAME))
        cursor.execute('drop table if exists emails ;')

    except mc.Error as err:
        # print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            Create_connect_database(cursor, DB_NAME)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            # print(err)

            exit(1)


    # print("lets created the table ")

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            # print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
            # print("it is executed ")
        except mc.Error as err:
            # print("is it not created ?")
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
                pass
            else:
                print(err.msg)
                pass
        else:
            # print("OK")
            pass


    add_email = ("INSERT INTO emails "
               "(email , Name) "
               "VALUES (%s, %s)")

    for mails in args[0]:
        cursor.execute(add_email, (mails ,'23'))


    cnx.commit()

    cursor.close()
    cnx.close()


