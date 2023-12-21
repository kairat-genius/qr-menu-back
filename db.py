from cs50 import SQL
import json

class Data:
    """ class manipulate with category data """

    def __init__(self):
        self._db = SQL('sqlite:///db.sqlite3')
        self._db._autocommit = True


    def _update_category_column(self, hashf: str, category: str) -> None:
        """ ONLY UPDATE Restaurant category column """

        self._db.execute("UPDATE Restaurant SET category=? WHERE hashf=?", json.dumps(category), hashf)
        self._db._disconnect()


    def getCategoryColumn(self, hashkey: str) -> dict:
        return json.loads(self._db.execute('SELECT category FROM Restaurant WHERE hashf=?', hashkey)[0]['category'])


    def getParentCategory(self, hashkey: str, ParentCatery: str) -> dict | KeyError:
        column = self.getCategoryColumn(hashkey)
        try:
            return column[ParentCatery]
        except KeyError as e:
            raise e
        
    def getParentCategoryList(self, hashkey: str) -> list | KeyError:
        column = self.getCategoryColumn(hashkey)
        try:
            return list(column.keys())
        except KeyError as e:
            raise e

    def setParentCategory(self, hashkey: str, ParentCategory: str) -> bool:
        try:
            self.getParentCategory(hashkey, ParentCategory)
        except KeyError:
            column = self.getCategoryColumn(hashkey)
            column[ParentCategory] = {}
            self._update_category_column(hashkey, column)

            return True
        else:
            return False
        
    def deleteParentCategory(self, hashkey: str, ParentCategory: str) -> bool:
        try:
            self.getParentCategory(hashkey, ParentCategory)
        except KeyError as e:
            raise e
        else:
            column = self.getCategoryColumn(hashkey)
            del column[ParentCategory]
            self._update_category_column(hashkey, column)
            return True
        
    def getParentCategoryNode(self, hashkey: str, ParentCategory: str, Node: str) -> dict | KeyError:
        try:
            self.getParentCategory(hashkey, ParentCategory)
        except KeyError as e:
            raise e
        else:
            column = self.getCategoryColumn(hashkey)
            try:
                return column[ParentCategory][Node]
            except KeyError as e:
                raise e
    
    def getParentCategoryNodeList(self, hashkey: str, ParentCategory: str) -> list | KeyError:
        try:
            self.getParentCategory(hashkey, ParentCategory)
        except KeyError as e:
            raise e
        else:
            column = self.getCategoryColumn(hashkey)
            try:
                return list(column[ParentCategory].keys())
            except KeyError as e:
                raise e
    
    def setParentCategoryNode(self, hashkey: str, ParentCategory: str, Node: str) -> dict | KeyError:
        try:
            self.getParentCategory(hashkey, ParentCategory)
        except KeyError as e:
            raise e
        else:
            column = self.getCategoryColumn(hashkey)
            
            column[ParentCategory][Node] = []
            self._update_category_column(hashkey, column)

            return True
    
    
    def deleteParentCategoryNode(self, hashkey: str, ParentCategory: str, Node: str) -> bool:
        try:
            self.getParentCategory(hashkey, ParentCategory)
        except KeyError as e:
            raise e
        else:
            column = self.getCategoryColumn(hashkey)

            try:
                del column[ParentCategory][Node]
                self._update_category_column(hashkey, column)

                return True
            except KeyError:
                return False
            
    
    def getCategoryNodeDish(self, hashkey: str, ParentCategory: str, Node: str, dishName: str) -> dict | bool:
        try:
            self.getParentCategoryNode(hashkey, ParentCategory, Node)
        except KeyError as e:
            raise e
        else:
            column = self.getCategoryColumn(hashkey)

            nodesList = column[ParentCategory][Node]

            for i in range(len(nodesList)):
                if dishName == nodesList[i]['dishName']:
                    return nodesList[i]
                
            return False
    
    def deleteCategoryNodeDish(self, hashkey: str, ParentCategory: str, Node: str, dishName: str) -> KeyError | bool:
        try:
            self.getParentCategoryNode(hashkey, ParentCategory, Node)
        except KeyError as e:
            raise e
        else:
            column = self.getCategoryColumn(hashkey)

            nodesList = column[ParentCategory][Node]

            
            for i in range(len(nodesList)):
                if dishName == nodesList[i]['dishName']:
                    del column[ParentCategory][Node][i]
                    self._update_category_column(hashkey, column)
                    return True
                
            return False
            
    

    def getCategoryNodeDishes(self, hashkey: str, ParentCategory: str, Node: str) -> list[dict]:
        try:
            self.getParentCategoryNode(hashkey, ParentCategory, Node)
        except KeyError as e:
            raise e
        else:
            column = self.getCategoryColumn(hashkey)

            return column[ParentCategory][Node]



    def setCategoryNodeDish(self, hashkey: str, ParentCategory: str, Node: str, **dishes: dict) -> bool | KeyError:
        try:
            self.getParentCategoryNode(hashkey, ParentCategory, Node)
        except KeyError as e:
            raise e
        
        else:
            if self.getCategoryNodeDish(hashkey, ParentCategory, Node, dishes['dishName']):
                return False
            else:
                column = self.getCategoryColumn(hashkey)

                try:
                    column[ParentCategory][Node].append({'dishName': dishes['dishName'],
                                                     'dishDescription': dishes['dishDescription'],
                                                     'dishPrice' : dishes['dishPrice'],
                                                     'dishPhotoLink': dishes['dishPhotoLink']})
                    
                    self._update_category_column(hashkey, column)
                    return True
                
                except KeyError as e:
                    raise e

    """Код админ панели"""

    def get_restaurant_data(self, restaurant_name):
        try:
            restaurant_data = self._db.execute('SELECT * FROM Restaurant WHERE restaurant=?', restaurant_name)
            return restaurant_data[0] if restaurant_data else None
        except Exception as e:
            raise e

    def update_user_data(self, restaurant, email, password, address, new_restaurant_name):
        """ Обновление данных пользователя в базе данных """

        # обновления данных в таблице Authefication
        auth_update_query = """
            UPDATE Authefication
            SET email=?, password=?
            WHERE hashf=(SELECT hashf FROM Restaurant WHERE restaurant=?)
        """

        # обновления данных в таблице Restaurant
        restaurant_update_query = """
            UPDATE Restaurant
            SET restaurant=?, address=?
            WHERE restaurant=?
        """

        #обновления данных в базе данных
        self._db.execute(auth_update_query, email, password, restaurant)
        self._db.execute(restaurant_update_query, new_restaurant_name, address, restaurant)