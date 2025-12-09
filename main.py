from pymongo import MongoClient
from bson.objectid import ObjectId

# 1. Підключення до бази даних
try:
    # Підключаємося до локального MongoDB клієнта
    client = MongoClient("mongodb://localhost:27017/")
    # Створюємо (або вибираємо) базу даних "cat_database"
    db = client["cat_database"]
    # Створюємо (або вибираємо) колекцію "cats"
    collection = db["cats"]
    print("Успішне підключення до MongoDB")
except Exception as e:
    print(f"Помилка підключення: {e}")

# --- Допоміжна функція (Create) ---
# Хоч у завданні явно не вимагається окрема функція Create, 
# вона потрібна, щоб наповнити базу початковими даними.
def create_cat(name, age, features):
    try:
        cat_doc = {
            "name": name,
            "age": age,
            "features": features
        }
        result = collection.insert_one(cat_doc)
        print(f"Кота {name} додано. ID: {result.inserted_id}")
    except Exception as e:
        print(f"Помилка при додаванні: {e}")

# --- Читання (Read) ---

def read_all():
    """Виведення всіх записів із колекції."""
    try:
        cats = collection.find()
        print("\n--- Всі коти в базі ---")
        for cat in cats:
            print(cat)
        print("-----------------------")
    except Exception as e:
        print(f"Помилка читання: {e}")

def read_by_name(name):
    """Виведення інформації про кота за ім'ям."""
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(f"\nЗнайдено кота: {cat}")
        else:
            print(f"\nКота з ім'ям '{name}' не знайдено.")
    except Exception as e:
        print(f"Помилка пошуку: {e}")

# --- Оновлення (Update) ---

def update_age(name, new_age):
    """Оновлення віку кота за ім'ям."""
    try:
        # $set змінює значення конкретного поля
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count > 0:
            print(f"Вік кота '{name}' оновлено на {new_age}.")
        elif result.matched_count > 0:
            print(f"Кота знайдено, але вік вже є {new_age}.")
        else:
            print(f"Кота з ім'ям '{name}' не знайдено.")
    except Exception as e:
        print(f"Помилка оновлення: {e}")

def add_feature(name, feature):
    """Додавання нової характеристики до списку features."""
    try:
        # $push додає елемент у масив
        result = collection.update_one({"name": name}, {"$push": {"features": feature}})
        if result.modified_count > 0:
            print(f"Характеристику '{feature}' додано до кота '{name}'.")
        else:
            print(f"Кота з ім'ям '{name}' не знайдено.")
    except Exception as e:
        print(f"Помилка оновлення: {e}")

# --- Видалення (Delete) ---

def delete_by_name(name):
    """Видалення запису з колекції за ім'ям тварини."""
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Кота '{name}' видалено.")
        else:
            print(f"Кота з ім'ям '{name}' не знайдено.")
    except Exception as e:
        print(f"Помилка видалення: {e}")

def delete_all():
    """Видалення всіх записів із колекції."""
    try:
        result = collection.delete_many({})
        print(f"Видалено записів: {result.deleted_count}")
    except Exception as e:
        print(f"Помилка очищення бази: {e}")


# --- Блок перевірки роботи скрипта ---
if __name__ == "__main__":
    # 1. Створюємо тестові дані (щоб було що читати та оновлювати)
    print(">>> Створення даних...")
    create_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    create_cat("murzik", 5, ["любить спати", "чорний"])
    
    # 2. Читаємо всіх
    read_all()
    
    # 3. Читаємо одного
    read_by_name("barsik")
    
    # 4. Оновлюємо вік
    print("\n>>> Оновлюємо вік...")
    update_age("barsik", 4)
    read_by_name("barsik")
    
    # 5. Додаємо характеристику
    print("\n>>> Додаємо характеристику...")
    add_feature("murzik", "ловить мишей")
    read_by_name("murzik")
    
    # 6. Видаляємо одного кота
    print("\n>>> Видаляємо кота...")
    delete_by_name("murzik")
    read_all()
    
    # 7. Видаляємо всіх (розкоментуйте, якщо хочете очистити базу в кінці)
    # print("\n>>> Очищення бази...")
    # delete_all()
    # read_all()
