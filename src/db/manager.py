import os
import psycopg2


class DBManager:
    """ Загружаем параметры подключения из переменных окружения """
    def __init__(self):
        self.db_name = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = os.getenv("DB_PORT", "5432")

        self.conn = None
        self.cursor = None

        self.connect()

    def connect(self):
        """ Подключение к БД """
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.conn.cursor()
            print("Подключение успешно")

        except psycopg2.Error as e:
            print("Ошибка подключения:", e)

    def close(self):
        """ Закрытие подключения к БД """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Соединение закрыто")


    def create_tables_if_not_exists(self):
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS employers
                            (
                                employer_id TEXT PRIMARY KEY,
                                name        TEXT,
                                trusted     BOOLEAN
                            );


                            DROP TABLE IF EXISTS vacancies;

                            CREATE TABLE IF NOT EXISTS vacancies
                            (
                                id           serial PRIMARY KEY,
                                hh_id        bigint UNIQUE,
                                employer_id  text REFERENCES employers (employer_id),
                                name         text,
                                description  text,
                                salary_min   numeric,
                                salary_max   numeric,
                                currency     text,
                                employment   text,
                                experience   text,
                                published_at timestamp
                            );""")
