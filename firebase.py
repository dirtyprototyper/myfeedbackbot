#to do: Firebase

import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("secrets/feedback-c70af-firebase-adminsdk-8xs5g-b1ef000417.json")

default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':"https://feedback-c70af-default-rtdb.asia-southeast1.firebasedatabase.app/"
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
    ref = db.reference("/feedback/")
    ref.push({
            'username': 'xx',
            'id': 'int',
            'attendance': 'xx',
            'takeaway': 'xx',
            'improvement': 'xx',
            'question': 'x'
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
def getallfeedback(name):
    ref = db.reference("/feedback/")
    data = ref.get()
    print(data)






############################
#question
def insertquestion(qn):
    ref = db.reference("/question/")
    ref.push({
        'username': "xx",
        'id': "int",
        'question': "xx",
        "code": "link"
    })

#get a user question
def getauserquestion(username):
    ref = db.reference("/question/")
    data = ref.get()
    print(data)

    for key, value in data.items():
        if(value["username"] == username):
            print(key) #-MmCD8WtmZxAwgWAWKlj
            print(value)   #{'date_of_birth': 'June 24, 1912', 'full_name': 'Gracey Hopper', 'name': 'yyyy', 'username': 'xxyyx'}

#get all question
def getallquestion():
    ref = db.reference("/question/")
    data = ref.get()
    print(data)

