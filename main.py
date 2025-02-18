import json

import requests


def bm_test_zadanie():
    """
    Функция дважды запрашивает API и возвращает пользователей с новыми достижениями,
    которые появились во втором запросе, но отсутствовали в первом.
    """
    # Делаем два запроса к API
    first_response = requests.get("https://base.media108.ru/training/sample/", timeout=5)
    second_response = requests.get("https://base.media108.ru/training/sample/", timeout=5)

    # Проверяем, что сервер вернул 200 для обоих запросов
    if first_response.status_code != 200 or second_response.status_code != 200:
        return (f'Ошибка API: '
                f'\nКод первого запроса: {first_response.status_code}'
                f'\nКод второго запроса: {second_response.status_code}')

    # Пробуем преобразовать ответы в JSON, обрабатываем возможную ошибку
    try:
        first_response = first_response.json()
        second_response = second_response.json()
    except json.decoder.JSONDecodeError:
        return f"Ошибка API: формат ответа не JSON"

    # Проверяем, что API вернул именно словари, а не список, число или строку
    if not isinstance(first_response, dict) or not isinstance(second_response, dict):
        return f"Ошибка API: формат ответа не словарь JSON"

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