from src.db.manager import DBManager


class Repository:
    def __init__(self):
        self.manager = DBManager()
        self.cur = self.manager.conn.cursor()

    def insert(self, vacancies):
        """Сохраняем работодателей и вакансии в базу."""

        employer_data = []
        vacancy_data = []

        for item in vacancies:
            # --- Работодатель ---
            employer = item.get("employer") or item.get("employeer") or {}
            employer_id = employer.get("id")

            if employer_id:
                employer_data.append((
                    employer_id,
                    employer.get("name"),
                    employer.get("trusted")
                ))

            # --- Описание ---
            snippet = item.get("snippet") or {}
            responsibility = snippet.get("responsibility") or ""
            requirement = snippet.get("requirement") or ""
            description = f"{responsibility} {requirement}".strip()

            # --- Зарплата ---
            salary = item.get("salary") or {}
            salary_min = salary.get("from")
            salary_max = salary.get("to")
            currency = salary.get("currency")

            # --- Вакансия ---
            vacancy_data.append((
                item.get("id"),
                employer_id,
                item.get("name"),
                description,
                salary_min,
                salary_max,
                currency,
                item.get("employment", {}).get("name"),
                item.get("experience", {}).get("name"),
                item.get("published_at")
            ))

        # Сохраняем работодателей
        if employer_data:
            self.cur.executemany(
                """
                INSERT INTO employers (employer_id, name, trusted)
                VALUES (%s, %s, %s)
                ON CONFLICT (employer_id) DO NOTHING;
                """,
                employer_data
            )

        # Сохраняем вакансии
        if vacancy_data:
            self.cur.executemany(
                """
                INSERT INTO vacancies (
                    hh_id, employer_id, name, description,
                    salary_min, salary_max, currency,
                    employment, experience, published_at
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (hh_id) DO NOTHING;
                """,
                vacancy_data
            )

        self.manager.conn.commit()

    # --- Методы из ТЗ ---

    def get_companies_and_vacancies_count(self):
        self.cur.execute(
            """
            SELECT e.name, COUNT(v.id)
            FROM employers e
            LEFT JOIN vacancies v ON v.employer_id = e.employer_id
            GROUP BY e.name
            ORDER BY COUNT(v.id) DESC;
            """
        )
        return self.cur.fetchall()

    def get_all_vacancies(self):
        self.cur.execute(
            """
            SELECT e.name,
                   v.name,
                   v.salary_min,
                   v.salary_max,
                   'https://hh.ru/vacancy/' || v.hh_id
            FROM vacancies v
            LEFT JOIN employers e ON v.employer_id = e.employer_id;
            """
        )
        return self.cur.fetchall()

    def get_avg_salary(self):
        self.cur.execute(
            """
            SELECT AVG((salary_min + salary_max) / 2.0)
            FROM vacancies
            WHERE salary_min IS NOT NULL
              AND salary_max IS NOT NULL;
            """
        )
        row = self.cur.fetchone()
        return row[0] if row else None

    def get_vacancies_with_higher_salary(self):
        self.cur.execute(
            """
            SELECT e.name,
                   v.name,
                   v.salary_min,
                   v.salary_max,
                   'https://hh.ru/vacancy/' || v.hh_id
            FROM vacancies v
            LEFT JOIN employers e ON v.employer_id = e.employer_id
            WHERE (salary_min + salary_max) / 2.0 >
                  (SELECT AVG((salary_min + salary_max) / 2.0)
                   FROM vacancies
                   WHERE salary_min IS NOT NULL
                     AND salary_max IS NOT NULL);
            """
        )
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        self.cur.execute(
            """
            SELECT e.name,
                   v.name,
                   v.salary_min,
                   v.salary_max,
                   'https://hh.ru/vacancy/' || v.hh_id
            FROM vacancies v
            LEFT JOIN employers e ON v.employer_id = e.employer_id
            WHERE LOWER(v.name) LIKE LOWER(%s);
            """,
            (f"%{keyword}%",)
        )
        return self.cur.fetchall()
