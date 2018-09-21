import random
import re

def file_reader(): #выбор темы, чтение файла и выбор слова для угадывания
    filename = int(input('Выберите тему:\n1 - мультфильмы\n2 - профессии\n3 - мировые валюты\n'))
    if filename == '':
        print('Введена пустая строка')
    else:
        if filename == 1:
            filename = 'мультфильмы.txt'
        elif filename == 2:
            filename = 'профессии.txt'
        elif filename == 3:
            filename = 'мировые валюты.txt'
        with open(filename, encoding='utf-8') as f:
            words = f.read()
            words = words.split()
        word = random.choice(words)
        return word

def word_guess(word): #определение количества букв в загаданном слове, ввод буквы пользователем - непосредственно, процесс отгадывания
    t = 24
    number_of_letters = len(word)
    print('У вас есть ',t, ' попытки, чтобы угадать слово из ',number_of_letters,' букв.')
    future_word = number_of_letters*'_ '
    print(future_word)
    used_letters = []
    while t>0 and '_' in future_word:
        l = input('Введите букву: ')
        if l == '':
            print('Введена пустая строка')
        elif re.fullmatch('[а-я]',l) is None:
            print('То, что вы ввели - не буква')
        elif l in used_letters:
            print('Вы уже вводили эту букву') 
        elif l in word:
            indexes = find_letters_in_word(word,l)
            future_word = list(future_word)
            for x in indexes:
                future_word[2*x] = l
            future_word = ''.join(future_word)   
            print('Такая буква в слове есть\n',future_word) 
        else:
            t -= 1
            print('Такой буквы в слове нет\nОставшиеся попытки: ',t)
            draw_picture(t)
        used_letters.append(l)
    if t>0:
        print('Поздравляем! Вы угадали слово!')
        



def find_letters_in_word(word, letter): #нахождение всех вхождений буквы в слово
    indexes = []
    x = 0
    while x < len(word):
        x = word.find(letter, x)
        if x == -1:
            return indexes
        else:
            indexes.append(x)
            x += 1
    return indexes
        
        
def draw_picture(number): #рисование частей виселицы и человечка
    if number == 23:
        print('\n\n\n\n |     ')
    elif number == 22:
        print('\n\n\n\n\n/|     ')
    elif number == 21:
        print('\n\n\n\n\n/|\    ')
    elif number == 20:
        print('\n\n\n\n\n/|\  | ')
    elif number == 19:
        print('\n\n\n\n\n/|\  |\\')
    elif number == 18:
         print('\n\n\n\n\n/|\ /|\\')
    elif number == 17:
        print('\n\n\n\n |\n/|\ /|\\')
    elif number == 16:
        print('\n\n\n\n |   |\n/|\ /|\\')
    elif number == 15:
        print('\n\n\n |\n |   |\n/|\ /|\\')
    elif number == 14:
        print('\n\n\n |   |\n |   |\n/|\ /|\\')
    elif number == 13:
        print('\n\n |\n |   |\n |   |\n/|\ /|\\')
    elif number == 12:
        print('\n\n |   |\n |   |\n |   |\n/|\ /|\\')
    elif number == 11:
        print('\n |\n |   |\n |   |\n |   |\n/|\ /|\\')
    elif number == 10:
        print('\n |   |\n |   |\n |   |\n |   |\n/|\ /|\\')
    elif number == 9:
        print('  _\n |   |\n |   |\n |   |\n |   |\n/|\ /|\\')
    elif number == 8:
        print('  __\n |   |\n |   |\n |   |\n |   |\n/|\ /|\\')
    elif number == 7:
        print('  ___\n |   |\n |   |\n |   |\n |   |\n/|\ /|\\')
    elif number == 6:
        print('  ___\n | | |\n |   |\n |   |\n |   |\n/|\ /|\\')
    elif number == 5:
        print('  ___\n | | |\n | о |\n |   |\n |   |\n/|\ /|\\')
    elif number == 4:
        print('  ___\n | | |\n | о |\n | | |\n |   |\n/|\ /|\\')
    elif number == 3:
        print('  ___\n | | |\n |\о |\n | | |\n |   |\n/|\ /|\\')
    elif number == 2:
        print('  ___\n | | |\n |\о/|\n | | |\n |   |\n/|\ /|\\')
    elif number == 1:
        print('  ___\n | | |\n |\о/|\n | | |\n |/  |\n/|\ /|\\')
    elif number == 0:
        print('  ___\n | | |\n |\о/|\n | | |\n |/ \|\n/|\ /|\\')
        print('Вы проиграли')
    
    
  
w = file_reader()
word_guess(w) 
        
