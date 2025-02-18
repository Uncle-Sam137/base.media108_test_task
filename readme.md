# Определение новых достижений пользователей

Этот проект содержит Python-скрипт, который анализирует данные о достижениях пользователей, полученные из API.  
Функция делает два запроса и определяет **новые достижения**, которые появились во втором запросе, но отсутствовали в первом.

---

##  Описание работы скрипта

Функция `bm_test_zadanie()` выполняет следующие действия:

1. Отправляет **два GET-запроса** к API:  
   - **Первый запрос** получает начальные данные пользователей и их достижения.  
   - **Второй запрос** получает обновленные данные.  


2. Если API вернёт ошибку (500 Internal Server Error, 404 Not Found) или ответ будет в неверном формате (не JSON),
функция корректно обработает ошибку и вернёт строку с описанием проблемы, а не сломается.


3. Сравнивает достижения пользователей в двух запросах.  


4. Формирует новый словарь, который содержит:  
   - **Метаданные пользователя** (без изменений).  
   - **Список только новых достижений**, которых не было в первом запросе.  


5. Возвращает итоговый словарь в том же формате, что и API.

---

##  Установка и запуск

### Установка зависимостей
Для работы скрипта требуется Python 3 и модуль `requests`.  
Установите его, если он не установлен:


    pip install requests

### Запуск скрипта
Просто запустите файл main.py:

    python main.py
Скрипт выполнит два запроса и вернет словарь с новыми достижениями.

---
## Тестирование
Для проверки корректности работы используется pytest.

Установка pytest (если не установлен)

    pip install pytest
### Запуск тестов

    pytest test_bm_test_zadanie.py
При успешном прохождении тестов появится вывод:


    =================== test session starts ===================
    collected 3 items
    test_bm_test_zadanie.py ....  [100%]
    =================== 3 passed in 0.25s =====================
---
## Пример работы

### Ответ первого запроса:


    {
      "user_1": {
        "metadata": {"name": "Alice"},
        "achievements": {"sport": true, "reading": true}
      }
    }
### Ответ второго запроса:

    {
      "user_1": {
        "metadata": {"name": "Alice"},
        "achievements": {"sport": true, "reading": true, "travel": true}
      }
    }
### Выходные данные

    {
      "user_1": {
        "metadata": {"name": "Alice"},
        "achievements": {"travel": true}
      }
    }
"travel" добавилось, так как его не было в первом запросе.

---

## Инструкция по использованию пакета

### Скачайте и установите пакет

Скачайте и поместите пакет в папку с вашим проектом

Установите его с помощью команды pip. Убедитесь, что у вас установлен Python и pip. Введите в командной строке:

    pip install my_package-0.1.tar.gz

### Как использовать функции из пакета

После установки или добавления пакета в проект, вы можете импортировать функции, классы и модули из пакета в ваш код.

Импорт функции из модуля:

Если в пакете есть модуль main.py с функцией bm_test_zadanie, используйте следующий код:

    from my_package.main import bm_test_zadanie

### Вызов функции
    bm_test_zadanie()

### Как узнать, какие функции доступны в пакете

Если вы не знаете, какие функции или классы доступны в пакете, можно использовать dir() для получения списка доступных объектов. Пример:

    import my_package
    print(dir(my_package))  # Покажет список всех доступных объектов в пакете

---
Разработано для тестового задания.
Если у вас есть вопросы или предложения, свяжитесь со мной!
