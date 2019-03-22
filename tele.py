import requests
import json
import datetime, time 
from telegram.ext import Updater, CommandHandler, InlineQueryHandler
import re

my_token = '874835868:AAFLxi1FzSXsuI9tzCeUvbvsXI0yqRkFkCM'
url_base = 'https://api.telegram.org/bot{}/'.format(my_token)



def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

# def bop(bot, update):
#     url = get_url()
#     chat_id = update.message.chat_id #recipient chat id
#     bot.send_photo(chat_id=chat_id, photo=url) #sendphoto(chat_id,photo)



def availability(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='i am availability '+'\n'+'/availability')


def start(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, 
    text='Welcome to SMT ilaundry, your one-stop best SMU laundry services!' +'\n'
    + 'Show entire availability table pls press /availability' + '\n'
        + 'get prompt press /prompt /washing_machine /dryer /yes /no')

def prompt(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='i am prompt '+'\n'+'/prompt')

def washingMachine(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='i am wm '+'\n'+'/prompt')


def dryer(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='i am dryer '+'\n'+'/prompt')


def yes(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='i am yes '+'\n'+'/prompt')

def no(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='i am no '+'\n'+'/prompt')


def main():
    updater = Updater(my_token)
    dp = updater.dispatcher #Dispatcher that handles the updates and dispatches them to the handlers.
    #dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('prompt',prompt))
    dp.add_handler(CommandHandler('washing_machine',washingMachine))
    dp.add_handler(CommandHandler('dryer',dryer))
    dp.add_handler(CommandHandler('yes',yes))
    dp.add_handler(CommandHandler('no',no))

    dp.add_handler(CommandHandler('availability',availability)) #add_handler(handler),register a handler
    updater.start_polling() #pull updates from telegram
    updater.idle() #stop signals

if __name__ == '__main__':
    main()


# url_getMe = '{}getme'.format(url_base)
# url_getUpdates = '{}getupdates'.format(url_base)
# url_sendMsg = '{}sendMessage'.format(url_base)





# here, we define common functions that we can use
# def print_pretty_json(json_object):
#     print(json.dumps(json_object, indent=2, sort_keys=True))
#     return 


# def send_welcome_msg():

#     # write your code here
#     params = {'chat_id':chat_id, 'text': Welcome_msg}
#     r = requests.post(url_sendMsg, params)
    
#     # your code should end above this line 
#     return r.json()
        
# send_welcome_msg()



# def listen_and_echo(chat_id):
#     # write your code here 
#     r = requests.get(url_getUpdates)
#     r = r.json()
#     i = 0
#     if len(r['result']) != 0:
#         current_end = r['result'][len(r['result'])-1]['message']['date']
#     print (current_end)

#     while len(r['result']) != 0:
#         r = requests.get(url_getUpdates)
#         r = r.json()
#         if current_end != r['result'][len(r['result'])-1]['message']['date']:
#             x = r['result'][len(r['result'])-1]['message']['date']
#             chat_id = r['result'][len(r['result'])-1]['message']['from']['id']
#             text = r['result'][len(r['result'])-1]['message']['text']
 
#             resend = text
#             params = {'chat_id': chat_id, 'text':resend }
#             r = requests.post(url_sendMsg, params)


#             current_end = x
#         time.sleep(1)
    


# listen_and_echo(chat_id)