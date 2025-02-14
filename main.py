import requests


def bm_test_zadanie():
    """
    Функция дважды запрашивает API и возвращает пользователей с новыми достижениями,
    которые появились во втором запросе, но отсутствовали в первом.
    """
    # Делаем два запроса к API
    first_response = requests.get("https://base.media108.ru/training/sample/").json()
    second_response = requests.get("https://base.media108.ru/training/sample/").json()

    res = dict()

    # Проходим по всем пользователям из второго запроса
    for user_id, user_data in second_response.items():
        # Создаем словарь для хранения новых данных пользователя
        x = dict()
        x['metadata'] = user_data['metadata']
        # Добавляем только новые достижения
        x['achievements'] = {el:True for el in user_data['achievements'] if el not in first_response[user_id]['achievements']}
        res[user_id] = x

    return res


def main():
    bm_test_zadanie()


if __name__ == '__main__':
    main()