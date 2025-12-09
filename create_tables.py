import psycopg2

def create_tables():
    # Параметри підключення до БД (localhost, бо скрипт запускається на вашому ПК)
    db_params = {
        "host": "localhost",
        "database": "hw02",
        "user": "postgres",
        "password": "567234",
        "port": "5432"
    }

    # SQL запити для створення таблиць
    sql_create_users = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100),
        email VARCHAR(100) UNIQUE
    );
    """

    sql_create_status = """
    CREATE TABLE IF NOT EXISTS status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE
    );
    """

    sql_create_tasks = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100),
        description TEXT,
        status_id INTEGER,
        user_id INTEGER,
        FOREIGN KEY (status_id) REFERENCES status (id),
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """

    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                # Видаляємо старі таблиці, щоб створити чисті (порядок важливий!)
                cur.execute("DROP TABLE IF EXISTS tasks;")
                cur.execute("DROP TABLE IF EXISTS status;")
                cur.execute("DROP TABLE IF EXISTS users;")
                
                # Створюємо нові
                cur.execute(sql_create_users)
                cur.execute(sql_create_status)
                cur.execute(sql_create_tasks)
                
                conn.commit()
                print("Таблиці успішно створено.")
    except Exception as e:
        print(f"Помилка: {e}")

if __name__ == '__main__':
    create_tables()
