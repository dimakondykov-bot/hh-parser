from dotenv import load_dotenv

from src.hh.api import HeadHunterApi
from src.db.repository import Repository


def main():
    load_dotenv()

    hh = HeadHunterApi()
    vacancies = hh.get_vacancies()

    repository = Repository()
    repository.insert(vacancies)

    print(repository.get_avg_salary())
    print(repository.get_all_vacancies())
    print(repository.get_vacancies_with_keyword('водитель'))
    print(repository.get_vacancies_with_higher_salary())
    print(repository.get_companies_and_vacancies_count())


if __name__ == "__main__":
    main()