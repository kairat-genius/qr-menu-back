from cs50 import SQL
import re
import hashlib

_sqlite = SQL('sqlite:///db.sqlite3')
_sqlite._autocommit = True


class Authefication:

    # init database
    def __init__(self):
        self._db = _sqlite

    def _create_restik_table(self) -> None:
        """ Create restik table if not exists """

        self._db.execute(r"""CREATE TABLE IF NOT EXISTS Restaurant (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hashf VARCHAR UNIQUE,
                    restaurant VARCHAR NOT NULL,
                    address VARCHAR,
                    category VARCHAR DEFAULT "{}")""")
        self._db._disconnect()



    def _insert_restik(self, hashf, rest) -> bool:
        """ INSERT DATA TO Restaurant table """

        try:
            self._db.execute("""INSERT INTO Restaurant(hashf,restaurant) VALUES(?, ?)""", hashf, rest)
            self._db._disconnect()
        except:
            return False
        else:
            return True


    def _create_auth_table(self) -> None:
        """ Create autentication table if not exists """

        self._db.execute("""CREATE TABLE IF NOT EXISTS Authefication (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hashf VARCHAR UNIQUE,
                    email VARCHAR NOT NULL,
                    password TEXT NOT NULL,
                    FOREIGN KEY (hashf) REFERENCES Restaurant(hashf) ON DELETE CASCADE)""")
        self._db._disconnect()


    def _insert_auth(self, hashf, **kwrags) -> bool:
        """ Insert in authentication table """

        try:
            self._db.execute("""INSERT INTO Authefication(hashf,email,password,hashf) VALUES(?, ?, ?,?)""",
                                hashf,
                                kwrags['email'],kwrags['password'],hashf
                            )
            self._db._disconnect()
        except:
            return False
        else:
            return True


    def CheckRegxpEmail(self, __email: str) -> bool | str:
        """ Function check correct email input with Regxp """

        if re.match(r'^(\w+)\.?((\w+|\w+\.\w+(\.\w+)?))?@([a-zA-Z]+)\.([a-zA-Z]{2,})(\.[a-zA-Z]{2,})?$', __email):
            return __email
        else: return False



    #Заменил r'^([A-Z]{1,})([\w.]{7,})$' на r'^[a-zA-Z0-9]+$'
    def CheckRegxpPassword(self, _password: str) -> bool | str:
        """ Function check correct password input with Regxp """

        if re.match(r'^[a-zA-Z0-9]+$', _password):
            return _password
        else:
            return False



    @staticmethod
    def _getHash(_email: str) -> hashlib:
        return hashlib.sha256(_email.encode('UTF-8')).hexdigest()



    @staticmethod
    def _passwordHash(_password: str) -> hashlib:
        return hashlib.sha256(_password.encode('UTF-8')).hexdigest()



    def get_user_email(self, __email):
        if user := self._db.execute('SELECT * FROM Authefication WHERE email=?', __email):
            return user
        else: return False


    def auth(self, **kwargs: dict):
        self._create_restik_table()
        self._create_auth_table()

        if email := self.CheckRegxpEmail(kwargs['email']):
            pass
        else:
            return 'Неправильний формат електроної пошти, пошта не має містити . в початку та кінці, може містити тільки один символ @ та не має містити : ; < > -'
        if password := self.CheckRegxpPassword(kwargs['password']):
            pass
        else:
            return 'Пароль повинен складатись з 8 симовлів, мати тільки букви латинського алфавіту, цифри та хоча б один спеціальний символ _ або . без пробілів'


        if self.get_user_email(email):
            return 'USER EMAIL ALREADY REGISTERED'

        else:
            hashf = self._getHash(email)


            if self._insert_restik(hashf, kwargs['restaurant']):
                pass
            else:
                return "insert_restik"
            
            kwargs['password'] = self._passwordHash(password)

            if self._insert_auth(hashf, **kwargs):
                pass
            else:
                self._db.execute('DELETE FROM Restaurant WHERE hashf=?', hashf)
                self._db._disconnect()
                return "insert_auth"
            
            return hashf

class Login(Authefication):

    def __init__(self) -> None:
        self._db = _sqlite


    def loginUser(self, hashkey: str) -> dict | bool:

        if user := self._db.execute("SELECT * FROM Authefication WHERE hashf=?", hashkey):
            self._db._disconnect()
            del user[0]['password']
            return user[0]
        else: 
            self._db._disconnect()
            return False
        

    def authUser(self, _password: str, __email: str) -> (dict | str):
        if self.CheckRegxpEmail(__email):
            user = self.get_user_email(__email)
            match user:
                case False:
                    return 'Користувача з данною поштою не існує'
                case _:
                    us = user[0]
                    if self._passwordHash(_password) == us['password']:
                        del us['password']
                        return us
                    else:
                        return 'Неправильний пароль. Перевірте правильність вводу'


