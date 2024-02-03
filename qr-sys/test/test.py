import requests
import logging
import time
url = "http://localhost:8001"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

with open("token.txt", "r") as file:
    token_cookie = file.read()

cookies = {'token': str(token_cookie)}


class User:
    def register(self):
        data = {
            "email": "test",
            "password": "test",
            "time": {
                "type": "days",
                "number": 1
            }
        }
        response = requests.post(f"{url}/api/admin/register", json=data)
        assert response.status_code == 200
        logger.info("Тест на регистрацию пройден." + str(response.json()["user_data"]))

    def login(self):
        data = {
            "email": "test",
            "password": "test",
            "time": {
                "type": "days",
                "number": 1
            }
        }

        response = requests.post(f"{url}/api/admin/login", json=data)
        assert response.status_code == 200
        token = response.json()["token"]
        logger.info("Тест на авторизацию пройден." + str(response.json()["user_data"]))
        with open("token.txt", "w") as file:
            file.write(token)


class Restaurant:
    def add_restaurant(self):
        data = {
            "name": "strin",
            "address": "string",
            "start_day": "string",
            "end_day": "string",
            "start_time": "string",
            "end_time": "string",
            "logo": "string",
        }
        response = requests.post(f"{url}/api/admin/add/restaurant", json=data, cookies=cookies)
        assert response.status_code == 200
        logger.info("Тест на добавление ресторана пройден." + str(response.json()["restaurant_data"]))

    def update_restaurant(self):
        # Параметры запроса
        data = {
            "name": "s",
            "address": "stg",
            "start_day": "string",
            "end_day": "string",
            "start_time": "string",
            "end_time": "stg",
            "logo": "string",
        }
        response = requests.patch(f"{url}/api/admin/update/restaurant", json=data, cookies=cookies)
        assert response.status_code == 200
        logger.info("Тест на изменения ресторана пройден." + str(response.json()["restaurant_data"]))

    def get_restaurant(self):
        response = requests.get(f"{url}/api/admin/get/restaurant", cookies=cookies)
        assert response.status_code == 200
        logger.info("Тест на просмотр ресторана пройден." + str(response.json()["restaurant_data"]))

    def delete_restaurant(self):
        response = requests.delete(f"{url}/api/admin/delete/restaurant", cookies=cookies)
        assert response.status_code == 200
        logger.info("Тест на удаление ресторана пройден." + str(response.json()["status"]))


class Tables:

    def create_tables(self):
        data = {
            "table_number": 5
        }
        response = requests.post(f"{url}/api/admin/create/tables", json=data, cookies=cookies)
        assert response.status_code == 200
        logger.info("Тест на добавление столов пройден. status: " + str(response.json()["status"]))

    def get_tables(self):
        response = requests.get(f"{url}/api/admin/get/tables?page=1", cookies=cookies)
        assert response.status_code == 200
        logger.info(f"Тест на просмотра столов пройден.{str(response.json()["data"])}")

    def delete_tables(self):
        data = {
            "data": {
                "type": "table",
                "table_number": 1
            }
        }
        response = requests.delete(f"{url}/api/admin/delete/tables", json=data, cookies=cookies)
        assert response.status_code == 200
        logger.info("Тест на удаление столов пройден. status: " + str(response.json()["status"]))


class Category:
    def add_category(self):
        data = {
            "category": "string",
            "color": "string"
        }
        response = requests.post(f"{url}/api/admin/add/category", json=data, cookies=cookies)
        assert response.status_code == 200
        logger.info(f"Тест на добавление категорий пройден. status: {str(response.json()["status"])}")

    def get_categories(self):
        response = requests.get(f"{url}/api/admin/get/categories", cookies=cookies)
        assert response.status_code == 200
        logger.info(f"Тест на просмотр категорий пройден. {str(response.json()["categories"])}")

    def get_restaurant_category(self):
        response = requests.get(f"{url}/api/admin/get-full-info/categories", cookies=cookies)
        assert "restaurant" in response.json()
        logger.info(f"Тест на просмотр ресторана и его категорий пройден. {str(response.json()["restaurant"])}")

    def delete_category(self):
        data = {
            "delete": {
                "type": "category",
                "category_id": 1
            }
        }
        response = requests.delete(f"{url}/api/admin/delete/categories", json=data, cookies=cookies)
        assert response.status_code == 200
        logger.info(f"Тест на удалений категорий пройден. status: {str(response.json()["status"])}")

class Dishes():
    def add_dish(self):
        data = {
            "data": {
                "img": "",
                "name": "string",
                "price": 0,
                "weight": 0,
                "comment": "",
                "category_id": 1
            }
        }
        response = requests.post(f"{url}/api/admin/add/dish", json=data, cookies=cookies)
        assert response.status_code == 200
        logger.info(f"Тест на добавление блюда пройден. status: {str(response.json()["status"])}")

    def get_dish(self):
        response = requests.get(f"{url}/api/admin/get/dish/1", cookies=cookies)
        assert response.status_code == 200
        logger.info(f"Тест на просмотр блюд пройден. dish: {str(response.json()["dish"])}")

    def delete_dish(self):
        data = {
            "dish_id": 1,
            "category_id": 1
        }
        response = requests.delete(f"{url}/api/admin/delete/dish", json=data, cookies=cookies)
        assert response.status_code == 200
        logger.info(f"Test на удаление блюда пройден. status: {str(response.json()["status"])}")


class Ingredient():
    def add_ing(self):
        data = {
            "ingredient": "string",
            "dish_id": 1
        }
        response = requests.post(f"{url}/api/admin/add/ingredient", json=data, cookies=cookies)
        assert response.status_code == 200
        logger.info(f"Test на добавление ингредиентов пройден. ingredient: {str(response.json()["ingredient"])}")

    def get_ing(self):
        response = requests.get(f"{url}/api/admin/get/ingredients?dish_id=2", cookies=cookies)
        assert response.status_code == 200
        logger.info(f"Тест на просмотр ингредиентов пройден. data: {str(response.json()["data"])}")

    def delete_ing(self):
        data = {
            "ingredient_id": 1,
            "dish_id": 1
        }
        response = requests.delete(f"{url}/api/admin/delete/ingredients", json=data, cookies=cookies)
        assert response.status_code == 200
        logger.info(f"Test на добавление ингредиентов пройден. status: {str(response.json()["status"])}")


user = User()
restaurant = Restaurant()
category = Category()
tables = Tables()
dishes = Dishes()
ingredient = Ingredient()

if __name__ == "__main__":
   """Проверку делать желательно по одному"""
   user.register() # регистарция
   user.login() # авторизация
   time.sleep(10)
   restaurant.add_restaurant() # добавление ресторана
   restaurant.get_restaurant() # просмотр ресторана
   restaurant.update_restaurant() # изменения ресторана
   restaurant.delete_restaurant() # удаление ресторана
   restaurant.add_restaurant()  # добавление ресторана повторно чтобы испытать другие части кода
   category.add_category() # добавление категорий
   category.get_categories() # просмотор категорий
   category.get_restaurant_category() # просмотр ресторана и его категорий
   category.delete_category() # удаление категорий
   tables.create_tables() # добавление столов
   tables.get_tables() # просмотр столов
   tables.delete_tables() # удаление столов
   dishes.add_dish() # добавление блюд
   dishes.get_dish() # просмотр блюд
   dishes.delete_dish() # удаление блюд
   ingredient.add_ing() # добавление ингрединетов
   ingredient.get_ing() # просмотр ингредиентов
   ingredient.delete_ing() # удаление ингредиентов


