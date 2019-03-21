import sqlite3
import os
from PIL import Image


class ImWorking:

    def __init__(self, login):
        self.user = login

    def open_image(self, image):
        try:
            return Image.open('{}/{}'.format(self.user, image))
        except FileNotFoundError:
            image += '.jpg'
            try:
                return Image.open('{}/{}'.format(self.user, image))
            except FileNotFoundError:
                return "I don't know file you need((("

    def save_image(self, pic, name):
        saving = True
        while saving:
            try:
                pic.save('static/{}/{}'.format(self.user, name))
                self.save_im_info(name)
                saving = False
            except FileNotFoundError:
                os.mkdir(self.user)
            except ValueError:
                name += '.jpg'
            except AttributeError:
                pic = pic.image


class DBWorking(ImWorking):
    def __init__(self, login, db_name='users.db'):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.access = False
        self.login = login
        super().__init__(login)

    def save_im_info(self, name):
        cursor = self.connection.cursor()
        cursor.execute('INSERT INTO images (login, im_name, likes) VALUES (?,?,?)', (self.login, name, 0))
        self.connection.commit()

    def image_info(self, name):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM images WHERE login = ? AND im_name = ?', (self.login, name))
        info = cursor.fetchone()
        cursor.close()
        return info

    def all_images(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT im_name FROM images WHERE login = ?', (self.login,))
        info = cursor.fetchall()
        cursor.close()
        return [str(i)[2:-3] for i in info]

    def is_login_created(self, login):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE login = ?', (login,))
        login = cursor.fetchone()
        cursor.close()
        return bool(login)

    def get_conn(self):
        return self.connection

    def sign_in(self, password):
        if self.is_login_created(self.login):
            cursor = self.connection.cursor()
            cursor.execute('SELECT password FROM users WHERE login = ?', (self.login,))
            base_password = str(cursor.fetchone())[2:-3]
            cursor.close()
            if base_password == password:
                self.access = True
                return 'successful'
            else:
                return 'wrong password'
        else:
            return 'you should sign up'

    def sign_up(self, password):
        cursor = self.connection.cursor()
        try:
            cursor.execute('INSERT INTO users (login, password) VALUES (?,?)', (self.login, password))
            self.connection.commit()
            cursor.close()
            self.access = True
            os.mkdir('static/' + self.user)
            return 'successful'
        except sqlite3.IntegrityError:
            cursor.close()
            return 'this login has been already created'

    def __del__(self):
        self.connection.close()
