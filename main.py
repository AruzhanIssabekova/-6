import psycopg2

with psycopg2.connect(
        dbname="work_db",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432",
) as connect:
    # Для создания таблицы
    user_choice = input("ЧТО???")

    with connect.cursor() as cur:
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS users
        (
            user_id serial,
            user_name VARCHAR(100),
            user_password VARCHAR(100),
            user_role VARCHAR(100) DEFAULT 'user',

            CONSTRAINT pk_user_id PRIMARY KEY (user_id),
            CONSTRAINT unique_user_name UNIQUE (user_name),
            CONSTRAINT user_role_good CHECK (user_role IN ('admin', 'user')) ,
            CONSTRAINT pass_len_chek CHECK (LENGTH(user_password) >= 8)
        )
        """
        )
        connect.commit()
    with connect.cursor() as cur:
        cur.execute(f"""
                    INSERT INTO users (user_name, user_password, user_role) VALUES
                    ('admin', 'Admin123*', 'admin')
                    """)
    if user_choice == "1":
        # Регистрация correct
        with connect.cursor() as cur:
            user_name = input("Введите логин: ")
            user_password = input("Введите пароль: ")

            cur.execute(f"SELECT user_id FROM users WHERE user_name = '{user_name}';")

            user = cur.fetchone()

            if user:
                print("Данный никнейм уже занят!")
            elif len(user_password) < 8:
                print("Ваш пароль не может содержать меньше 8 символов!")
            else:
                cur.execute(
                    f"""
                    INSERT INTO users (user_name, user_password, user_role) VALUES 
                    ('{user_name}', '{user_password}', 'user')
                    """
                )
                connect.commit()
    elif user_choice == "2":
        # Авторизация
        with connect.cursor() as cur:
            for count in range(3, 0, -1):
                login = input("Введите ваш логин: ")
                password = input("Введите ваш пароль: ")
                cur.execute(
                    f"""
                            SELECT user_name, user_password, user_role FROM users
                            WHERE user_name = '{login}' AND user_password = '{password}'
                    """
                )
                user = cur.fetchone()
                if not user:
                    print(f"Не верные данные! Осталось {count - 1} попыток")
                    continue

                print(f"Вы вошли в систему! Ваша роль {user[2]}")
                if user[2] == 'admin':
                    a = input('Вы желаете удалить пользователя (ды\нет)?')
                    if a == 'да':
                        user_id_to_delete = input("Введите ID пользователя для удаления: ")
                        try:
                            cur.execute(f"DELETE FROM users WHERE user_id = {user_id_to_delete}")
                            connect.commit()
                            print("Пользователь успешно удален.")
                        except psycopg2.errors.IntegrityError as e:
                            print("Ошибка удаления пользователя:", e)
                break
