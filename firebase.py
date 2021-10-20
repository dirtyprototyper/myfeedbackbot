#to do: Firebase

import firebase_admin
from firebase_admin import credentials, db,  firestore, storage
from telegram.ext.filters import Filters

cred = credentials.Certificate("secrets/feedback-c70af-firebase-adminsdk-8xs5g-b1ef000417.json")

default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':"https://feedback-c70af-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': 'feedback-c70af.appspot.com'

	})


# putting data
# ref = db.reference("/users/")

# ref.push({
#         'date_of_birth': 'June 24, 1912',
#         'username': 'xxyxyx',
#         'name': 'yyyxy',
#         'full_name': 'Gracee Hopper'

# })
#end

#getting data
# ref = db.reference("/users/")
# best_sellers = ref.get()
# print(best_sellers)

# for key, value in best_sellers.items():
#     if(value["name"] == "yyyy"):
#         print(key) #-MmCD8WtmZxAwgWAWKlj
#         print(value)   #{'date_of_birth': 'June 24, 1912', 'full_name': 'Gracey Hopper', 'name': 'yyyy', 'username': 'xxyyx'}
#end        


#############
# Feedback
#inserting feedback. To do
def insertfeedback(data):
    print(data)
    print(data['name'])
    
    ref = db.reference("/feedback/")
    ref.push({
            'attendeename': data['name'],
            'username': data['username'],
            'id': data['id'],
            'attendance': data['attendance'],
            'takeaway': data['takeaway'],
            'improvement': data['improvement'],
            'question': data['question']
    })

#to amend the data. Revised: no need to get a single feedback
#get a user feedback
# def getauserfeedback(name):
#     ref = db.reference("/feedback/")
#     data = ref.get()
#     print(data)

#     for key, value in data.items():
#         if(value["change_this_line"] == name):
#             print(key) #-MmCD8WtmZxAwgWAWKlj
#             print(value)   #{'date_of_birth': 'June 24, 1912', 'full_name': 'Gracey Hopper', 'name': 'yyyy', 'username': 'xxyyx'}

#get all feedback
def getallfeedback():
    print('getallfeedback')
    ref = db.reference("/feedback/")
    data = ref.get()
    # print(data)
    
    #single 'object' without the key.
    # for x in data.values():
    #     print(x)

    
    
    





############################
#question
def insertquestion(qn):
    print(qn)
    ref = db.reference("/question/")
    ref.push({
        'username': qn['username'],
        'id': qn['id'],
        'question': qn['question'],
        "code": qn["filename"]
    })




#get all question
def getallquestion():
    ref = db.reference("/question/")
    data = ref.get()
    print(data)


#get a user question
def getquestionbytele(username):
    ref = db.reference("/question/")
    data = ref.get()
    # print(data)

    for key, value in data.items():
        if(value["username"] == username):
            print(key) #-MmCD8WtmZxAwgWAWKlj
            print(value)   #{'date_of_birth': 'June 24, 1912', 'full_name': 'Gracey Hopper', 'name': 'yyyy', 'username': 'xxyyx'}



############## FILE STORAGE ##############################
import os


# db = firestore.client()
bucket = storage.bucket()

#https://stackoverflow.com/questions/52883534/firebase-storage-upload-file-python
def uploadfile(filename, filecontent):
    print("uploadfile")

    #setting file name
    filename = str(filename) + ".txt"

    #writing the file
    f = open("codes/" + filename, "a")
    f.write(filecontent)
    f.close
    #end of writing the file

    #creating the 'file' in firebase
    blob = bucket.blob(filename)

    #Getting the directory with file
    dirname = os.path.dirname(__file__)
    adirectory = os.path.join(dirname+"\\codes\\",  filename )

    #check file content to ensure it is there
    with open(adirectory, 'r') as f:
        print(f.read())

    #upload to firebase
    with open(adirectory, "rb") as adirectory:
        blob.upload_from_file(adirectory)
        blob.make_public()
        print(blob.public_url)

    #test with erturn
    allfile(filename)


import datetime
import requests


#gets you a single file with its file name.
#needs to be ***.txt
def allfile(filename):
    print("all file. jk, single file only")

    #locate the file in the bucket
    blob = bucket.blob(filename)

    #genereate signature so that it can be downloaded
    url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')

    r = requests.get(url)
    
    #save the file
    open("code/"+ filename, 'wb').write(r.content)







