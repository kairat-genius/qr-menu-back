from cs50 import SQL
import json
from auth import Authefication


class Data:
    """ class manipulate with category data """

    def __init__(self):
        self._db = SQL('sqlite:///db.sqlite3')
        self._db._autocommit = True

    """Код админ панели"""

    """Взятие название ресторана"""

    def get_restaurant_data(self, restaurant_name):
        try:
            restaurant_data = self._db.execute('SELECT * FROM Restaurant WHERE restaurant = ?', restaurant_name)
            return restaurant_data[0] if restaurant_data else None
        except Exception as e:
            raise e

    """Взятие паролей из базы данных"""

    def get_user_data_password(self, restaurant_name):
        try:
            query = '''
                SELECT Authefication.password
                FROM Authefication
                INNER JOIN Restaurant ON Authefication.hashf = Restaurant.hashf
                WHERE Restaurant.restaurant = ?
            '''
            user_data = self._db.execute(query, restaurant_name)
            return user_data[0] if user_data else None
        except Exception as e:
            raise e

    """Взятие данных из базы данных"""

    def get_user_data(self, restaurant_name):
        try:
            query = '''
                SELECT Authefication.email, Restaurant.address, Restaurant.restaurant, Restaurant.start_day, Restaurant.end_day, Restaurant.start_time, Restaurant.end_time, Restaurant.logo
                FROM Authefication
                INNER JOIN Restaurant ON Authefication.hashf = Restaurant.hashf
                WHERE Restaurant.restaurant = ?
            '''
            user_data = self._db.execute(query, restaurant_name)
            return user_data[0] if user_data else None
        except Exception as e:
            raise e

    """Взятие данных menu из таблицы базы данных из таблицы Dishes(блюд)"""

    def get_menu_data(self, restaurant_name, dishes_url=None):
        try:
            if dishes_url:
                # Используем фильтрацию по имени блюда, если dishes_url передан
                query = '''
                    SELECT Dishes.id, Dishes.name, Dishes.img, Dishes.weight, Dishes.price, Dishes.comment, Categories.category, GROUP_CONCAT(Ingredients.ingredient) AS ingredients
                    FROM Dishes
                    LEFT JOIN DishIngredient ON Dishes.id = DishIngredient.dish_id
                    LEFT JOIN Ingredients ON DishIngredient.ingredient_id = Ingredients.id
                    JOIN Categories ON Dishes.category_id = Categories.id
                    JOIN Restaurant ON Categories.restaurant_id = Restaurant.id
                    WHERE Restaurant.restaurant = ? AND Dishes.url = ?
                    GROUP BY Dishes.id;
                '''
                menu_data = self._db.execute(query, restaurant_name, dishes_url)
                return menu_data[0] if menu_data else None
            else:
                # В противном случае, получаем все блюда
                query = '''
                    SELECT Dishes.id, Dishes.name, Dishes.img, Dishes.weight, Dishes.price, Dishes.comment, Categories.category, GROUP_CONCAT(Ingredients.ingredient) AS ingredients
                    FROM Dishes
                    LEFT JOIN DishIngredient ON Dishes.id = DishIngredient.dish_id
                    LEFT JOIN Ingredients ON DishIngredient.ingredient_id = Ingredients.id
                    JOIN Categories ON Dishes.category_id = Categories.id
                    JOIN Restaurant ON Categories.restaurant_id = Restaurant.id
                    WHERE Restaurant.restaurant = ?
                    GROUP BY Dishes.id;
                '''
                menu_data = self._db.execute(query, restaurant_name)
                return menu_data if menu_data else None
        except Exception as e:
            raise e

    """Взятие категорий"""
    def get_category_data(self, restaurant_name):
        try:
            query = '''
                SELECT Categories.category
                FROM Categories
                JOIN Restaurant ON Categories.restaurant_id = Restaurant.id
                WHERE Restaurant.restaurant = ?
            '''
            category_data = self._db.execute(query, restaurant_name)
            return category_data if category_data else None
        except Exception as e:
            raise e



    """Взятие данных из таблицы базы данных Tables(столы) """
    def get_table_data(self, restaurant_name):
        try:
            query = '''
                SELECT Tables.id, Tables.menu_link, Tables.qr_code 
                FROM Tables 
                JOIN Restaurant ON Tables.restaurant_id = Restaurant.id
                WHERE Restaurant.restaurant = ?
            '''
            table_data = self._db.execute(query, restaurant_name)
            return table_data if table_data else None
        except Exception as e:
            raise e

    """ Удаление стола """
    def delete_table(self, restaurant_name, id):
        try:
            query = '''
                DELETE FROM Tables
                WHERE id = ? AND restaurant_id = (SELECT id FROM Restaurant WHERE restaurant = ?)
            '''
            self._db.execute(query, id, restaurant_name)
            return True
        except Exception as e:
            print(f"Error in delete_table: {str(e)}")
            return False

    """ Удаление блюда """
    def delete_dishes(self, restaurant_name, id):
        try:
            query = '''
                DELETE FROM Dishes
                WHERE id = ? AND category_id IN (SELECT id FROM Categories WHERE restaurant_id = (SELECT id FROM Restaurant WHERE restaurant = ?))
            '''
            self._db.execute(query, id, restaurant_name)
            return True
        except Exception as e:
            print(f"Error in delete_table: {str(e)}")
            return False



    """Изменения, сохранения данных в базе данных Settings"""
    def update_user_data(self, restaurant, email, password, address, new_restaurant, start_day, end_day, start_time,
                         end_time, logo):
        auth_instance = Authefication()

        # Получаем старый хешированный пароль
        old_data = self.get_user_data_password(restaurant)
        old_hashed_password = old_data.get('password')

        # Хешируем новый пароль, если он передан
        hashed_password = auth_instance._passwordHash(password) if password else old_hashed_password

        auth_update_query = '''
            UPDATE Authefication
            SET email = ?, password = ?
            WHERE hashf = (SELECT hashf FROM Restaurant WHERE restaurant = ?)
        '''
        restaurant_update_query = '''
            UPDATE Restaurant
            SET restaurant=?, address=?, start_day=?, end_day=?, start_time=?, end_time=?, logo=?
            WHERE restaurant = ?
        '''
        self._db.execute(restaurant_update_query, new_restaurant, address, start_day, end_day, start_time, end_time,
                         logo,
                         restaurant)
        self._db.execute(auth_update_query, email, hashed_password, restaurant)

    """Изменения, сохранения данных в базе данных add a new tables"""
    # def update_table_data(self):

    def update_menu_data(self, name, img, price, weight, comment, category, restaurant, dishes_url):

        url = dishes_url
        dishes_update_query = '''
                UPDATE Dishes
                SET name=?, img=?, price=?, weight=?, comment=?, category_id=(
                    SELECT id FROM Categories
                    WHERE (category = ? OR category IS NULL) AND restaurant_id = (
                        SELECT id FROM Restaurant
                        WHERE restaurant = ?
                    )
                )
                WHERE url = ? AND category_id IN (
                    SELECT id FROM Categories
                    WHERE restaurant_id = (
                        SELECT id FROM Restaurant
                        WHERE restaurant = ?
                    )
                )
            '''

        self._db.execute(dishes_update_query, name, img, price, weight, comment, category, restaurant, url, restaurant)

