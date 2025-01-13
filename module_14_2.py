import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

# Код из предыдущего задания:
for i in range(1, 11):
    cursor.execute(''' INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)'''
                   , (f'User{i}', f'example{i}@gmail.com', i * 10, 1000))

for i in range(1, 11):
    if i % 2 != 0:
        cursor.execute('''
        UPDATE Users
        SET balance = balance - 500
        WHERE id = ?
        ''', (i,))

for i in range(1, 11):
    if (i - 1) % 3 == 0:
        cursor.execute('''
        DELETE FROM Users
        WHERE id = ?
        ''', (i,))

cursor.execute('''
    SELECT username, email, age, balance FROM Users WHERE age != 60
    ''')

for username, email, age, balance in cursor.fetchall():
    print(f'Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}')

# Удаление пользователя с id=6
cursor.execute(''' DELETE FROM Users WHERE id = ? ''', (6,))

# Подсчёт кол-ва всех пользователей
cursor.execute('''SELECT COUNT(*) FROM Users''')
total_users = cursor.fetchone()[0]

# Подсчет суммы всех балансов
cursor.execute('''SELECT SUM(balance) FROM Users''')
all_balances = cursor.fetchone()[0]  # Извлекаем значение из кортежа

if total_users > 0:
    average_balance = all_balances / total_users
    print(f'{average_balance}')
else:
    print('Нет пользователей в базе данных.')

connection.commit()
connection.close()
