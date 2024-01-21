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
        """ Create Restaurant table if not exists """
        self._db.execute(r"""CREATE TABLE IF NOT EXISTS Restaurant (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    hashf VARCHAR UNIQUE,
                    restaurant VARCHAR NOT NULL,
                    address VARCHAR,
                    start_day VARCHAR,
                    end_day VARCHAR,
                    start_time TIME,
                    end_time TIME,
                    logo BLOB)""")

    def _insert_restik(self, hashf, rest, address=None, start_day=None, end_day=None, start_time=None,
                       end_time=None, logo=None) -> bool:
        """ INSERT DATA TO Restaurant table """
        try:
            self._db.execute(
                """INSERT INTO Restaurant(hashf, restaurant, address, start_day, end_day, start_time, end_time, logo) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
                hashf, rest, address, start_day, end_day, start_time, end_time, logo)

        except:
            return False
        else:
            return True

    def _create_categories_table(self) -> None:
        """ Create Categories table if not exists """
        self._db.execute(r"""CREATE TABLE IF NOT EXISTS Categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category VARCHAR NOT NULL,
                    url VARCHAR,
                    color VARCHAR,
                    restaurant_id INTEGER,
                    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(id) ON DELETE CASCADE)""")

    def _create_dishes_table(self) -> None:
        """ Create Dishes table if not exists """
        self._db.execute(r"""CREATE TABLE IF NOT EXISTS Dishes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    img BLOB,
                    name VARCHAR NOT NULL,
                    url VARCHAR,
                    price INTEGER,
                    weight INTEGER,
                    comment VARCHAR,
                    category_id INTEGER,
                    FOREIGN KEY (category_id) REFERENCES Categories(id) ON DELETE CASCADE)""")

    def _create_ingredients_table(self) -> None:
        """ Create Ingredients table if not exists """
        self._db.execute(r"""CREATE TABLE IF NOT EXISTS Ingredients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ingredient VARCHAR,
                    restaurant_id INTEGER,
                    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(id) ON DELETE CASCADE)""")

    def _create_dish_ingredient_table(self) -> None:
        """ Связь многие ко многим таблицы блюд и ингредиентов """
        self._db.execute(r"""CREATE TABLE IF NOT EXISTS DishIngredient (
                       dish_id INTEGER,
                       ingredient_id INTEGER,
                       PRIMARY KEY (dish_id, ingredient_id),
                       FOREIGN KEY (dish_id) REFERENCES Dishes(id) ON DELETE CASCADE,
                       FOREIGN KEY (ingredient_id) REFERENCES Ingredients(id) ON DELETE CASCADE)""")

    def _create_tables(self) -> None:
        """ Create Tables (столы) if not exists """
        self._db.execute(r"""CREATE TABLE IF NOT EXISTS Tables (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    menu_link VARCHAR,
                    qr_code VARCHAR,
                    restaurant_id INTEGER,
                    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(id) ON DELETE CASCADE)""")

    def _create_auth_table(self) -> None:
        """ Create autentication table if not exists """

        self._db.execute("""CREATE TABLE IF NOT EXISTS Authefication (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hashf VARCHAR UNIQUE,
                    email VARCHAR NOT NULL,
                    password TEXT NOT NULL,
                    FOREIGN KEY (hashf) REFERENCES Restaurant(hashf) ON DELETE CASCADE)""")


    def _insert_auth(self, hashf, **kwrags) -> bool:
        """ Insert in authentication table """

        try:
            self._db.execute("""INSERT INTO Authefication(hashf,email,password) VALUES(?, ?, ?)""",
                             hashf,
                             kwrags['email'], kwrags['password']
                             )

        except:
            return False
        else:
            return True

    def CheckRegxpEmail(self, __email: str) -> bool | str:
        """ Function check correct email input with Regxp """

        if re.match(r'^(\w+)\.?((\w+|\w+\.\w+(\.\w+)?))?@([a-zA-Z]+)\.([a-zA-Z]{2,})(\.[a-zA-Z]{2,})?$', __email):
            return __email
        else:
            return False

    # Заменил r'^([A-Z]{1,})([\w.]{7,})$' на r'^[a-zA-Z0-9]+$'
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
        else:
            return False

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


auth_instance = Authefication()

# Создание таблиц
auth_instance._create_dishes_table()
auth_instance._create_restik_table()
auth_instance._create_categories_table()
auth_instance._create_auth_table()
auth_instance._create_tables()
auth_instance._create_ingredients_table()
auth_instance._create_dish_ingredient_table()
