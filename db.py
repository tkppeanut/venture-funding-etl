import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "Venture Funding",
    "user": "postgres",
    "password": "090229"
}


def connect_db():
    return psycopg2.connect(**DB_CONFIG)