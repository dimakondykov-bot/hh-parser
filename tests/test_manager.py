import pytest


from unittest.mock import MagicMock, patch
import os
from src.db.manager import DBManager


def test_dbmanager_connect_uses_env_vars():
    os.environ["DB_NAME"] = "test_db"
    os.environ["DB_USER"] = "test_user"
    os.environ["DB_PASSWORD"] = "test_pass"
    os.environ["DB_HOST"] = "test_host"
    os.environ["DB_PORT"] = "1234"

    test_conn = MagicMock()
    test_cursor = MagicMock()
    test_conn.cursor.return_value = test_cursor


    with patch("src.db.manager.psycopg2.connect", return_value=test_conn) as mock_connect:
        manager = DBManager()


    mock_connect.assert_called_once_with(
        dbname="test_db",
        user="test_user",
        password="test_pass",
        host="test_host",
        port="1234",
    )


    assert manager.conn == test_conn
    assert manager.cursor == test_cursor


def test_dbmanager_close_closes_cursor_and_connection():
    test_conn = MagicMock()
    test_cursor = MagicMock()
    test_conn.cursor.return_value = test_cursor

    with patch("src.db.manager.psycopg2.connect", return_value=test_conn):
        manager = DBManager()


    manager.close()


    test_cursor.close.assert_called_once()
    test_conn.close.assert_called_once()
