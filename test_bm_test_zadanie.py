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


# Класс-обертка для мок-ответов API
class MockResponse:
    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        return self.json_data
