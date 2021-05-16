# Data-Science-Telegram-Bot

This is a telegram bot which I have implemented for students of Data Science at UNITN.
With COVID we started online lessons and remembering zoom links and passwords for each lecture was upsetting.
The purpose of this bot is to make those informations handy, but, for a matter of privacy, a whitelist has been implemented.
This way, each student can make a request to access the informations, and an admin promptly receive a notification about it.
After that, is possibile to see his information (NickName, Name, Surname (if provided) and the unique Telegram ID). Because students have had created a telegram group chat to have conversations about exams, it was easy to match those users (thought as legit students) with those which requested the access to bot.

## lectures.json

this is a file containing a dictionary of dictionaries with informations about lessons, both for students of curriculum A and B.

## pending_list.txt

This is a list which contains informations about users not white listed (yet).
It's suggested to initialize this with admin telegram ID.

## whitelist.txt

This is a list populated with users which have access to lectures informations.

## background_functioning.py

Telegram API functioning

## main.py

in communication with background_functioning.py it allows to capture specific keywords and respond accordingly. This is how users can "ask" informations about lectures to the bot.
Inside this script there are some commands which are accessible by admins only (a list is initialized at the beginning).

## requirements.py

list of packages required to make this function properly.

## bot.log

is a log file which anonymously tracks some of the actions (e.g. when somebody is accessing informations about one curriculum or the other and so on)

## Acknowledgments

I want to thank [Filippo Vicari](https://github.com/filvi) for helping me on this.
