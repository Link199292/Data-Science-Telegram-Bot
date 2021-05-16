from background_functioning import *
from check_status import *
import re
import json
import logging

LOG_FORMAT = "%(levelname)s: %(asctime)s - %(message)s"
logging.basicConfig(filename="bot.log", level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger()



admins_user_ids = ['AdminCode1', 'AdminCode2']
curriculum = "B"

with open("lectures.json") as json_lectures:
    diz = json.load(json_lectures)

def callback(bot, update):
    global curriculum

    if 'message' in update:
        # messages "handler"
        message_id = update['message']['message_id']  # https://core.telegram.org/bots/api#message
        #id univoco utente
        user_id = update['message']['from']['id']
        chat_id = update['message']['chat']['id']
        text = update['message']['text']
        try:
            first_name = update['message']['from']['first_name']
        except:
            first_name = ""
        try:
            last_name = update['message']['from']['last_name']
        except:
            last_name = ""
        try:
            username = update['message']['from']['username']
        except:
            username = ""

        white_lst = []
        pending_lst = []
        
        with open("pending_list.txt", "r") as f:
            line = f.readline()
            pending_lst.append(line.rstrip("\n"))
            while line != "":
                line = f.readline()
                if line != "":
                    pending_lst.append(line.rstrip("\n"))

        with open("whitelist.txt", "r") as f:
            line = f.readline()
            white_lst.append(line.rstrip("\n"))
            while line != "":
                line = f.readline()
                if line != "":
                    white_lst.append(line.rstrip("\n"))

        #check if user is inside white list
        status = check_status(user_id, white_lst)

        #WELCOME
        if text == '/start':
            bot.sendMessage(chat_id = chat_id, text = "Here you can find some useful informations about Data Science's course.\n\nMain commands:\n\n/start\n/lessons", parse_mode = "markdown")
            if not status:
                bot.sendMessage(chat_id = chat_id, text = "Almost forgot!\nIf it's your first time here, remember to make a request:\n\n/permission", parse_mode = "markdown")  # you can find method parameters in https://core.telegram.org/bots/api#sendmessage

        #ASK FOR PERMISSION OR CHECK REQUEST STATUS
        if text == "/permission":
            if str(user_id) not in pending_lst and str(user_id) not in white_lst:
                logger.info("/permission called")
                bot.sendMessage(chat_id = chat_id, text = "Your request has been sent. We're going to process it as soon as possible.")
                #then append user_id in the lst and update the associated file
                with open("pending_list.txt", "a", encoding = "utf-8") as f_in:
                    if str(user_id) not in pending_lst:
                        f_in.write(f"{user_id};{first_name};{last_name};{username}\n")
                        pending_lst.append(user_id)
            elif str(user_id) in white_lst:
                bot.sendMessage(chat_id = chat_id, text = "You're in!")
            elif str(user_id) in pending_lst:
                bot.sendMessage(chat_id = chat_id, text = "Your request is pending. Just be patient.")

        #ADMINS COMMANDS:
        if str(user_id) in admins_user_ids:
            if text == "/pending":
                result = ""
                for i in pending_lst:
                    try:
                        pending_id, pending_first, pending_last, pending_user = i.split(";")
                        x = " ".join(i.split(";"))
                        result += f"id: {pending_id}\nname: {pending_first} {pending_last}\nusername: {pending_user}\n/approve_{pending_id}\n\n"
                    except:
                        result = "No users in pending"
                bot.sendMessage(chat_id = chat_id, text = result)

            my_regexp = "/approve_(\d)+"
            command = text
            m = re.search(my_regexp, command)
            if m:
                pending_id = command.split("_")[-1]
                for i in pending_lst:
                    if i.split(";")[0] == pending_id:
                        pending_lst.remove(i)
                with open("pending_list.txt", "w", encoding = "utf-8") as f_in:
                    f_in.write("\n".join(pending_lst))
                if pending_id not in white_lst:
                    with open("whitelist.txt", "a") as f_in:
                        f_in.write(f"{pending_id}\n")

        #EACH COMMAND THAT REQUIRES PERMISSION HAS TO BE INSIDE THIS "IF" statment

        if status or str(user_id) in admins_user_ids:
            if text == "/lessons":
                logger.info("/lessons called")
                bot.sendMessage(chat_id = chat_id, text = "/Curriculum_A\n\n/Curriculum_B")
            if text[:-2] == "/Curriculum":
                if text[-1] == "A":
                    curriculum = "A"
                    logger.info("/Curriculum_A called")
                elif text[-1] == "B":
                    curriculum = "B"
                    logger.info("/Curriculum_B called")
                result = "Click one of the following lessons to see their informations:\n\n"
                for i in diz[curriculum].keys():
                    result += f"/{'_'.join(i.split())}\n\n"
                    
                bot.sendMessage(chat_id = chat_id, text = result)
            if " ".join(text.split("_"))[1:] in diz[curriculum].keys():
                unslashed_lesson = " ".join(text.split("_"))[1:]
                result = f"*{unslashed_lesson}*\n\n"
                for i, j in diz[curriculum][unslashed_lesson].items():
                    if j != "":
                        result += f"{i}: {j}\n\n"
                        logger.info(i + "called")
                bot.sendMessage(chat_id = chat_id, text = result, parse_mode = "markdown")


bot = EzTG(token = 'YourAPIHere', callback=callback)
