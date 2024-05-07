import telebot #pip install telebot
import tube

bot = telebot.TeleBot('') #Ключ от тг бота

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я бот. Как дела?')

@bot.message_handler(commands=['help'])
def help_message(message):
    string_for_help_msg = 'Команды: \nsee 1 - вывод отслеживаемых каналов построчно\nsee 2 - вывод отслеживаемых каналов 1 сообщением\n'
    string_for_help_msg += 'add Name_channel https://www.youtube.com/@Name_channel URL - добавляет новый канал\n'
    string_for_help_msg += 'del Name_channel - удаляет канал по имени\n'
    string_for_help_msg += '@Name_channel - выводид URL канала\n'
    string_for_help_msg += 'parsing - Присылает файл с отслеживанием каналов'
    bot.send_message(message.chat.id, string_for_help_msg)

@bot.message_handler(content_types=['text'])
def echo_all(message):
    command = message.text
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, чем я могу тебе помочь?')
    elif command[:3] == 'add':
        bot.send_message(message.chat.id, 'Произвожу обновление списка...Добавляю элемент')
        st = command[3:].rstrip().lstrip()
        tube.add(st)
    elif command[:3] == 'del':
        bot.send_message(message.chat.id, 'Произвожу обновление списка...Удаляю элемент')
        st = command[3:].rstrip().lstrip()
        tube.delete_elem(st)
    elif command[:5] == 'see 1':
        bot.send_message(message.chat.id, 'Лови список')
        mas_for_display = tube.display_list()
        for i in mas_for_display:
            bot.send_message(message.chat.id, i)
    elif command[:5] == 'see 2':
        mas_for_display = tube.display_list()
        string_for_display = ''
        for mes in mas_for_display:
            string_for_display += mes
        bot.send_message(message.chat.id, string_for_display)
    elif message.text.lower()[0] == '@':
        url_channel = tube.get_url(message.text.lower())
        bot.send_message(message.chat.id, url_channel)
    elif command == 'parsing':
        bot.send_message(message.chat.id, 'Начинаю работу...')
        tube.main()
        bot.send_message(message.chat.id, 'Обновление успешно завершено')
        try:
            bot.send_document(message.chat.id, open(r'result.txt', 'rb'))
        except:
            bot.send_message(message.chat.id, 'Новые видео не вышли')
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю. Напиши /help.')


bot.polling(none_stop=True, interval=1)
