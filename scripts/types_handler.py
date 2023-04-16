TYPES = {'document': 'document', 'video': 'video',
         'audio': 'audio', 'photo': 'photo',
         'video_note': 'video_note', 'voice': 'voice'}


def get_type(bot):
    @bot.message_handler(content_types=['document'])
    def doc_handler(message):
        get_data(message=message, doc_type=TYPES['document'])


    @bot.message_handler(content_types=['video'])
    def doc_handler(message):
        get_data(message=message, doc_type=TYPES['video'])


    @bot.message_handler(content_types=['audio'])
    def doc_handler(message):
        get_data(message=message, doc_type=TYPES['audio'])


    @bot.message_handler(content_types=['photo'])
    def doc_handler(message):
        get_data(message=message, doc_type=TYPES['photo'])


    @bot.message_handler(content_types=['video_note'])
    def doc_handler(message):
        get_data(message=message, doc_type=TYPES['video_note'])


    @bot.message_handler(content_types=['voice'])
    def doc_handler(message):
        get_data(message=message, doc_type=TYPES['voice'])



