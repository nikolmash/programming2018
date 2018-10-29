import urllib.request
import re
import os


def main():
    with open('газета/metadata.csv', 'w', encoding='utf-8') as f:  # создается пустая csv таблица
        for x in ('path', 'author', 'header', 'created', 'sphere',
                  'topic', 'style', 'audience_age', 'audience_level',
                  'audience_size', 'source', 'publication', 'publ_year',
                  'medium', 'country', 'region', 'language'):
            f.write(x)
            f.write('\t')
        f.write('\n')
    common_url = 'http://www.vpgazeta.ru/article/'
    for i in range(90176, 90325):  # статьи в указанном диапазоне скачиваются и обрабатываются
        global page_url
        page_url = common_url + str(i)
        try:
            page = urllib.request.urlopen(page_url)
            article_html = page.read().decode('utf-8')
            list_with_meta = find_metadata(article_html)
            save_plain_text(article_html)
            fill_in_metadata(list_with_meta)
        except:
            print('Error at', page_url)
    for i in range(77300, 77500):  # статьи в указанном диапазоне скачиваются и обрабатываются
        page_url = common_url + str(i)
        try:
            req = urllib.request.Request(page_url)
            page = urllib.request.urlopen(req)
            article_html = page.read().decode('utf-8')
            list_with_meta = find_metadata(article_html)
            save_plain_text(article_html)
            fill_in_metadata(list_with_meta)
        except:
            print('Error at', page_url)


def find_metadata(html):  # осуществляется поиск метаданных по html тексту
    reg_author = re.search('АВТОР.*?<a.*?">(.*?)</a>', html, flags=re.DOTALL)
    if reg_author is not None:
        global author
        author = reg_author.group(1)
    else:
        author = '—'
    reg_header = re.search('bigger4 title">(.*?)</span>',
                           html, flags=re.DOTALL)
    global header
    header = reg_header.group(1)
    symbols_to_delete = ['?', ':']
    for x in symbols_to_delete:
        if x in str(header):
            header = header.replace(x, '')
    reg_created = re.search(r'smaller2 superhidden spaced">'
                            r'(\d\d/\d\d/\d\d\d\d)</span>', html,
                            flags=re.DOTALL)
    global created
    created = reg_created.group(1)
    reg_publ_year = re.search(r'\d\d\d\d', created)
    global publ_year
    publ_year = reg_publ_year.group()
    reg_publ_month = re.search('/(.*?)/', created)
    global publ_month
    publ_month = reg_publ_month.group(1)
    reg_topic = re.search('smaller2 superhidden spaced.*?'
                          'НОВОСТИ.*?">(.*?)</a>', html, flags=re.DOTALL)
    global topic
    topic = reg_topic.group(1)
    if len(topic.split()) > 2:
        topic = '—'
    list_with_meta = ['', author, header, created, topic, page_url, publ_year]
    return list_with_meta


def save_plain_text(html):  # сохраняется текст в режиме для чтения
    reg_text = re.search('ADV-ЗАМЕТКА -->(.*?)<div class="clear"',
                         html, flags=re.DOTALL)
    text = reg_text.group(1)  # вытаскивается непосредственно текст статьи
    text_with_paragraph = re.sub(r'<br />', '\n', text)  # в следующих двух строчках чистится от тэгов и символов
    almost_ready_text = re.sub('&?[a-z]', '', text_with_paragraph)
    ready_text = re.sub('<.*?/>', '', almost_ready_text, flags=re.DOTALL)
    directory = 'газета/' + 'plain/' + publ_year + '/' + publ_month  # собирается путь к будущему файлу
    if not os.path.exists(directory):
        os.makedirs(directory)  # создание папки
    name_of_the_file = header + '.txt'
    global path
    path = directory + '/' + name_of_the_file
    with open(path, 'w', encoding='utf-8') as f:   # запись статьи в виде для чтения в файл
        if author is not None:
            f.write('@' + author + '\n')
        else:
            f.write('@' + 'None' + '\n')
        f.write('@' + header + '\n')
        f.write('@' + created + '\n')
        f.write('@' + topic + '\n')
        f.write('@' + page_url + '\n')
        f.write(ready_text)


def fill_in_metadata(list):  # заполнение таблицы с метаданными
    list[0] = path  # дополнение к уже имеющимся сведениям
    tuple_with_meta = tuple(list)
    row = '%s\t%s\t%s\t%s\tпублицистика\t%s\tнейтральный\t' \
          'н-возраст\tн-уровень\tреспубликанская\t%s\t' \
          'Волжская правда\t%s\tгазета\tРоссия\tМарий Эл\tru'
    with open('газета/metadata.csv', 'a', encoding='utf-8') as f:  # запись в таблицу
        f.write(row % tuple_with_meta)
        f.write('\n')


main()
