from scripts.db_session import global_init
from telebot import TeleBot
from scripts import config, db_handler, file_handler, keyboards, features


bot = TeleBot(config.TOKEN)
global_init()


@bot.message_handler(commands=['start'])
def start(message):
    db_handler.new_user(user_id=message.from_user.id)
    # db_handler.new_tag(user_id=message.from_user.id, tag_name="Test")
    bot.send_message(message.chat.id, text="привет лох 8===D", reply_markup=keyboards.default_keyboard)
    print(message.from_user.id)  # TODO DEBUG


@bot.message_handler(content_types=['document'])
def doc_handler(message): file_handler.get_data(message=message, doc_type='document', file_id=message.document.file_id,
                                                file_name=message.document.file_name)


@bot.message_handler(content_types=['video'])
def doc_handler(message): file_handler.get_data(message=message, doc_type='video', file_id=message.video.file_id,
                                                file_name=message.video.file_name)


@bot.message_handler(content_types=['audio'])
def doc_handler(message): file_handler.get_data(message=message, doc_type='audio', file_id=message.audio.file_id,
                                                file_name=message.audio.file_name)


@bot.message_handler(content_types=['photo'])
def doc_handler(message): bot.send_message(message.chat.id,
                                           text="Фото необходимо отправлять без сжатия")  # file_handler.get_data(message=message, doc_type='photo', file_id=message.photo[-1].file_id)


@bot.message_handler(content_types=['video_note'])
def doc_handler(message): file_handler.get_data(message=message, doc_type='video_note',
                                                file_id=message.video_note.file_id)


@bot.message_handler(content_types=['voice'])
def doc_handler(message): file_handler.get_data(message=message, doc_type='voice', file_id=message.voice.file_id)


@bot.message_handler(content_types=['text', 'document'])
def send_file(message):
    if not features.TAG:
        features.add_tag_from_message(message)
    elif message.text == "Мои теги":
        bot.send_message(message.chat.id, text='Ваши теги:', reply_markup=keyboards.get_tags(message.from_user.id))
    else:
        bot.send_message(message.chat.id, text='no', reply_markup=None)


@bot.callback_query_handler(func=lambda call: call.data.startswith('open:'))
def call_back(call):
    bot.send_message(call.message.chat.id, text='Файлы с таким тегом', reply_markup=keyboards.get_files(call))


@bot.callback_query_handler(func=lambda call: call.data.startswith('send:'))
def call_back(call):
    file_handler.send_data(call)


bot.polling(none_stop=True, interval=0)
