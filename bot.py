import gensim
import urllib.request
import time
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pymorphy2 import MorphAnalyzer


updater = Updater(token='761231703:AAHTs8MU1Z8GcFKaWRzPnh0i08q-l1ot9vc')
dispatcher = updater.dispatcher

urllib.request.urlretrieve("http://rusvectores.org/static/models/rusvectores2/ruscorpora_mystem_cbow_300_2_2015.bin.gz", "ruscorpora_mystem_cbow_300_2_2015.bin.gz")
m = 'ruscorpora_mystem_cbow_300_2_2015.bin.gz'

if m.endswith('.vec.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
elif m.endswith('.bin.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
else:
    model = gensim.models.KeyedVectors.load(m)
model.init_sims(replace=True)
model_path = "model_rus.bin"

model.wv.save_word2vec_format(model_path, binary=True)
def changing(sentence):
    morph = MorphAnalyzer()
    sentence = sentence.lower()
    new_sentence = ''
    error_mes = ''
    content_words_forms = {}
    function_pos = ['PREP', 'CONJ', 'PRCL', 'INTJ', 'NPRO']
    only_words = re.findall(r'[а-я]+', sentence)
    for word in only_words:
        ana = morph.parse(word)[0]
        if ana.tag.POS not in function_pos:
            if ana.tag.POS == 'NOUN':
                pword = ana.normal_form + '_S'
                tags = {ana.tag.case, ana.tag.number}
            if ana.tag.POS == 'ADJF' or ana.tag.POS == 'ADJS':
                pword = ana.normal_form + '_A'
                tags = {ana.tag.gender, ana.tag.number, ana.tag.case}
            if ana.tag.POS == 'VERB' or ana.tag.POS == 'INFN':
                pword = ana.normal_form + '_V'
                if ana.tag.tense == 'pres':
                    tags = {ana.tag.person, ana.tag.number, ana.tag.tense}
                if ana.tag.tense == 'past':
                    tags = {ana.tag.gender, ana.tag.number, ana.tag.tense}
                if ana.tag.tense == 'futr':
                    tags = {ana.tag.tense}
            if ana.tag.POS == 'NUMR':
                pword = ana.normal_form + '_NUM'
                tags = {ana.tag.person, ana.tag.number, ana.tag.case}
            if ana.tag.POS == 'ADVB':
                pword = ana.normal_form + '_ADV'
                tags = {ana.tag.POS}
            if pword in model:
                for item in model.wv.most_similar(pword, topn=20):
                    new_lem = item[0]
                    lemma_reg = re.search(r'([а-я]+)_', new_lem)
                    lemma = lemma_reg.group(1)
                    new_lem_parse = morph.parse(lemma)[0]
                    if new_lem_parse.inflect(tags) is None:
                        continue
                    else:
                        new_word = new_lem_parse.inflect(tags).word
                        break
            else:
                new_word = word
                error_mes = 'Слова ' + ana.normal_form + ' в модели нет'
        else:
            new_word = word
        new_sentence = new_sentence + new_word + ' '
    return new_sentence, error_mes

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, пришли мне любое предложение, и я покажу, как оно именится!')
    time.sleep(1)

def answer_text(bot, update):
    if re.findall(r'[a-zA-Z\d]+', update.message.text) != []:
        bot.send_message(chat_id=update.message.chat_id, text='Мне нужны только слова русского языка!')
    else:
        picture = open('cat.jpg', 'rb')
        bot.send_photo(chat_id=update.message.chat_id, photo=picture)
        if changing(update.message.text)[1] == '':
            reply = changing(update.message.text)[0]
        else:
            bot.send_message(chat_id=update.message.chat_id, text=changing(update.message.text)[1])
            reply = changing(update.message.text)[0]
        bot.send_message(chat_id=update.message.chat_id, text=reply)
    time.sleep(1)

def send_anger(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Что это такое? Я жду предложение')

# Хендлеры
start_command_handler = CommandHandler('start', start)
text_message_handler = MessageHandler(Filters.text, answer_text)
media_message_handler = MessageHandler(Filters.audio & Filters.video & Filters.document & Filters.photo & Filters.invoice & Filters.sticker, send_anger)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
dispatcher.add_handler(media_message_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()