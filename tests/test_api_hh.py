from unittest.mock import patch, MagicMock
from src.hh.api_hh import HeadHunterApi


def test_get_vacancies():
    """ Тест запроса API """
    api = HeadHunterApi()

    test_response = MagicMock()
    test_response.status_code = 200
    test_response.json.return_value = {"items": [{"id": 1}, {"id": 2}]}

    with patch('requests.get', return_value=test_response):
        result = api.get_vacancies()

    assert result == [{"id": 1}, {"id": 2}]


