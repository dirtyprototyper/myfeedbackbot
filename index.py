'''
start: feedback (users)
question : normal asking question (users)
manual: owner replying. Need chatid & message.
cancel: quitting and ending the conversation (all of the above. it ends the conversation regardless of state)

What's avaiilable on the bot for firebase:
Available:
inserting feedback. (feedback)
inserting question. (question). To implement the code feature and S3.
Answering specific question to the user who asked. (manual)


Not Available(on telegram):
Not returning all feedback.
Not returning all question.


ToDo:
1. To finish up sql for workbench. (refractored inserted. Will need to do a "get") [done]
2. Move everything to Firebase (Basic get and insert is there. to test it out. To upload stuff to s3)
3. Test if it works on S3 with Firebase (to test if firebase and angular works even when hosting on s3)
4. Refractoring (config file, index.py)
5. link to angular
'''

from contextvars import Token
import logging
from warnings import filters
from mysql.connector import Error
import uuid

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, constants
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    conversationhandler,
)
#for mysql workbench
# from config import  getallfeedback, getquestionbytele, insertfeedback, insertquestion

from firebase import insertfeedback, getallfeedback, insertquestion, getquestionbytele, getallquestion, uploadfile

from dotenv import load_dotenv


# from s3ops import upload_file
load_dotenv()
import os
bottoken = os.environ.get('TOKEN')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

#feedback
ATTENDANCE, TAKEAWAY, IMPROVEMENT, QUESTION = range(0,4)
#question
QUERY,PHOTO, CODE = range(4,7)
ANSWER,REPLY= range(7,9)
#manual reply


def start(update: Update, context: CallbackContext) -> int:

    
    """Starts the conversation."""
    reply_keyboard = [['Day1', 'Day2', "Both"]]

    update.message.reply_text(
        'Hi! My name is feedback_to_bot.\nPlease kindly feedback about the session so that we can improve :). '
        'Send /cancel to stop talking to me.\n\n'
        'Which day did you attend?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Day 1, Day 2, Both'
        ),
    )

    return ATTENDANCE


    
def attendance(update: Update, context: CallbackContext) -> int:
    """collect basic information of user"""
    user = update.message.from_user

    logger.info("User: %s, attended on: %s",user.first_name, update.message.text)
    #storing data in dict
    if (user.last_name != None):
        context.user_data["name"] = user.first_name + " " + user.last_name
    else:
        context.user_data["name"] = user.first_name 
        
    context.user_data["username"] = user.username
    context.user_data["id"] = user.id
    context.user_data["attendance"] = update.message.text
    #end of storing data

    update.message.reply_text(
        'I see! Please tell me your key takeaway or something you enjoyed.\n'
        'so I know what we did well.',
        reply_markup=ReplyKeyboardRemove(),
    )

    return TAKEAWAY

def takeaway(update: Update, context: CallbackContext) -> int:
    """collect user's takeaway"""
    
    #storing data in dict
    context.user_data["takeaway"] = update.message.text
    
    user = update.message.from_user
    logger.info(update.message.text)
    update.message.reply_text(
        'I see! Please tell me something that we should improve on.\n',
        # 'so I know what we did well.',
        reply_markup=ReplyKeyboardRemove(),
    )

    return IMPROVEMENT

def improvement(update: Update, context: CallbackContext) -> int:

    """collect user's feedback for improvement"""
    context.user_data["improvement"] = update.message.text

    user = update.message.from_user
    logger.info(update.message.text)
    update.message.reply_text(
        'Is there anything you would like to ask about?.\n We will reply to these questions asap',
        # 'so I know what we did well.',
        reply_markup=ReplyKeyboardRemove(),
    )

    return QUESTION

def question(update: Update, context: CallbackContext) -> int:
    '''collect user's question if any'''
    context.user_data["question"] = update.message.text

    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    
    try: 
        insertfeedback(context.user_data)
    
    except Exception as e:
        print("Error")
        print(e)
        update.message.reply_text("There's is an error.. Try again later")

    else:
        # print("else")
        update.message.reply_text('Thank you! We hope to see you in our events in the future :).')
        

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

# for asking question
def query(update: Update, context: CallbackContext) -> int:

    update.message.reply_text(
        'Hi! My name is feedback_to_bot.\nPlease kindly feedback about the session so that we can improve :). '
        'Send /cancel to stop talking to me.\n\n'
        'Ask Away!',
    )    
    # print(update.message.chat_id)


    return CODE

def code(update: Update, context: CallbackContext) -> int:
    print("code")
    update.message.reply_text(
        'Send me the code if any. \n'
        '/skip to skip',
    )    

    user = update.message.from_user

    context.user_data["username"] = user.username
    context.user_data["id"] = user.id
    context.user_data["question"] = update.message.text

    return QUERY


def skip(update: Update, context: CallbackContext) -> int:
    print("skip")
    # user = update.message.from_user
    # logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text(
        'No Code received.\n Okie :). Wait for hooman now'
    )
    # context.user_data["code"] = update.message.text

    #to insert data into table for question
    insertquestion(context.user_data)
    return ConversationHandler.END

import threading

def acknowledge(update: Update, context: CallbackContext) -> int:
    print("acknowledges")
    
    #writing the file
    filename = uuid.uuid1()
    context.user_data['filename'] = str(filename)

   
    # f = open( "codes/" + str(filename), "a")
    # f.write(update.message.text)
    # f.close
   

    
    # uploadfile("codes/" + str(filename)+ ".txt" )
    uploadfile(filename, update.message.text )



    # insertquestion(context.user_data)


    update.message.reply_text("Code received.\nOkie, wait for hooman now")



    #to insert data into table for quesiton

    return ConversationHandler.END
#end of asking question



#manually answer questions.
#to do: add db features
def manual(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Okie, give me the id")
    print("manual")    
    return ANSWER

def answer(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("the answer?")
    
    #this is the chatid
    # print(update.message.text)
    context.user_data["chat_id"] = update.message.text

    return REPLY

def reply(update: Update, context: CallbackContext) -> int:
    #this is the anwer
    # print(update.message.text)

    #chat_id to be dynamic
    context.bot.send_message(
        chat_id= context.user_data["chat_id"],
        text = update.message.text  
    )
    return ConversationHandler.END
#end of manual


def main() -> None:
    print(bottoken)
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(bottoken) 
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    #/start
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ATTENDANCE: [MessageHandler(Filters.regex('^(Day1|Day2|Both)$'), attendance)],
            TAKEAWAY: [MessageHandler(Filters.text & ~Filters.command,takeaway )],
            IMPROVEMENT: [MessageHandler(Filters.text & ~Filters.command,improvement) ],
            QUESTION: [MessageHandler(Filters.text & ~Filters.command, question)],
            # FEEDBACK2: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],

            # FEEDBACK3: [
            #     MessageHandler(Filters.location, location),
            #     CommandHandler('skip', skip_location),
            # ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    #/question
    question_handler= ConversationHandler(
        entry_points=[CommandHandler('question', query)],
        states={
            CODE: [MessageHandler(Filters.text, code)],
            QUERY: [MessageHandler(Filters.text & ~Filters.command, acknowledge), CommandHandler('skip', skip)],

        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(question_handler)


    #/manual
    manual_handler = ConversationHandler(
        entry_points=[CommandHandler('manual',manual)],
        states={
            ANSWER:[MessageHandler(Filters.text & ~Filters.command, answer)],
            REPLY: [MessageHandler(Filters.text & ~Filters.command, reply)],
        },
        
        fallbacks   = [CommandHandler('cancel',cancel)],
    )
    # manual.add_handler(manual_handler)
    dispatcher.add_handler(manual_handler)

    # Start the Bot
    updater.start_polling()



    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

