import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('7020103895:AAEKOpg07idMUJu3RY7lvMLEY29UmhfYCoM')

id = None
turName = None
descr = None
info = ''
balance = 0
nick = ''
adress = ''
id = ''
link = ''
numparticipants = 0
price = 0
admins = 'lT_e_m_4_i_kl'
numuser = 0
maxusers = 0

@bot.message_handler(commands=['start'])
def start(message):
    
    global nick
    global adress
    global id
    global numuser

    nick = message.from_user.first_name
    adress = message.from_user.username
    id = message.from_user.id

    connection = sqlite3.connect('TestBase.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS Tur (id INTEGER PRIMARY KEY,turname TEXT NOT NULL,descript TEXT, organ TEXT, link TEXT, price INTEGER, numuser INTEGER, maxusers INTEGER)')
    connection.commit()
    connection.close()

    connection = sqlite3.connect('TestBase.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY,name TEXT NOT NULL,adress TEXT NOT NULL, balance INTEGER)')
    connection.commit()
    connection.close()

    connection = sqlite3.connect('TestBase.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users (name, adress, balance) VALUES (?, ?, ?)', (nick,adress,balance))
    connection.commit()
    connection.close()

    keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)    
    Rbtn1 = types.KeyboardButton('Пользовательские турниры')
    Rbtn2 = types.KeyboardButton('Профиль')
    Rbtn3 = types.KeyboardButton('Мои турниры 🔒')

    keybord.row(Rbtn1)
    keybord.row(Rbtn2)
    keybord.row(Rbtn3)
    
    welcomMessage = f'Привет, <b>{message.from_user.first_name}</b>\nДля получения информации о боте введи: /help'
    bot.send_message(message.chat.id, welcomMessage, parse_mode='html', reply_markup=keybord)
    

# @bot.message_handler(commands=['test'])
# def test(message):
#     connection = sqlite3.connect('TestBase.db')
#     cursor = connection.cursor()
#     cursor.execute(f"UPDATE Users SET balance = '0' WHERE adress = 'lT_e_m_4_i_kl'")
#     connection.commit()
#     print('GOOD')


@bot.message_handler(commands=['help'])
def help(message):
    helpMessage = 'Информация о боте... её нет('
    bot.send_message(message.chat.id, helpMessage, parse_mode='html')


@bot.message_handler(commands=['GO'])
def GO(message):

            checkadress = str(message.from_user.username)

            connection = sqlite3.connect('TestBase.db')
            cursor = connection.cursor()
            cursor.execute(f"SELECT link FROM Tur WHERE id ='1'")
            link = str(cursor.fetchone())[2:][:-3]
            connection = sqlite3.connect('TestBase.db')
            cursor = connection.cursor()
            cursor.execute(f"SELECT balance FROM Users WHERE adress = '{checkadress}'")
            userbalance = str(cursor.fetchone())[1:][:-2]
            connection = sqlite3.connect('TestBase.db')
            cursor = connection.cursor()
            cursor.execute(f"SELECT price FROM Tur WHERE id ='1'")
            price = str(cursor.fetchone())[1:][:-2]
            connection = sqlite3.connect('TestBase.db')
            cursor = connection.cursor()
            cursor.execute(f"SELECT numuser FROM Tur WHERE id ='1'")
            numuser = str(cursor.fetchone())[1:][:-2]
            cursor = connection.cursor()
            cursor.execute(f"SELECT maxusers FROM Tur WHERE id ='1'")
            itsmaxusers = str(cursor.fetchone())[1:][:-2]
            connection.commit()

            itsmaxusers = int(itsmaxusers)
            numuser = int(numuser)
            price = int(price)
            userbalance = int(userbalance)

            if numuser >= itsmaxusers: 
                bot.send_message(message.chat.id, 'Комната уже набрана')
            elif userbalance < price:
                bot.send_message(message.chat.id, 'У вас недостаточно средств на балансе')
            else: 
                connection = sqlite3.connect('TestBase.db')
                cursor = connection.cursor()
                cursor.execute(f"UPDATE Tur SET numuser = {numuser+1} WHERE id = '1'")
                connection.commit()

                cursor.execute(f"UPDATE Users SET balance = {userbalance-price} WHERE adress = '{checkadress}'")
                connection.commit()
                bot.send_message(message.chat.id, f'• Вы успешно зарегестрированны на турнир •\nЗалетай на канал: {link}\nи ожидай код от LOBBY')
                bot.send_message(message.chat.id, '⬥При повторном вызове команды *GO\nваши средства улетят на чай админу)')    
 


@bot.message_handler(content_types=['text'])
def checkText(message):
    # global inlineKeybord
    admin = ['lT_e_m_4_i_kl', 'Okaykay123456', 'turatvv', 'Mr_BUDDA']
    
    if message.text == 'Мои турниры 🔒' and message.from_user.username in admin:
        inlineKeybord = types.InlineKeyboardMarkup()
        Ilbtn = types.InlineKeyboardButton('Создать турнир',callback_data="createTur")
        inlineKeybord.add(Ilbtn)
        bot.reply_to(message, '• Ваши турниры •', reply_markup=inlineKeybord)

    elif message.text == 'Мои турниры 🔒' and message.from_user.username != 'lT_e_m_4_i_kl' or message.from_user.username == 'Okaykay123456':
        bot.reply_to(message, '• У вас нету доступа к данному разделу •')
        

    elif message.text == 'Профиль':

        checkadress = message.from_user.username
        connection = sqlite3.connect('TestBase.db')
        cursor = connection.cursor()
        cursor.execute(f"SELECT balance FROM Users WHERE adress ='{checkadress}'")
        userbalance = str(cursor.fetchone())[1:][:-2]

        global nick
        global id
        results = ''
        row = ''

        connection = sqlite3.connect('TestBase.db')
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM Users WHERE adress = '{adress}'")
        if cursor.rowcount > 0 : 
             results = cursor.fetchall()
             for row in results :
                balance = row[3]

        bot.reply_to(message, f'• Профиль •\nНикнейм: {message.from_user.first_name}\nID:\
 {message.from_user.id}\nБаланс: {userbalance}₽')  
        bot.send_message(message.chat.id, '⬥Для пополнения и вывода баланса\nобратитесь к @lT_e_m_4_i_kl')

    elif  message.text == 'Пользовательские турниры':
                      
            connection = sqlite3.connect('TestBase.db')
            cursor = connection.cursor()
            cursor.execute(f"SELECT numuser FROM Tur WHERE id ='1'")
            numuser = str(cursor.fetchone())[1:][:-2]
            cursor = connection.cursor()
            cursor.execute(f"SELECT maxusers FROM Tur WHERE id ='1'")
            itsmaxusers = str(cursor.fetchone())[1:][:-2]
            connection.commit()
            itsmaxusers = int(itsmaxusers)
            numuser = int(numuser)

            if numuser >= itsmaxusers:

                connection = sqlite3.connect('TestBase.db')
                cursor = connection.cursor()    
                cursor.execute("DELETE FROM Tur WHERE id = '1'")

                bot.reply_to(message, 'Соревнования не найдены')

            else:
                checkadress = None
                connection = sqlite3.connect('TestBase.db')
                cursor = connection.cursor()
                cursor.execute(f"SELECT turname FROM Tur WHERE organ !='{checkadress}'")
                itisturname = str(cursor.fetchone())[2:][:-3]

                cursor.execute(f"SELECT organ FROM Tur WHERE organ !='{checkadress}'")
                itisorgan = str(cursor.fetchone())[2:][:-3]

                cursor.execute(f"SELECT descript FROM Tur WHERE organ !='{checkadress}'")
                itisdescript = str(cursor.fetchone())[2:][:-3]    

                cursor.execute(f"SELECT price FROM Tur WHERE organ !='{checkadress}'")
                itisprice = str(cursor.fetchone())[1:][:-2]


                if turName == None: bot.reply_to(message, 'Соревнования не найдены')

                
                else: fulltur = f'Название: {itisturname}\nОрганизатор: @{itisorgan}\nСтоимость участия: {itisprice}₽\nКол-во участников: {maxusers}\nОписание: {itisdescript}'

                bot.reply_to(message, f'• Доступные вам соревнования •\n{fulltur}\n...\nДля участия в турнире пропиши /GO', reply_markup='')
        
    else:
            
        bot.reply_to(message, '• Главное МЕНЮ •', reply_markup='')


@bot.callback_query_handler(func=lambda callback:True)  
def createTur(callback):
    if callback.data == 'createTur':
            bot.reply_to(callback.message, 'Введи название турнира')
            bot.register_next_step_handler(callback.message, on_click)     
           
def on_click(message):
        global turName
        turName = message.text.strip()
        bot.send_message(message.chat.id, 'Введи описание турнира')
        bot.register_next_step_handler(message, on_click2)

def on_click2(message):
        global descr
        descr = message.text.strip()
        bot.send_message(message.chat.id, 'Укажи ссылку на ТГ канал для тех,\nкто оплатил вход')
        bot.register_next_step_handler(message, on_click3)

def on_click3(message):
        global link
        link = message.text.strip()
        bot.send_message(message.chat.id, 'Введи стоимость турнира')
        bot.register_next_step_handler(message, on_click4)

def on_click4(message):
        global link
        global descr
        global price
        price = message.text.strip()
        bot.send_message(message.chat.id, 'Введи количество участников')
        bot.register_next_step_handler(message, on_click5)


def on_click5(message):
        global maxusers
        maxusers = message.text.strip()
        organizer = message.from_user.username
        readyTur = f'•Турнир создан•\n[ Название: {turName}\nОрганизатор: @{organizer}\nСтоимость участия: {price}₽\nКол-во участников: {maxusers} ]\n\
Описание: {descr}'

        
    
        connection=sqlite3.connect('TestBase.db')
        cursor=connection.cursor()
        cursor.execute("DELETE FROM Tur WHERE id > 0")
        connection.commit()
        connection.close()

        connection = sqlite3.connect('TestBase.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Tur (turname, descript, organ, link, price, numuser, maxusers) VALUES (?, ?, ?, ?, ?, ?, ?)', (turName, descr, organizer, link, price, numuser, maxusers))
        connection.commit()
        connection.close()

        bot.send_message(message.chat.id, f'{readyTur}',reply_markup='')

# bot.polling()    

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e: 
            print('❌❌❌❌❌ Сработало исключение! ❌❌❌❌❌')