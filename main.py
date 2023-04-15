from telebot import TeleBot
from scripts import config
from scripts import db_handler
#from types_handler import get_type

bot = TeleBot(config.TOKEN)
file_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    # db_handler.new_user(user_id=message.from_user.id)
    db_handler.new_tag(user_id=message.from_user.id, tag_name="Test")
    bot.send_message(message.chat.id, text="hi")
    print(message.from_user.id)  # TODO DEBUG


@bot.message_handler(content_types=['document'])
def doc_handler(message): get_data(message=message, doc_type='document', file_id=message.document.file_id)


@bot.message_handler(content_types=['video'])
def doc_handler(message): get_data(message=message, doc_type='video', file_id=message.video.file_id)


@bot.message_handler(content_types=['audio'])
def doc_handler(message): get_data(message=message, doc_type='audio', file_id=message.audio.file_id)


@bot.message_handler(content_types=['photo'])
def doc_handler(message): get_data(message=message, doc_type='photo', file_id=message.photo[-1].file_id)


@bot.message_handler(content_types=['video_note'])
def doc_handler(message): get_data(message=message, doc_type='video_note', file_id=message.video_note.file_id)


@bot.message_handler(content_types=['voice'])
def doc_handler(message): get_data(message=message, doc_type='voice', file_id=message.voice.file_id)

def get_data(message, doc_type, file_id):
    chat_id = message.chat.id
    file_data['chat_id'] = chat_id
    file_data['file_id'] = file_id
    # file_data['file_name'] = message.document.file_name
    file_data['file_type'] = doc_type
    print(file_data)


@bot.message_handler(content_types=['text'])
def send_file(message):
    if file_data:
        bot.send_document(chat_id=file_data['chat_id'], document=file_data['file_id'])
    else:
        pass


bot.polling(none_stop=True, interval=0)
