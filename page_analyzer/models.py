import os
import psycopg
from dotenv import load_dotenv
from datetime import date

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    try:
        conn = psycopg.connect(DATABASE_URL)
        return conn
    except psycopg.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        raise


def get_url_by_id(url_id):
    conn = get_db_connection()
    url_data = None
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, created_at FROM urls WHERE id = %s",
                (url_id,)
            )
            url_data = cur.fetchone()
    finally:
        if conn:
            conn.close()
    return url_data


def get_url_by_name(url_name):
    conn = get_db_connection()
    url_data = None
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, created_at FROM urls WHERE name = %s",
                (url_name,)
            )
            url_data = cur.fetchone()
    finally:
        if conn:
            conn.close()
    return url_data


def insert_url(url_name):
    conn = get_db_connection()
    new_url_data = None
    today = date.today()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO urls (name, created_at) VALUES"
                " (%s, %s) RETURNING id, name, created_at",
                (url_name, today)
            )
            new_url_data = cur.fetchone()
            conn.commit()
    except psycopg.Error as e:
        conn.rollback()
        print(f"Ошибка вставки URL: {e}")
    finally:
        if conn:
            conn.close()
    return new_url_data


def get_all_urls():
    conn = get_db_connection()
    urls_list = []
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    urls.id,
                    urls.name,
                    MAX(url_checks.created_at) as last_check_date
                FROM urls
                LEFT JOIN url_checks ON urls.id = url_checks.url_id
                GROUP BY urls.id, urls.name
                ORDER BY urls.id DESC;
                """
            )
            urls_list = cur.fetchall()
    finally:
        if conn:
            conn.close()
    return urls_list


def insert_url_check(url_id):
    conn = get_db_connection()
    success = False
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO url_checks (url_id) VALUES (%s)",
                (url_id,)
            )
            conn.commit()
            success = True
    except psycopg.Error as e:
        conn.rollback()
        print(f"Ошибка вставки проверки URL: {e}")
    finally:
        if conn:
            conn.close()
    return success


def get_url_checks(url_id):
    conn = get_db_connection()
    checks_list = []
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, url_id, status_code, h1, title, description, created_at
                FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC;
                """,
                (url_id,)
            )
            checks_list = cur.fetchall()
    finally:

        if conn:
            conn.close()
    return checks_list


def init_db():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS urls (
                    id serial PRIMARY KEY,
                    name varchar(255) NOT NULL,
                    created_at date NOT NULL
                );
            """)
            conn.commit()
            print("✅ Таблица 'urls' создана или уже существует.")
    except psycopg.Error as e:
        print(f"❌ Ошибка при создании таблицы: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
