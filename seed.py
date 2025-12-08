import psycopg2
from faker import Faker
import random

def seed_database():
    db_params = {
        "host": "localhost",
        "database": "hw02",
        "user": "postgres",
        "password": "567234",
        "port": "5432"
    }

    fake = Faker()

    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                # 1. Додавання статусів
                statuses = [('new',), ('in progress',), ('completed',)]
                # ON CONFLICT DO NOTHING дозволяє уникнути помилок дублювання при повторному запуску
                cur.executemany("INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", statuses)
                
                # Отримуємо ID статусів
                cur.execute("SELECT id FROM status")
                status_ids = [row[0] for row in cur.fetchall()]

                # 2. Додавання користувачів
                users = []
                for _ in range(10):  # 10 користувачів
                    users.append((fake.name(), fake.unique.email()))
                
                cur.executemany("INSERT INTO users (fullname, email) VALUES (%s, %s)", users)

                # Отримуємо ID створених користувачів
                cur.execute("SELECT id FROM users")
                user_ids = [row[0] for row in cur.fetchall()]

                # 3. Додавання завдань
                tasks = []
                for _ in range(30):  # 30 завдань
                    title = fake.sentence(nb_words=5)
                    description = fake.text()
                    status_id = random.choice(status_ids)
                    user_id = random.choice(user_ids)
                    tasks.append((title, description, status_id, user_id))

                cur.executemany("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)", tasks)
                
                conn.commit()
                print("Базу даних успішно наповнено випадковими даними.")

    except Exception as e:
        print(f"Помилка при наповненні бази даних: {e}")

if __name__ == '__main__':
    seed_database()