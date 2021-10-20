import datetime
from logging import error
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from mysql.connector.errors import custom_error_exception


def openconnection():
    # db
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
    
    #if got error
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            # print("Something is wrong with your user name or password")
            raise Exception("dog ate the paper containing the credentials..")
            
            
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            raise Exception("dog ate my db..?")
            
        else:
            print(err)
            raise Exception(err)

    #if no error
    else:
        cursor = cnx.cursor()
        return cnx, cursor 


def closeconnection(cnx,cursor):

    cnx.commit()
    cursor.close()
    cnx.close()




#to refractor       
def insertfeedback(data):
    print("insert feedback")
    cnx, cursor = openconnection()

    # try:
    #     dbconfig = {
    #         "user" :'bot',
    #         "password" :"13Eddie07",
    #         "database": "codingfeedback",
    #     }

    #     cnx = mysql.connector.connect(
    #         **dbconfig
    #     )
    #     cursor = cnx.cursor()
    
    feedback = (
        "INSERT INTO feedback"
        "(attendeename, username,id,attendance,takeaway,improvement,question) "
        "VALUES (%s, %s, %s,%s, %s, %s, %s)")

    feedbackdata = tuple(data.values())        
    cursor.execute(feedback,feedbackdata)
    closeconnection(cnx,cursor)
    #     cnx.commit()
    #     cursor.close()
    #     cnx.close()

    # #if got error
    # except mysql.connector.Error as err:
    #     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    #         print("Something is wrong with your user name or password")
    #         raise Exception("dog ate the paper containing the credentials..")
            
            
    #     elif err.errno == errorcode.ER_BAD_DB_ERROR:
    #         print("Database does not exist")
    #         raise Exception("dog ate my db..?")
            
    #     else:
    #         print(err)
    #         raise Exception(err)
            

def getallfeedback():
    print("get feedback")
    cnx, cursor = openconnection()

    query = ("SELECT * FROM feedback ")

    for result in cursor.execute(query, multi=True):
            if result.with_rows:
                print("Rows produced by statement '{}':".format(
                result.statement))
                #print(result.fetchall())
                theresult = result.fetchall()

                #all the data
                return theresult

            else:
                print("Number of rows affected by statement '{}': {}".format(
                result.statement, result.rowcount))


    # query = ("SELECT * FROM feedback "
    #      "WHERE hire_date BETWEEN %s AND %s")
    # cursor.execute(query, (hire_start, hire_end))

    closeconnection(cnx,cursor)

############################



#to refractor       
def insertquestion(data):
    print("insert question")
    cnx,cursor = openconnection()

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
    closeconnection(cnx,cursor)
    # try:
    #     dbconfig = {
    #         "user" :'bot',
    #         "password" :"13Eddie07",
    #         "database": "codingfeedback",
    #     }

    #     cnx = mysql.connector.connect(
    #         **dbconfig
    #     )
    #     cursor = cnx.cursor()
    
    

        # questiondata = tuple(data.values())        
        # print(questiondata)
        # if( len(questiondata) == 4):    
        #     question = (
        #         "INSERT INTO question"
        #         "(username,id,question,code) "
        #         "VALUES (%s, %s, %s,%s)")

        # else:
        #     question = (
        #         "INSERT INTO question"
        #         "(username,id,question) "
        #         "VALUES (%s, %s, %s)")

        # cursor.execute(question,questiondata)
        # cnx.commit()
        # cursor.close()
        # cnx.close()

    #if got error
    # except mysql.connector.Error as err:
    #     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    #         print("Something is wrong with your user name or password")
    #         raise Exception("dog ate the paper containing the credentials..")
            
            
    #     elif err.errno == errorcode.ER_BAD_DB_ERROR:
    #         print("Database does not exist")
    #         raise Exception("dog ate my db..?")
            
    #     else:
    #         print(err)
    #         raise Exception(err)
            

def getquestions():
    cnx, cursor = openconnection()

    query = ("SELECT * FROM question")

    for result in cursor.execute(query, multi=True):
            if result.with_rows:
                print("Rows produced by statement '{}':".format(
                result.statement))
                #print(result.fetchall())
                theresult = result.fetchall()

                #all the data
                return theresult

            else:
                print("Number of rows affected by statement '{}': {}".format(
                result.statement, result.rowcount))

    closeconnection(cnx,cursor)

#telegram username
def getquestionbytele(username):
    cnx, cursor = openconnection()

    query = ("SELECT question,code FROM question"
        "WHERE username = '{}'".format(username) )
    


    query = 'select * from question where username = "{}" ;'.format(username)

    for result in cursor.execute(query,multi = True):
            if result.with_rows:
                print("Rows produced by statement '{}':".format(
                result.statement))
                #print(result.fetchall())
                theresult = result.fetchall()
                print(theresult)
                #all the data
                return theresult

            else:
                print("Number of rows affected by statement '{}': {}".format(
                result.statement, result.rowcount))
                print("else")
                print(result)
                

    closeconnection(cnx,cursor)

