from scripts.db_session import global_init
from telebot import TeleBot
from scripts import config, db_handler, file_handler, keyboards, features, tag_handler

bot = TeleBot(config.TOKEN)
global_init()


@bot.message_handler(commands=['start'])
def start(message):
    db_handler.new_user(user_id=message.from_user.id)
    bot.send_message(message.chat.id, text=f"Привет {message.from_user.first_name}!\n"
                                           f"Я твое карманное облако\n"
                                           f"Для начала работы со мной, нужно создать тег, для этого отправь "
                                           f"название тега в чат. После этого можешь начинать скидывать файлы, и они "
                                           f"будут храниться в этом теге. Также, создать тег можно добавив комментарий "
                                           f"к отправляемому документу. ",
                     reply_markup=keyboards.default_keyboard)
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
def doc_handler(message): file_handler.get_data(message=message, doc_type='photo', file_id=message.photo[-1].file_id)


@bot.message_handler(content_types=['video_note'])
def doc_handler(message): file_handler.get_data(message=message, doc_type='video_note',
                                                file_id=message.video_note.file_id)


@bot.message_handler(content_types=['voice'])
def doc_handler(message): file_handler.get_data(message=message, doc_type='voice', file_id=message.voice.file_id)


@bot.message_handler(content_types=['text'])
def send_file(message):
    current_tag = db_handler.get_current_tag(db_handler.get_db_user_id(message.from_user.id))
    if not features.TAG and message.text != "Мои теги" and message.text != "Удалить текущий тег":
        features.add_tag_from_message(message)
    elif message.text == "Мои теги":
        bot.send_message(message.chat.id,
                         text=f"Вы находитесь в теге '{current_tag}'"
                              f'\nВаши теги:', reply_markup=keyboards.get_tags(message.from_user.id))
    elif message.text == "Удалить текущий тег":
        bot.send_message(message.chat.id, text=f"Тег {current_tag} будет удален,"
                                               f" а также будут удалены файлы с этим тегом. \nХотите продолжить?",
                         reply_markup=keyboards.yes_no(current_tag))
    else:
        tag_handler.search_tag_from_message(message=message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('open:'))
def call_back(call):
    current_tag = db_handler.get_current_tag(db_handler.get_db_user_id(call.message.chat.id))
    bot.send_message(call.message.chat.id,
                     text=f"Файлы с тегом '{current_tag}':",
                     reply_markup=keyboards.get_files(call))
    bot.send_message(call.message.chat.id, text=f"Вы находитесь в теге '{current_tag}'",
                     reply_markup=keyboards.rm_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('send:'))
def call_back(call):
    file_handler.send_data(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('delete:'))
def call_back(call):
    tag_handler.remove_tag(call)


bot.polling(none_stop=True, interval=0)
