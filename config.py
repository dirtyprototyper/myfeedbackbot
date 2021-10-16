import datetime
from logging import error
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from mysql.connector.errors import custom_error_exception

# def openconnection():
#     # db
#     try:
#         cnx = mysql.connector.connect(
#            host='localhost',
#             database='codingfeedback',
#             username='feedbackadmin',
#             password='Password123'
#         )

#     #if got error
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Something is wrong with your user name or password")
#             exit()
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("Database does not exist")
#             exit()
#         else:
#             print(err)
#             exit()

#         #if no error
#     else:
#         cursor = cnx.cursor()
#         return cnx, cursor 


# def closeconnection(cnx,cursor):

#     cnx.commit()
#     cursor.close()
#     cnx.close()




#to refractor       
def insertfeedback(data):
    print("insert feedback")
    try:
        dbconfig = {
            "user" :'bot',
            "password" :"13Eddie07",
            "database": "codingfeedback",
            
        }

        cnx = mysql.connector.connect(
            **dbconfig
        )
        cursor = cnx.cursor()
    

        feedback = (
            "INSERT INTO feedback"
            "(attendeename, username,id,attendance,takeaway,improvement,question) "
            "VALUES (%s, %s, %s,%s, %s, %s, %s)")

        feedbackdata = tuple(data.values())        
        cursor.execute(feedback,feedbackdata)
        cnx.commit()
        cursor.close()
        cnx.close()

    #if got error
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            raise Exception("dog ate the paper containing the credentials..")
            
            
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            raise Exception("dog ate my db..?")
            
        else:
            print(err)
            raise Exception(err)
            
            


#to refractor       
def insertquestion(data):
    print("insert question")
    try:
        dbconfig = {
            "user" :'bot',
            "password" :"13Eddie07",
            "database": "codingfeedback",
        }

        cnx = mysql.connector.connect(
            **dbconfig
        )
        cursor = cnx.cursor()
    
    

        questiondata = tuple(data.values())        
        print(questiondata)
        if( len(questiondata) == 4):    
            question = (
                "INSERT INTO question"
                "(username,id,question,code) "
                "VALUES (%s, %s, %s,%s)")

        else:
            question = (
                "INSERT INTO question"
                "(username,id,question) "
                "VALUES (%s, %s, %s)")

        cursor.execute(question,questiondata)
        cnx.commit()
        cursor.close()
        cnx.close()

    #if got error
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            raise Exception("dog ate the paper containing the credentials..")
            
            
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            raise Exception("dog ate my db..?")
            
        else:
            print(err)
            raise Exception(err)
            
            