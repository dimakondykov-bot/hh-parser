from dotenv import load_dotenv

from src.db.manager import DBManager
from src.hh.api_hh import HeadHunterApi
from src.db.repository import Repository


def main():
    """ Фуекция позволяет получать вакансии с сайта HeadHunter, сохраняет их в базу данных и выполняет запросы к БД"""
    load_dotenv()  # Загружаем переменные оркружения

    manager = DBManager()
    manager.create_tables_if_not_exists()

    # Получение вакансий с HeadHunter. Создаём объект HeadHunterApi и делаем запрос get_vacancies()
    hh = HeadHunterApi()
    vacancies = hh.get_vacancies()

    # Сохраняем вакансии в БД
    repository = Repository(manager)
    repository.insert(vacancies)

    print(repository.get_avg_salary())
    print(repository.get_all_vacancies())
    print(repository.get_vacancies_with_keyword('водитель'))
    print(repository.get_vacancies_with_higher_salary())
    print(repository.get_companies_and_vacancies_count())


if __name__ == "__main__":
    main()
