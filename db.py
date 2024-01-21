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

    """Взятие данных для settings из базы данных"""

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
                    SELECT Dishes.id, Dishes.name, Dishes.img, Dishes.weight, Dishes.price, Dishes.comment, Categories.category, Categories.color, GROUP_CONCAT(Ingredients.ingredient) AS ingredients_str
                    FROM Dishes
                    LEFT JOIN DishIngredient ON Dishes.id = DishIngredient.dish_id
                    LEFT JOIN Ingredients ON DishIngredient.ingredient_id = Ingredients.id
                    JOIN Categories ON Dishes.category_id = Categories.id
                    JOIN Restaurant ON Categories.restaurant_id = Restaurant.id
                    WHERE Restaurant.restaurant = ? AND Dishes.url = ?
                    GROUP BY Dishes.id;
                '''
                menu_data = self._db.execute(query, restaurant_name, dishes_url)

                # Преобразование строки с ингредиентами в список
                if menu_data and menu_data[0]['ingredients_str']:
                    menu_data[0]['ingredients'] = menu_data[0]['ingredients_str'].split(',')
                    del menu_data[0]['ingredients_str']

                return menu_data[0] if menu_data else None
            else:
                # В противном случае, получаем все блюда
                query = '''
                    SELECT Dishes.id, Dishes.name, Dishes.img, Dishes.weight, Dishes.price, Dishes.comment, Categories.category, GROUP_CONCAT(Ingredients.ingredient) AS ingredients_str
                    FROM Dishes
                    LEFT JOIN DishIngredient ON Dishes.id = DishIngredient.dish_id
                    LEFT JOIN Ingredients ON DishIngredient.ingredient_id = Ingredients.id
                    JOIN Categories ON Dishes.category_id = Categories.id
                    JOIN Restaurant ON Categories.restaurant_id = Restaurant.id
                    WHERE Restaurant.restaurant = ?
                    GROUP BY Dishes.id;
                '''

                menu_data = self._db.execute(query, restaurant_name)

                # Преобразование строки с ингредиентами в список для каждого блюда
                if menu_data:
                    for dish in menu_data:
                        if dish['ingredients_str']:
                            dish['ingredients'] = dish['ingredients_str'].split(',')
                            del dish['ingredients_str']
                        else:
                            dish['ingredients'] = []

                return menu_data if menu_data else None
        except Exception as e:
            raise e

    """Взятие категорий"""

    def get_category_data(self, restaurant_name):
        try:
            query = '''
                SELECT Categories.category, Categories.color
                FROM Categories
                JOIN Restaurant ON Categories.restaurant_id = Restaurant.id
                WHERE Restaurant.restaurant = ?
            '''
            category_data = self._db.execute(query, restaurant_name)
            return category_data if category_data else None
        except Exception as e:
            raise e

    """Взятие старых категорий для изменения по url"""

    def get_category_data_url(self, restaurant_name, category_url):
        try:
            query = '''
                SELECT Categories.category, Categories.color
                FROM Categories
                JOIN Restaurant ON Categories.restaurant_id = Restaurant.id
                WHERE Restaurant.restaurant = ? AND Categories.url = ?
            '''
            category_data = self._db.execute(query, restaurant_name, category_url)
            return category_data[0] if category_data else None
        except Exception as e:
            raise e

    """Получение всех ингредиентов ресторана"""

    def get_ingredients_list(self, restaurant_name):
        try:
            query = '''
                SELECT DISTINCT Ingredients.ingredient
                FROM Ingredients
                WHERE Ingredients.restaurant_id = (
                    SELECT id FROM Restaurant WHERE restaurant = ?
                );
            '''
            ingredients_list = self._db.execute(query, restaurant_name)
            return [ingredient['ingredient'] for ingredient in ingredients_list] if ingredients_list else []
        except Exception as e:
            print(f"Error in get_ingredients_list: {str(e)}")
            return []

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

    def add_tables_data(self, menu_links, qr_codes, restaurant):
        try:

            for i in range(len(menu_links)):
                menu_link = menu_links[i]
                qr_code = qr_codes[i]

                table_add_query = '''
                    INSERT INTO Tables (menu_link, qr_code, restaurant_id)
                    VALUES (?, ?, (
                                SELECT id FROM Restaurant
                                WHERE restaurant = ?
                                )
                            );
                '''
                self._db.execute(table_add_query, menu_link, qr_code, restaurant)

            return {'message': 'Changes saved successfully'}
        except Exception as e:
            raise e

    """Изменения, добавления Блюда"""
    def update_menu_data(self, name, img, price, weight, comment, category, ingredients, restaurant, dishes_url=None):
        try:
            # Если есть dishes_url, выполняем обновление данных о блюде
            if dishes_url:
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
                self._db.execute(dishes_update_query, name, img, price, weight, comment, category, restaurant, url,
                                 restaurant)

                # Получаем id обновленного блюда
                dish_id_query = '''
                    SELECT id FROM Dishes
                    WHERE url = ? AND category_id IN (
                        SELECT id FROM Categories
                        WHERE restaurant_id = (
                            SELECT id FROM Restaurant
                            WHERE restaurant = ?
                        )
                    )
                '''
                dish_id = self._db.execute(dish_id_query, url, restaurant)
            else:
                # Если dishes_url отсутствует, добавляем новое блюдо
                dishes_insert_query = '''
                    INSERT INTO Dishes (name, img, price, weight, comment, category_id)
                    VALUES (?, ?, ?, ?, ?, (
                        SELECT id FROM Categories
                        WHERE (category = ? OR category IS NULL) AND restaurant_id = (
                            SELECT id FROM Restaurant
                            WHERE restaurant = ?
                        )
                    ));
                '''
                self._db.execute(dishes_insert_query, name, img, price, weight, comment, category, restaurant)

                # Получаем id только что добавленного блюда
                dish_id_query = 'SELECT last_insert_rowid() as id;'
                dish_id = self._db.execute(dish_id_query)

            if dish_id and ingredients:
                dish_id = dish_id[0]['id']

                # Удаляем старые ингредиенты блюда
                delete_old_ingredients_query = '''
                    DELETE FROM DishIngredient
                    WHERE dish_id = ?
                '''
                self._db.execute(delete_old_ingredients_query, dish_id)

                # Подготавливаем строку для IN-запроса по ингредиентам
                placeholders = ', '.join(
                    ['(?, (SELECT id FROM Ingredients WHERE ingredient = ?))' for _ in ingredients])

                ingredient_update_query = f'''
                    INSERT OR REPLACE INTO DishIngredient (dish_id, ingredient_id)
                    VALUES {placeholders}
                '''

                # Создаем список параметров для execute
                params_list = [item for sublist in [(dish_id, ingredient) for ingredient in ingredients] for item in
                               sublist]

                # Выполняем запрос
                self._db.execute(ingredient_update_query, *params_list)

        except Exception as e:
            raise e

    def update_category_data(self, category, color, restaurant, category_url=None):
        try:
            # Обновление данных о категории по URL, если указан
            if category_url:
                category_update_query = '''
                    UPDATE Categories
                    SET category = ?, color = ?
                    WHERE restaurant_id = (
                        SELECT id FROM Restaurant
                        WHERE restaurant = ?
                    ) AND url = ?;
                '''
                self._db.execute(category_update_query, category, color, restaurant, category_url)
            else:
                # Добавление новой категории, если не указан URL
                category_insert_query = '''
                    INSERT INTO Categories (category, color, restaurant_id)
                    VALUES (?, ?, (SELECT id FROM Restaurant WHERE restaurant = ?));
                '''
                self._db.execute(category_insert_query, category, color, restaurant)
        except Exception as e:
            raise e
