import re

import requests
from bs4 import BeautifulSoup

# Задача №1.

test_task = ["111111111110000000000000000", "1000", "1101011000"]


def task(array):
    return array.find('0')


# Задача №2.

def count_animals_by_alphabet():
    url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    page = requests.get(url).text
    stats = {}
    ru_names = True
    while ru_names:
        bs = BeautifulSoup(page, 'lxml')
        animals = bs.find('div', class_='mw-category mw-category-columns').find_all('a')
        for animal in animals:
            name = animal.text

            # Фильтрация иностранных слов
            if re.match('[a-zA-Z]', name[0]):
                if name[0] == 'A':
                    ru_names = False
                break

            if name[0] in stats:
                stats[name[0]] += 1
            else:
                stats[name[0]] = 1
        links = bs.find('div', id='mw-pages').find_all('a')
        for a in links:
            if a.text == 'Следующая страница':
                url = 'https://ru.wikipedia.org/' + a.get('href')
                page = requests.get(url).text
    return dict(sorted(stats.items()))


def appearance(intervals):
    time_cross = 0
    i, j, k = 0, 0, 0
    while i < len(intervals['lesson']) and \
            j < len(intervals['pupil']) and \
            k < len(intervals['tutor']):
        a1, a2 = intervals['lesson'][i], intervals['lesson'][i + 1]
        b1, b2 = intervals['pupil'][j], intervals['pupil'][j + 1]
        c1, c2 = intervals['tutor'][k], intervals['tutor'][k + 1]

        if a1 <= b2 and a1 <= c2 and \
                a2 >= b1 and a2 >= c1 and \
                b1 <= c2 and b2 >= c1:
            time_cross += min(a2, b2, c2) - max(a1, b1, c1)

        if c2 == min(a2, b2, c2):
            k += 2
        elif b2 == min(a2, b2, c2):
            j += 2
        else:
            i += 2
    return time_cross


tests = [
    {'data': {'lesson': [1594663200, 1594666800],
              'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
              'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },

    {'data': {'lesson': [1594702800, 1594706400],
              'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150,
                        1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480,
                        1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503,
                        1594706524, 1594706524, 1594706579, 1594706641],
              'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },

    {'data': {'lesson': [1594692000, 1594695600],
              'pupil': [1594692033, 1594696347],
              'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    print('Задание 1')
    for test in test_task:
        print(task(test))

    print('Задание 2')
    stats = count_animals_by_alphabet()
    for letter_stat in stats:
        if letter_stat == 'Ё':
            continue
        elif letter_stat == 'Е':
            print(f'{letter_stat}: {stats[letter_stat]}')
            print(f"{letter_stat}: {stats['Ё']}")
        else:
            print(f'{letter_stat}: {stats[letter_stat]}')

    print('Задание 3')
    for i, test in enumerate(tests):
        test_answer = appearance(test['data'])
        assert test_answer == test['answer'],\
            f'Error on test case {i},' \
            f' got {test_answer}, expected {test["answer"]}'
