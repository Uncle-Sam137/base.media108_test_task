import json

import pytest
from unittest.mock import patch
from main import bm_test_zadanie


# Тестовые данные
first_response_mock = {
    "user_1": {
        "metadata": {"name": "Alice"},
        "achievements": {"sport": True, "reading": True}
    },
    "user_2": {
        "metadata": {"name": "Bob"},
        "achievements": {"cooking": True}
    }
}

second_response_mock = {
    "user_1": {
        "metadata": {"name": "Alice"},
        "achievements": {"sport": True, "reading": True, "travel": True}  # Новое достижение "travel"
    },
    "user_2": {
        "metadata": {"name": "Bob"},
        "achievements": {"cooking": True}
    }
}


# Фикстура для замены запросов к API
@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock_get:
        yield mock_get


# Тест 1: Проверяем, что новые достижения правильно определяются
def test_new_achievements(mock_requests_get):
    mock_requests_get.side_effect = [MockResponse(first_response_mock), MockResponse(second_response_mock)]

    result = bm_test_zadanie()

    assert result["user_1"]["achievements"] == {"travel": True}  # "travel" - новое достижение
    assert result["user_2"]["achievements"] == {}  # У Bob новых достижений нет


# Тест 2: Если список достижений не изменился, achievements должен быть пустым
def test_no_new_achievements(mock_requests_get):
    mock_requests_get.side_effect = [MockResponse(first_response_mock), MockResponse(first_response_mock)]

    result = bm_test_zadanie()

    assert result["user_1"]["achievements"] == {}  # Нет новых достижений
    assert result["user_2"]["achievements"] == {}  # Нет новых достижений


# Тест 3: Если во втором запросе список достижений пуст
second_response_empty_achievements = {
    "user_1": {
        "metadata": {"name": "Alice"},
        "achievements": {}
    },
    "user_2": {
        "metadata": {"name": "Bob"},
        "achievements": {}
    }
}


def test_empty_achievements(mock_requests_get):
    mock_requests_get.side_effect = [MockResponse(first_response_mock), MockResponse(second_response_empty_achievements)]

    result = bm_test_zadanie()

    assert result["user_1"]["achievements"] == {}  # Достижения исчезли, но новых нет
    assert result["user_2"]["achievements"] == {}  # Достижения исчезли, но новых нет


#Тест на неожиданный формат данных
def test_unexpected_json_format(mock_requests_get):
    mock_requests_get.side_effect = [MockResponse([]), MockResponse("Invalid response")]

    result = bm_test_zadanie()

    assert isinstance(result, str)
    assert "Ошибка API: формат ответа не словарь JSON" in result


#Тест на обработку ошибок API если сервер вернёт не 200
def test_api_error(mock_requests_get):
    mock_requests_get.side_effect = [MockErrorResponse(500), MockErrorResponse(500)]  # Симуляция ошибки сервера

    result = bm_test_zadanie()

    assert isinstance(result, str)  # Функция должна вернуть строку с ошибкой
    assert "Ошибка API" in result  # Проверяем, что в ответе есть сообщение об ошибке


#Тест на некорректный JSON
def test_invalid_json_response(mock_requests_get):
    with patch("requests.get") as mock_get:
        mock_get.return_value = MockInvalidJSONResponse()  # Симуляция некорректного JSON

        result = bm_test_zadanie()

        assert isinstance(result, str)
        assert "Ошибка API: формат ответа не JSON" in result


# Класс-обертка для мок-ответов API
class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code  # Добавляем статус код

    def json(self):
        return self.json_data


#Класс для эмуляции ошибки API
class MockErrorResponse:
    def __init__(self, status_code):
        self.status_code = status_code

    def json(self):
        return None  # API ничего не вернёт


#Класс, который сломает json()
class MockInvalidJSONResponse:
    status_code = 200  # API вернул 200, но JSON сломан

    def json(self):
        raise json.decoder.JSONDecodeError("Expecting value", "doc", 0)  # Симуляция ошибки JSON
