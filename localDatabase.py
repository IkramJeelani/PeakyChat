import sqlite3


class LocalDB(object):
    connection = sqlite3.connect('database.db')

    with connection:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS user(email string,password string)')
        connection.commit()

    @classmethod
    def insert(cls, Email, Password):
        with cls.connection:
            cursor = cls.connection.cursor()
            cursor.execute('INSERT INTO user VALUES(:email,:password)',
                           {'email': Email, 'password': Password})
            cls.connection.commit()

    @classmethod
    def showAll(cls):
        with cls.connection:
            cursor = cls.connection.cursor()
            cursor.execute('SELECT oid,* FROM user')
            cls.connection.commit()
            return cursor.fetchall()

    @classmethod
    def update(cls, oid, Email, Password):
        with cls.connection:
            cursor = cls.connection.cursor()
            cursor.execute('''UPDATE user SET 
                            email=:email,
                            password=:password
                            WHERE oid=:oid''',

                           {
                               'email': Email,
                               'password': Password,
                               'oid': oid})
            cls.connection.commit()
