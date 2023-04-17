import telebot

from scripts import config, db_handler

bot = telebot.TeleBot(config.TOKEN)
TAG = True
new_tag_name = None
doc_type, file_id, file_name = None, None, None


def match_tag(message, d_type, f_id, f_name):
    global TAG
    global doc_type
    global file_id
    global file_name
    doc_type = d_type
    file_id = f_id
    file_name = f_name
    TAG = False
    bot.reply_to(message, text="Введите тег")


def load_file(message, tag_name, doc_type, file_id, file_name):
    try:
        db_handler.new_file(user_id=message.from_user.id,
                            tag_name=tag_name,
                            file_id=file_id,
                            f_type=doc_type,
                            file_name=file_name)
        bot.send_message(message.chat.id, text=f"Файл успешно загружен в тег '{tag_name}'!")
    except Exception:
        bot.send_message(message.chat.id, text="Что то пошло не так")
        raise Exception


def add_tag_from_message(message):
    print("debug --> зашли в обработку ввода")
    global TAG, new_tag_name
    while not TAG:
        try:
            new_tag_name = message.text
            TAG = True
        except Exception:
            bot.reply_to(message, "Что то пошло не так")
            raise Exception
    load_file(message=message, tag_name=new_tag_name, doc_type=doc_type, file_id=file_id, file_name=file_name)


def search_tag_from_message():
    pass
