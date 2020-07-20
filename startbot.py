import telebot
import requests
import os
import cv2
import utils

bot = telebot.TeleBot( utils.token )


#Handle command /start
@bot.message_handler(commands=['start'])
def send_start(message):
    bot.send_message(message.chat.id, 'Hello! Send photos with face or voice messages!')


@bot.message_handler(content_types=[ 'text' ])
def send_text( message ):
    if message.content_type == 'text':
        bot.send_message( message.chat.id, 'Send photos with face' )


#Handle photos
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        #Get file id for download
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)

        #Create user id folder
        os.makedirs(utils.photos[0] + str(message.from_user.id), exist_ok=True)
        count_files = utils.countFiles(
            utils.photos[0] + str(message.from_user.id)
        )

        #Get file object
        downloaded_file = bot.download_file(file_info.file_path)

        #If photo without faces
        if not utils.isFace(downloaded_file):
            bot.reply_to(message , "NO FACE") 
            print( message.from_user.username + ' send photo without face')
        else:
            #Save photo with faces
            utils.savePhoto(message.from_user.id, downloaded_file, count_files )
            bot.reply_to(message ,"FACE. SAVED")
            print(message.from_user.username + ' send photo with face')
    except Exception as e:
        print(e)



#Handle voice messages
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    try:
        #Get file id for download
        file_info = bot.get_file(message.voice.file_id)

        #Create user id folder
        os.makedirs(utils.voices[0] + str(message.from_user.id), exist_ok=True)
        count_files = utils.countFiles(
            utils.voices[0] + str(message.from_user.id)
        )

        #Get file object
        downloaded_file = bot.download_file(file_info.file_path)

        #Save object to file
        utils.saveVoice (message.from_user.id, downloaded_file,count_files)
        print(message.from_user.username + ' send voice message. duration= ' + str(message.voice.duration))

        #Convert OGG to WAV
        utils.oggToWav(utils.generatePath('voice', message.from_user.id, count_files))
    except Exception as e:
        print(e)


#Handle docs
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    bot.send_message(message.chat.id, 'Hello! Send photos with face or voice messages!')   



utils.setUp()
bot.polling(none_stop=True, interval=0)
