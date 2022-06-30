import telebot
from telebot import types
import requests as rq  
from bs4 import BeautifulSoup as BS  
  
URL = 'https://yandex.kz/maps/163/nur-sultan/stops/stop__10011009'
URL2 = "https://yandex.kz/maps/163/nur-sultan/stops/stop__10011058"
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36', 'accept': '*/*'}  
  
def get_html(url, params=None):  
    r = rq.get(url, headers=HEADERS, params=params)  
    return r  
  
def get_content(html):  
    soup = BS(html, 'html.parser')  
    items = soup.find_all('li', class_ = 'masstransit-vehicle-snippet-view _clickable _type_bus')  
  
    Bus = [] 
    for item in items:  
        #number os bus  
        num = item.find('a', class_ = 'masstransit-vehicle-snippet-view__name')  
        if num:  
            num = num.get_text()  
        else:  
            num = 'Null'  
        #time for dom ministerstv  
        time = item.find('span', class_ = 'masstransit-prognoses-view__title-text')  
        if time:  
            time = time.get_text()  
        else:                              
            time = item.find('span', class_ = 'masstransit-prognoses-view__every-value').get_text()  
        if time == 'келеді':  
                time = 'подъезжает'  
        elif 'әр' in time:  
            temp = 'каждые ' + time[2:5] + ' мин'  
            time = temp  
        Bus.append('Автобус: ' + num + ", ") 
        Bus.append('Время: ' + time + '\n') 
    return Bus 
      
html = get_html(URL)  
Buss = get_content(html.text) 

html2 = get_html(URL2)
Buss2 = get_content(html2.text)
bot = telebot.TeleBot('5511831490:AAHIzJrn2dd1uHGI1TDnkxa6sLwATUWcMNA')  
  
@bot.message_handler(commands=['start'])  
def start(message):   
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,)
    btn1 = types.KeyboardButton("Дом министреств")
    btn2 = types.KeyboardButton("Министерство иностранных дел")
    btn3 = types.KeyboardButton("Министерство иностранных дел")
    markup.add(btn1, btn2, btn3)
    markup.add(btn1, btn2, btn3)
    markup.add(btn1, btn2, btn3)
    markup.add(btn1, btn2, btn3)
    markup.add(btn1, btn2, btn3)
    markup.add(btn1, btn2, btn3)
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(message.chat.id, '<b>Привет. Я бот, который может помочь тебе с расписанием автобусов</b>', parse_mode='html', reply_markup=markup)
    
  
@bot.message_handler(func=lambda message: True)  
def businfo(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Дом министреств")
    btn2 = types.KeyboardButton("Министерство иностранных дел")
    markup.add(btn1, btn2)
    if message.text == "Дом министреств":
        bot.send_message(message.chat.id,''.join(map(str, Buss)), parse_mode='html')
        pass
    if message.text == "Министерство иностранных дел":
        bot.send_message(message.chat.id, ''.join(map(str, Buss2)), parse_mode='html') 


        # bot.send_message(message.chat.id, 'Информация о прибытии автобусов на остановку "Дом министреств"', parse_mode='html',)  
        # bot.send_message(message.chat.id, ''.join(map(str, Buss)), parse_mode='html',)  
  
bot.polling(none_stop=True)
