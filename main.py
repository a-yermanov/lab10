import psycopg2
import csv

# Функция для подключения к базе данных
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="PhoneBook",      # Имя базы данных
            user="postgres",         # Имя пользователя PostgreSQL
            password="0000",         # Пароль пользователя
            host="localhost",        # Хост (обычно localhost)
            port="5432"              # Порт PostgreSQL
        )
        print("Соединение с базой данных установлено.")
        return conn
    except psycopg2.Error as e:
        print("Ошибка подключения к базе данных:", e)
        return None

# Функция для создания таблицы (если она не существует)
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS PhoneBook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            phone_number VARCHAR(15) UNIQUE NOT NULL
        );
        """)
        conn.commit()
        print("Таблица PhoneBook создана.")
    except psycopg2.Error as e:
        print("Ошибка создания таблицы:", e)

# Функция для добавления данных
def insert_data(conn, first_name, last_name, phone_number):
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO PhoneBook (first_name, last_name, phone_number)
        VALUES (%s, %s, %s);
        """, (first_name, last_name, phone_number))
        conn.commit()
        print(f"Данные добавлены: {first_name} {last_name}, {phone_number}.")
    except psycopg2.Error as e:
        print("Ошибка вставки данных:", e)

# Функция для загрузки данных из CSV-файла
def upload_from_csv(conn, file_path):
    try:
        cursor = conn.cursor()
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Пропускаем заголовок
            for row in reader:
                cursor.execute("""
                INSERT INTO PhoneBook (first_name, last_name, phone_number)
                VALUES (%s, %s, %s)
                ON CONFLICT (phone_number) DO NOTHING;
                """, (row[0], row[1], row[2]))
        conn.commit()
        print(f"Данные из файла {file_path} успешно загружены.")
    except Exception as e:
        print("Ошибка загрузки данных из CSV:", e)

# Функция для обновления данных
def update_data(conn):
    try:
        id_to_update = int(input("Введите ID записи для изменения: "))
        print("Выберите, что вы хотите обновить:")
        print("1. Имя")
        print("2. Фамилию")
        print("3. Номер телефона")
        choice = input("Ваш выбор: ")

        if choice == "1":
            new_value = input("Введите новое имя: ")
            column = "first_name"
        elif choice == "2":
            new_value = input("Введите новую фамилию: ")
            column = "last_name"
        elif choice == "3":
            new_value = input("Введите новый номер телефона: ")
            column = "phone_number"
        else:
            print("Неверный выбор.")
            return

        cursor = conn.cursor()
        query = f"UPDATE PhoneBook SET {column} = %s WHERE id = %s;"
        cursor.execute(query, (new_value, id_to_update))
        conn.commit()
        print(f"Данные обновлены: ID={id_to_update}, {column}={new_value}.")
    except Exception as e:
        print("Ошибка обновления данных:", e)

# Функция для удаления данных
def delete_data(conn):
    try:
        id_to_delete = int(input("Введите ID записи для удаления: "))
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PhoneBook WHERE id = %s;", (id_to_delete,))
        conn.commit()
        print(f"Запись с ID={id_to_delete} удалена.")
    except Exception as e:
        print("Ошибка удаления данных:", e)

# Функция для запроса данных
def select_data(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PhoneBook order by 1 ;")
        rows = cursor.fetchall()
        print("Данные в таблице:")
        for row in rows:
            print(f"ID: {row[0]}, Имя: {row[1]}, Фамилия: {row[2]}, Телефон: {row[3]}")
    except psycopg2.Error as e:
        print("Ошибка запроса данных:", e)

# Меню для управления данными
def menu(conn):
    while True:
        print("\nМеню:")
        print("1. Показать все записи")
        print("2. Добавить новую запись")
        print("3. Загрузить данные из CSV")
        print("4. Изменить запись")
        print("5. Удалить запись")
        print("6. Выйти")
        choice = input("Ваш выбор: ")

        if choice == "1":
            select_data(conn)
        elif choice == "2":
            first_name = input("Введите имя: ")
            last_name = input("Введите фамилию: ")
            phone_number = input("Введите номер телефона: ")
            insert_data(conn, first_name, last_name, phone_number)
        elif choice == "3":
            file_path = input("Введите путь к CSV-файлу: ")
            upload_from_csv(conn, file_path)
        elif choice == "4":
            update_data(conn)
        elif choice == "5":
            delete_data(conn)
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор, попробуйте снова.")

# Основной код
if __name__ == "__main__":
    connection = connect_to_db()  # Установить соединение
    if connection:
        menu(connection)  # Запустить меню
        connection.close()
        print("Соединение с базой данных закрыто.")