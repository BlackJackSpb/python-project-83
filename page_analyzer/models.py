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
    urls_data = []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM urls ORDER BY id DESC;")
            urls_data = cur.fetchall()
    finally:
        if conn:
            conn.close()
    return urls_data
