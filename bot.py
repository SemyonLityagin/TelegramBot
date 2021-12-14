from datetime import datetime
import telebot
from pathlib import Path
from telebot import types
import random
from pathlib import Path

emotion = {1: " "} #словарь пользователей с выбранными эмоциями 

texts = {}

emo_list = {}

emo_keys = []

def get_emo(index):
    get_emo_list()
    return emo_list[index]

def get_emo_list():
    index = 1
    global emo_keys
    emo_keys = []
    with open('./emotion.txt', 'r', encoding="utf-8") as outfile2:
        while True:
            emotions = outfile2.readline()
            if emotions == "": break
            emo_keys.append(str(index))
            emo_list[str(index)] = emotions[:-1]
            index+=1
            
def get_text(index, texts):
    ind = 1
    with open('./texts.txt', 'r', encoding="utf-8") as outfile2:
        while True:
            texts_list = outfile2.readline()
            if texts_list == "": break
            texts[ind] = texts_list[:-1]
            ind+=1
    return  texts[index]

def get_text_count():
    ind = 1
    with open('./texts.txt', 'r', encoding="utf-8") as outfile2:
        while True:
            texts_list = outfile2.readline()
            if texts_list == "": break
            ind+=1
    return ind


def save_emotional_state(user_id):
    #переименование аудизаписи
    with open('./' + str(user_id) + '/' +'info.txt', 'r') as outfile2:
        flag, ind, emo = outfile2.read().split()
        flag = int(flag)
        ind = int(ind)

    print(emo + " from user " + str(user_id) + " saved")
    #TO DO:
    now = datetime.now()
    with open('./' + str(user_id) + '/' +'records.txt', 'a') as outfile:
        outfile.write(str(user_id) + " " + emo + " " + now.strftime("%d_%m_%Y_%H:%M:%S\n"))
      
    p = Path('./' + str(user_id)+ '/' + 'audio.mp3')
    target = Path('./' + str(user_id)+ '/' + str(user_id)+ "+" + now.strftime("%d_%m_%Y_%H_%M_%S")+ "+"  + emo + "+" + str(ind)+'.mp3')
    p.rename(target)
    flag+=1
    if(flag%2 == 0):
        if(ind == get_text_count()):
            ind = 0
        ind+=1
    new_info = str(flag)+' '+str(ind)+' '+emo
    #перезапись данных в info.txt
    with open('./' + str(user_id) + '/' +'info.txt', 'w') as outfile:
        outfile.write(new_info)


bot = telebot.TeleBot("1886283664:AAFdKFqn-eWWWLNCQLSU9Q7-Zetc-olEYtk", parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    #создается папка пользователя
    Path('./' + str(message.from_user.id)).mkdir(parents=True, exist_ok=True)
    #создается файл с количеством раз, которое был выдан текст, и номером текста
    with open('./' + str(message.from_user.id) + '/' +'info.txt', 'w') as outfile:
        outfile.write("0 1 bob")
    emotion[message.from_user.id] = []
    bot.send_message(message.chat.id, "Используйте /get, чтобы получить текст для прочтения")
    bot.send_message(message.chat.id, "\nЗапишите голосовое сообщение с тем, как читаете текст")
    bot.send_message(message.chat.id, "\nКогда получите текст - запишите голосовое сообщение с тем, как вы его читаете")
    bot.send_message(message.chat.id, "\nПожалуйста, в ответах, где появляются кнопки - используйте их; всегда следуйте указаниям бота")

@bot.message_handler(commands=['get'])
def send_text(message):
    #чтение данных из info.txt
    try:
        with open('./' + str(message.from_user.id) + '/' +'info.txt', 'r') as outfile:
            flag, ind, emo = outfile.read().split()
            flag = int(flag)
            ind = int(ind)
    except FileNotFoundError:
        Path('./' + str(message.from_user.id)).mkdir(parents=True, exist_ok=True)
        with open('./' + str(message.from_user.id) + '/' +'info.txt', 'w') as outfile:
            outfile.write("0 1 bob")
        emotion[message.from_user.id] = []
        flag = 0
        ind = 1
        emo = "bob"
    if ind >= get_text_count():
        ind = 1
    print(message.from_user.id, flag, ind, emo)
    #выдача текста
    bot.reply_to(message, get_text(ind, texts))
    bot.send_message(message.chat.id, "\nЗапишите голосовое сообщение с тем, как читаете текст")
    new_info = str(flag)+' '+str(ind)+' '+emo
    #перезапись данных в info.txt
    with open('./' + str(message.from_user.id) + '/' +'info.txt', 'w') as outfile:
        outfile.write(new_info)
    
@bot.message_handler(func=lambda m: True)
def text_message_from_user(message):
    try:
        with open('./' + str(message.from_user.id) + '/' +'info.txt', 'r') as outfile:
            flag, ind, emo = outfile.read().split()
        ind = int(ind)
    except FileNotFoundError:
        Path('./' + str(message.from_user.id)).mkdir(parents=True, exist_ok=True)
        with open('./' + str(message.from_user.id) + '/' +'info.txt', 'w') as outfile:
            outfile.write("0 1 bob")
            emotion[message.from_user.id] = []
        flag = 0
        ind = 1
        emo = "bob"
    #Перезапись/не_перезапись/сохрание аудиозаписи
    if message.text in ['Хочу перезаписать']:
        bot.reply_to(message, get_text(ind, texts))
    elif message.text in ['Все записано верно']:
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, "Отлично", reply_markup=markup)
        send_emo_list(message)
    #Перезапись/не_перезапись/сохрание эмоциональное состояние пользователя
    elif message.text in ['Да']:
        if not(Path('./' + str(message.from_user.id) +'/audio.mp3').exists()):
            send_text(message)
        else:    
            try:
                with open('./' + str(message.from_user.id) + '/' +'rewrite.txt', 'a') as outfile:
                    outfile.write(str(emotion[message.from_user.id][len(emotion[message.from_user.id])-1]) + " " + str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S")) + ' | ')
                try:
                    emotion[message.from_user.id].pop()
                    send_emo_list(message)
                except IndexError:
                    send_text(message)
            except KeyError:
                with open('./' + str(message.from_user.id) + '/' +'rewrite.txt', 'a') as outfile:
                    outfile.write("изменения утеряны в виду отключения бота в момент записи\n")
                emotion[message.from_user.id] = ["5"]
                try:
                    emotion[message.from_user.id].pop()
                    send_emo_list(message)
                except IndexError:
                    send_text(message)
            except IndexError:
                send_text(message)
    elif message.text in ['Да.']:
        send_emo_list(message)
    elif message.text in ['Нет']:
        try:
            with open('./' + str(message.from_user.id) + '/' +'rewrite.txt', 'a') as outfile:
                outfile.write(str(emotion[message.from_user.id][len(emotion[message.from_user.id])-1]) + " " + str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S")) + '\n')
            add_emotion(message)
        except IndexError:
            send_text(message)
        except KeyError:
            send_text(message)
    elif message.text in ['Нет.']:
        with open('./' + str(message.from_user.id) + '/' +'rewrite.txt', 'a') as outfile:
            outfile.write("//---" + '\n')
        save_info(flag, ind, message)
        save_emotional_state(message.from_user.id)
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, "Эмоция записана. Повторите действие через часов 6-8.\nПросто напишите /get", reply_markup=markup)
    elif message.text in emo_keys:
        if message.from_user.id not in emotion.keys(): 
            emotion[message.from_user.id] = []
        emotion[message.from_user.id].append(emo_list[message.text])
        rewrite_emotion(message)
    elif message.text != "":
        bot.send_message(message.chat.id, "Пожалуйста, следуйте последней инструкции")
def save_info(flag, ind, message):
    try:
        full_emo = '_'.join(emotion[message.from_user.id])
    except KeyError:
        full_emo = "утеря"
    new_info = flag+' '+str(ind)+' ' + full_emo
    with open('./' + str(message.from_user.id) + '/' +'info.txt', 'w') as outfile:
        outfile.write(new_info)
    emotion[message.from_user.id] = []
def send_emo_list(message):
    #Отправляет список эмоций
    letter = ""
    bot.send_message(message.chat.id, "Выберете эмоцию (напишите только номер), что сейчас чувствуете, из списка:")
    get_emo_list()
    for i in emo_keys:
        letter += i+ " " + emo_list[i] + '\n'
    with open('./' + str(message.from_user.id) + '/' +'rewrite.txt', 'a') as outfile:
        outfile.write(str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S")) + ' ')
    bot.send_message(message.chat.id, letter)
    letter = ""
      
def add_emotion(message):
    #Создает иконку с выбором ответа
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Нет.')
    itembtn2 = types.KeyboardButton('Да.')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Хотите выбрать еще?", reply_markup=markup)
  
def rewrite_emotion(message):
    #Создает иконку с выбором ответа
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Нет')
    itembtn2 = types.KeyboardButton('Да')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Хотите изменить выбор?", reply_markup=markup)

def rewrite_voice_message(message):
    #Создает иконку с выбором ответа
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Все записано верно')
    itembtn2 = types.KeyboardButton('Хочу перезаписать')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Оцените верность записанного вами голосового сообщения", reply_markup=markup)

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    #Получение текущего времени
    now = datetime.now()
    #Предлагаем перезаписать аудио
    rewrite_voice_message(message)
    #Файл для сохранения
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    #Оп-оп, сохраняем
    scr = './' + str(message.from_user.id) + '/'+'audio'+'.mp3'
    with open(scr, 'wb') as new_file:
        new_file.write(downloaded_file)
bot.polling(none_stop=True, interval=0)
