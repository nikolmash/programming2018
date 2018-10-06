import json
import urllib.request


def main(list_of_users):  # Выполнение всех внутренних функций
    user = input('Введите имя пользователя: ')
    while user not in list_of_users:
        user = input('Данного пользователя нет в списке. Попробуйте ввести'
                     ' другое имя: ')
    print('\nВы выбрали пользователя {}'.format(user))
    user_page = request(user)
    repos_and_description(user_page)
    languages(user_page, user)
    repos_number(users)
    followers_number(users)
    popular_lang(users)


def request(user):  # Посылка запроса на сервер, изменение json в строку python
    page = 1
    full_text = ''
    while page < 100:
        url = 'https://api.github.com/users/{}/repos?page={}'.format(user, page)
        response = urllib.request.urlopen(url)
        text = response.read().decode('utf-8')
        full_text += text
        page += 1
    full_data = json.loads(full_text)
    return full_data


def repos_and_description(page):  # Пункт 1: считывание и вывод информации о репозиториях и их описаниях
    repos_dict = {}
    for i in page:
        repos_dict[i["name"]] = i["description"]
    print('\nНиже представлены репозитории пользователя: ')
    for key, value in repos_dict.items():
        print(key, ': ', value)


def languages(page, user):  # Пункт 2: информация об использованных пользователем языках
    lang_dict = {}
    for i in page:
        if i["language"] is not None:
            if i["language"] in lang_dict:
                print('')
                lang_dict[i["language"]].append(i["name"])
            else:
                lang_dict[i["language"]] = list()
                lang_dict[i["language"]].append(i["name"])
    for lang in lang_dict:
        lang_dict[lang] = ', '.join(lang_dict[lang])
    print('\nПользователь {} использует языки '.format(user), end='')
    print(', '.join(['{}'.format(i) for i in lang_dict]))
    print(', '.join(['язык {} используется в репозиториях: '
                     '{}'.format(key, value) for key, value in lang_dict.items()]).capitalize())


def repos_number(list_of_users):  # Пункт 3: выявление лидера по количеству репозиториев
    repos_dict = {}
    for user in list_of_users:
        data = request(user)
        repos_dict[user] = len(data)
    max_repos = 0
    winner = ''
    for user in repos_dict:
        if repos_dict[user] > max_repos:
            max_repos = repos_dict[user]
        winner = user
    list_of_users = ', '.join(list_of_users)
    print('Из списка {} больше всего подписчиков у пользователя'
          ' {}'.format(list_of_users, winner))


def popular_lang(list_of_users):  # Пункт 4: определение самого популяного среди пользователей языка
    freq_lang = {}
    for user in list_of_users:
        data = request(user)
        for i in data:
            if i["language"] is not None:
                if i["language"] in freq_lang:
                    freq_lang[i["language"]] += 1
                else:
                    freq_lang[i["language"]] = 1
    max_freq = 0
    winner = ''
    for language in freq_lang:
        if freq_lang[language] > max_freq:
            max_freq = freq_lang[language]
    print('{} - самый популярный язык среди пользователей'.format(winner))


def followers_number(list_of_users):  # Пункт 5: выявление лидера по количеству подписчиков
        follow_dict = {}
        for user in list_of_users:
            data = request(user)
            follow_dict[user] = len(data)
        max_followers = 0
        winner = ''
        for user in follow_dict:
            if follow_dict[user] > max_followers:
                max_followers = follow_dict[user]
            winner = user
        print('Больше всего подписчиков у пользователя с ником '
              '{}'.format(winner))


users = [i for i in input('Введите имена пользователей Github через '
                          'пробел: ').split()]
main(users)
