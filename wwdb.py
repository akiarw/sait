import sqlite3


class DBUWorking:
    def __init__(self, login, password, db_name='users.db'):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.access = False
        self.login = login
        self.password = password
        print(self.sign_in())

    def is_login_created(self, login):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE login = ?', (login,))
        login = cursor.fetchone()
        cursor.close()
        return bool(login)

    def get_conn(self):
        return self.connection

    def sign_in(self):
        if self.is_login_created(self.login):
            cursor = self.connection.cursor()
            cursor.execute('SELECT password FROM users WHERE login = ?', (self.login,))
            base_password = str(cursor.fetchone())[2:-3]
            cursor.close()
            if base_password == self.password:
                self.access = True
                return 'successful'
            else:
                return 'wrong password'
        else:
            return 'you should sign up'

    def sign_up(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute('INSERT INTO users (login, password) VALUES (?,?)', (self.login, self.password))
            self.connection.commit()
            cursor.close()
            return 'successful'
        except sqlite3.IntegrityError:
            cursor.close()
            return 'this login has already been created'

    def __del__(self):
        self.connection.close()


class DBFWorking:

    def __init__(self, login, db_name='users.db'):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.login = login

    def get_conn(self):
        return self.connection

    def add_photo(self, filename):
        cursor = self.connection.cursor()
        cursor.execute('INSERT INTO photos (login, photo) VALUES (?,?)', (self.login, filename))
        cursor.close()
        self.connection.commit()

    def get_photos(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT photo FROM photos WHERE login = ?", (self.login,))
        names = cursor.fetchall()
        cursor.close()
        return [str(name)[2:-3] for name in names]

    def __del__(self):
        self.connection.close()
       