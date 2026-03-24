import unittest
import pytest
from unittest.mock import MagicMock, patch

from src.db.manager import DBManager
from src.db.repository import Repository


def test_insert_vacancy():
    test_manager = MagicMock()
    test_cursor = MagicMock()

    # cursor() должен вернуть поддельный курсор
    test_manager.conn.cursor.return_value = test_cursor

    # создаём Repository с поддельным менеджером
    repository = Repository(test_manager)

    vacancies = [
        {
            "id": "123",
            "name": "Python Developer",
            "employer": {"id": "1", "name": "Company", "trusted": True},
            "snippet": {"responsibility": "Do work", "requirement": "Know Python"},
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "employment": {"name": "Full time"},
            "experience": {"name": "1-3 years"},
            "published_at": "2024-01-01"
        }
    ]

    repository.insert(vacancies)

    # insert вызывает executemany ДВА раза
    assert test_cursor.executemany.call_count == 2

    # commit должен быть вызван
    test_manager.conn.commit.assert_called_once()


def setup_repository_with_cursor(fake_data):
    test_manager = MagicMock()
    test_cursor = MagicMock()

    test_cursor.fetchall.return_value = fake_data
    test_manager.conn.cursor.return_value = test_cursor

    repository = Repository(test_manager)

    return repository, test_cursor


def test_get_all_vacancies():
    test_data = [
        ("Company", "PHP", 120000, 170000, "https://hh.ru/vacancy/")
    ]

    repository, cursor = setup_repository_with_cursor(test_data)

    result = repository.get_all_vacancies()

    cursor.execute.assert_called_once()
    assert result == test_data



def test_get_companies_and_vacancies_count():
    test_data = [
        ("Company A", 5),
        ("Company B", 2),
    ]

    repository, cursor = setup_repository_with_cursor(test_data)

    result = repository.get_companies_and_vacancies_count()

    cursor.execute.assert_called_once()
    assert result == test_data
