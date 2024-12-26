import sqlite3

conn = sqlite3.connect('not_telegram.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

# Заполнение 10-ю записями:
users = [
    (f'User{i}', f'example{i}@gmail.com', i * 10, 1000) for i in range(1, 11)
]

cursor.executemany('''
INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)
''', users)

conn.commit()
conn.close()

# Обновление balancа у каждой 2ой записи начиная с 1ой на 500:
for i in range(1, 11):
    if i % 2 != 0:
        cursor.execute('''
        UPDATE Users
        SET balance = balance - 500
        WHERE id = ?
        ''', (i,))

conn.commit()
conn.close()

# Удаление каждой 3-ей записи в таблице начиная с 1ой:
for i in range(1, 11):
    if (i - 1) % 3 == 0:
        cursor.execute('''
        DELETE FROM Users
        WHERE id = ?
        ''', (i,))

conn.commit()
conn.close()

# Выборка всех записей при помощи fetchall(), где возраст не равен 60:
cursor.execute('''
SELECT username, email, age, balance FROM Users WHERE age != 60
''')

records = cursor.fetchall()

for record in records:
    username, email, age, balance = record
    print(f'Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}')

conn.commit()
conn.close()
