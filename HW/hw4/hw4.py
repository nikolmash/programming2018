from flask import Flask, render_template, request, url_for
import json
import re

app = Flask(__name__)


@app.route('/')
def mainpage():
    return render_template('questionnaire.html')


@app.route('/json', methods=['POST'])
def jsondata():
    dict_data = request.form
    with open('data.csv', 'a', encoding='utf-8') as h:  # запись в файл полученных данных
        for i in dict_data:
            if dict_data[i] == '':
                h.write(' ')
            else:
                h.write(dict_data[i])
            h.write('\t')
        h.write('\n')
    json_data = json.dumps(dict_data, ensure_ascii=False)  # преобразование словаря в json
    global result
    result = fulldata(json_data)  # функция, которая накапливает json
    return '<html><head><style>body{background-color: #95129d;' \
           ' color: #ffffff;}</style></head><body>' + result + '</body></html>'


@app.route('/search')
def searchpage():  # страница поиска
    url = url_for('mainpage')  # ссылка на главную страницу
    return render_template('searchpage.html', url=url)


@app.route('/results', methods=['POST'])
def resultpage():
    req_dict = request.form  # получение параметров, по которым будет вестись поиск
    search_request = req_dict["searchrequest"]
    search_lang = req_dict["language"]
    json_strings = re.findall('{.*?}', result, flags=re.DOTALL)  # разбиение большой json строки на массив из маленьких
    results = ''
    for i in json_strings:
        if (search_request in i) and (search_lang in i):  # в каждой json строке совершаем поиск
            data = json.loads(i)
            for key, value in data.items():
                results = results + key + ' : ' + value + '<br>'  # красивая запись ключа-значения словаря
            results += '<br>'*2
    if results == '':
        return '<html><head><style>body{background-color: #95129d; ' \
               'color: #ffffff;}</style></head><body><h1 align="center">' \
               'Результаты поиска</h1><h2>К сожалению, ' \
               'поиск не дал результатов</h2></body></html>'
    else:
        return '<html><head><style>body{background-color: #95129d;' \
               ' color: #ffffff;}</style></head><body><h1 align="center">' \
               'Результаты поиска</h1><h2>' \
               'Вот.что удалось найти:</h2>' + results + '</body></html>'


@app.route('/stats')
def statistic_count():
    global json_strings
    json_strings = re.findall('{.*?}', result, flags=re.DOTALL)  # снова большую json строку делим на маленькие
    response_number = len(json_strings)  # ищем количество ответов на анкету
    dict_lang = {}  # пустые словари для будущих частотных словарей
    dict1 = {}
    dict2 = {}
    dict3 = {}
    dict4 = {}
    dict5 = {}
    dict6 = {}
    dict7 = {}
    dict8 = {}
    for x in json_strings:
        data = json.loads(x)
        if data["language"] in dict_lang:  # частотный словарь языков информантов
            dict_lang[data["language"]] += 1
        else:
            dict_lang[data["language"]] = 1
        if data["sky1"] in dict1:  # частотный словарь ответов на задание 1
            dict1[data["sky1"]] += 1
        else:
            dict1[data["sky1"]] = 1
        if data["sky2"] in dict2:  # частотный словарь ответов на задание 2
            dict2[data["sky2"]] += 1
        else:
            dict2[data["sky2"]] = 1
        if data["sea"] in dict3:  # частотный словарь ответов на задание 3
            dict3[data["sea"]] += 1
        else:
            dict3[data["sea"]] = 1
        if data["sand"] in dict4:  # частотный словарь ответов на задание 4
            dict4[data["sand"]] += 1
        else:
            dict4[data["sand"]] = 1
        if data["moon"] in dict5:  # частотный словарь ответов на задание 5
            dict5[data["moon"]] += 1
        else:
            dict5[data["moon"]] = 1
        if data["sunset"] in dict6:  # частотный словарь ответов на задание 6
            dict6[data["sunset"]] += 1
        else:
            dict6[data["sunset"]] = 1
        if data["canyon"] in dict7:  # частотный словарь ответов на задание 7
            dict7[data["canyon"]] += 1
        else:
            dict7[data["canyon"]] = 1
        if data["flower"] in dict8:  # частотный словарь ответов на задание 8
            dict8[data["flower"]] += 1
        else:
            dict8[data["flower"]] = 1
    url = url_for('mainpage')
    return render_template('statistic.html', num=response_number,
                           lang=dict_lang, task1=dict1, task2=dict2,
                           task3=dict3, task4=dict4, task5=dict5,
                           task6=dict6, task7=dict7, task8=dict8, url=url)


def fulldata(string):  # функция, которую мы использовали для накопления большой json строки
    global json_string
    json_string = json_string + string
    return json_string


if __name__ == '__main__':
    global json_string
    json_string = ''
    with open('data.csv', 'w', encoding='utf-8') as f:  # создание пустой таблицы с подписями к колонам
        for i in 'firstname lastname sex age language sky1' \
                 ' sky2 sea sand moon sunset canyon'.split():
            f.write(i)
            f.write('\t')
        f.write('\n')
    app.run()
