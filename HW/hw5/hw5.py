import sqlite3
from flask import Flask, render_template, request
import os
import re


def database():  # создание базы данных
    for dir in os.listdir('project\gazeta\plain'):  # перебор папок с текстами газетного корпуса
        dirpath = r'project\gazeta\plain\%s\10' % dir
        for file in os.listdir(dirpath):
            filepath = os.path.join(dirpath, file)
            with open(filepath, encoding="utf-8") as f:  # открывается текст газеты для обработки
                text = f.read()
            metalist = re.findall(r'@.*?\n', text)
            for x in metalist:
                text = text.replace(x, '')  # текст очищается от ненужных тегов и метаданных
            text = text.replace(r'<.*?>', '')  # вытаскиваются данные для базы
            header = metalist[1].replace('@', '')
            header = header.replace('\n', '')
            date = metalist[2].replace('@', '')
            date = date.replace('\n', '')
            url = metalist[4].replace('@', '')
            url = url.replace('\n', '')
            text = text.replace('\n', '')
            mystemdirpath = dirpath.replace('plain', 'mystem-plain')  # лемматизированный текст очищается от ненужных тегов и метаданных
            mystemfilepath = os.path.join(mystemdirpath, file)
            with open(mystemfilepath, encoding="utf-8") as p:
                mystemtext = p.read()
            list_to_delete = re.findall(r'@.*?\n', mystemtext)
            for x in list_to_delete:
                mystemtext = mystemtext.replace(x, '')
            mystemtext = mystemtext.replace(r'<.*?>', '')
            mystemtext = mystemtext.replace('\n', '')
            c.execute('INSERT INTO newspapers VALUES (?, ?, ?, ?, ?)',  # создание одной строчки файла в базе данных
                      (url, header, date, text, mystemtext))
            conn.commit()


app = Flask(__name__)


@app.route('/')
def mainpage():
    return render_template('searchpage.html')  # страница поиска


@app.route('/results', methods=['POST'])
def resultpage():
    results = []
    dict_data = request.form  # запрос, который был получены из формы, преображен в удобный формат
    criteria = dict_data["searchrequest"]
    condition = ('%'+criteria+'%',)
    conn = sqlite3.connect('newspapers.db')
    c = conn.cursor()  # поиск по нелемматизированным текстам
    c.execute('SELECT * FROM newspapers WHERE Plain_text LIKE ?',
              condition)
    for x in c.fetchall():  # запись найденных данных в список
        text_result = []
        text_result.append(x[0])
        text_result.append(x[1])
        for index in range(0, len(x[3])-251, 250):  # нахождение кусочка файлов из 250-ти символов с искомым словом
            if criteria in x[3][index:index+250]:
                part = '...' + x[3][index:index+250] + '...'
                text_result.append(part)
        results.append(text_result)
    conn.close()
    with open('input.txt', 'w', encoding="utf-8") as f:  # сам запрос записывается в файл и лемматизируется
        f.write(criteria)
    os.system('mystem.exe -c -d -l ' + 'input.txt ' + 'output.txt')
    with open('output.txt', encoding="utf-8") as q:
        lemma = q.read()
    lemma = lemma.replace('\n', '')
    lemma_condition = ('%'+lemma+'%',)
    conn = sqlite3.connect('newspapers.db')  # поиск данных по лемматизированным текстам и по лемме
    c = conn.cursor()
    c.execute('SELECT * FROM newspapers WHERE Mystem_plain_text LIKE ?',
              lemma_condition)
    for x in c.fetchall():
        text_result = []  # запись найденных данных в список
        text_result.append(x[0])
        text_result.append(x[1])
        for index in range(0, len(x[4])-251, 250):
            if lemma in x[4][index:index+250]:
                part = '...' + x[3][index:index+250] + '...'
                text_result.append(part)
        results.append(text_result)
    conn.close()
    return render_template('Resultpage.html',
                           criteria=criteria, results=results)


conn = sqlite3.connect('newspapers.db')
c = conn.cursor()
c.execute("CREATE TABLE newspapers( Url text,"
          " Header text, Date_of_creation date, "
          "Plain_text text, Mystem_plain_text text)")
database()
conn.close()
if __name__ == '__main__':
    app.run()
