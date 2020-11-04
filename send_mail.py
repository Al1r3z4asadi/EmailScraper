import smtplib
import mysql.connector  as mc 
from mysql.connector import errorcode
import os

def send_mail(link):
    DB_NAME = 'AzmoonNarm'
    table = 'emails'
    config = {
    'user': 'root',
    'password': os.environ.get('database_password'),
    'host': '127.0.0.1',
    }
    cnx = mc.connect(**config)
    cursor = cnx.cursor(buffered=True)

    try:
        cursor.execute("USE {}".format(DB_NAME))
        cursor.execute("Select email from emails")
        emails = cursor.fetchall()

    except mc.Error as err:
        # print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            # print(err)
        
            exit(1)

    # for email in emails :
        # print(email[0])




    for email in emails : 
        conn = smtplib.SMTP('smtp.gmail.com' , 587) 
        conn.ehlo()
        conn.starttls()
        conn.login(os.environ.get("email_addr") , os.environ.get("email_pass"))
        conn.sendmail(os.environ.get("email_addr") , email[0] ,
            'Subject: If you got this email means that you still checking your emails Eeh \n\n {}\n\n'.format(link)
        )

    conn.quit()
    cnx.commit()
    cursor.close()
    cnx.close()





