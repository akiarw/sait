import sqlite3


class DBFWorking:

    def __init__(self, name='photos.db'):
        self.connection = sqlite3.connect(name, check_same_thread=False)

    def get_conn(self):
        return self.connection

    def add_photo(self, photo_id, filename):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO photos
                        (photo_id, photo) 
                        VALUES (?,?)''', (str(photo_id), filename))
        cursor.close()
        self.connection.commit()

    def get_photo(self, photo_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT photo FROM photos WHERE photo_id = ?", (str(photo_id),))
        row = cursor.fetchone()
        cursor.close()
        return row

    def __del__(self):
        self.connection.close()
