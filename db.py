import sqlite3


class User:
    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def register(self, telegram_id, email, status='activate'):
        with self.connection as con:
            con.execute("INSERT INTO users (tg_id, email, status) ""VALUES (?, ?, ?)",
                        (telegram_id, email, status))

    def get_active_list(self):
        with self.connection:
            result = self.cursor.execute("SELECT tg_id FROM users WHERE status=?", ('activate',)).fetchall()
            tg_list = []
            for i in result:
                tg_list.append(i[0])
            return tg_list

    def get_email_channel_list(self):
        with self.connection:
            result = self.cursor.execute("SELECT email FROM users WHERE status=?", ('channels',)).fetchall()
            tg_list = []
            for i in result:
                tg_list.append(i[0])
            return tg_list

    def delete_user(self, email):
        with self.connection:
            self.cursor.execute("DELETE FROM users WHERE email=?", (email,)).fetchall()

    def get_email_active_list(self):
        with self.connection:
            result = self.cursor.execute("SELECT email FROM users WHERE status=?", ('activate',)).fetchall()
            tg_list = []
            for i in result:
                tg_list.append(i[0])
            return tg_list

    def set_status(self, email, status):
        with self.connection:
            self.cursor.execute("UPDATE users SET status=? WHERE email=?", (status, email,))

    def get_id_by_email(self, email):
        result = self.cursor.execute("SELECT tg_id FROM users WHERE email=?", (email,)).fetchone()
        if result is None:
            return False
        return result[0]

    def get_status_by_email(self, email):
        result = self.cursor.execute("SELECT status FROM users WHERE email=?", (email,)).fetchone()
        if result is None:
            return False
        return result[0]


db = User('db.db')
print(db.get_active_list())
print(db.get_email_active_list())
print(db.get_id_by_email('jakemize011@gmail.com'))
