# -*- coding: utf-8 -*-

import mysql.connector
# import Category  --> ne fonctionne pas, le bon syntaxe : from Category import *
from Product import *
from Display import Display
import requests
import json
from configuration import TABLES, globals, sql_queries


class Create_empty_database:
    """Comment."""

    def __init__(self):
        """Initiate Create empty database Class."""
        self.mydb = self.connect_to_database()
        self.cursor = self.mydb.cursor()
        self.create_new_database()

    def connect_to_database(self):
        """Connection to database and creates a cursor."""
        mydb = mysql.connector.connect(
            host=globals.HOST,
            user=globals.USER,
            passwd=globals.PASSWORD,
        )
        return mydb

    def create_new_database(self):
        """Comment."""
        req = "CREATE database {}".format(globals.DB_NAME)
        self.cursor.execute(req)
        self.cursor.execute(TABLES['category'])
        self.cursor.execute(TABLES['product'])
        self.cursor.execute(TABLES['category_has_product'])


class Category:
    """Comment."""

    def __init__(self):
        """Initiate Category Class."""
        self.mydb = self.connect_to_database_p5_off()
        self.cursor = self.mydb.cursor()
        self.insert_categories()

    def connect_to_database_p5_off(self):
        """Connection to database and creates a cursor."""
        mydb = mysql.connector.connect(
            host=globals.HOST,
            user=globals.USER,
            passwd=globals.PASSWORD,
            database=globals.DB_NAME
        )
        return mydb

    def insert_categories(self):
        """Insert categories names in database p5_off."""
        data = [
            (globals.CATEGORIES[0],),
            (globals.CATEGORIES[1],),
            (globals.CATEGORIES[2],),
            (globals.CATEGORIES[3],),
            (globals.CATEGORIES[4],),
        ]

        stmt = "INSERT INTO category (name) VALUES (%s)"
        self.cursor.executemany(stmt, data)
        self.mydb.commit()


class Download_products:
    """Comment."""

    def __init__(self):
        """Initiate Category Class."""
        self.mydb = self.connect_to_database_p5_off()
        self.cursor = self.mydb.cursor()
        self.products_for_beverage()
        self.products_for_meal()
        self.products_for_meat()
        self.products_for_cheese()
        self.products_for_dessert()

    def connect_to_database_p5_off(self):
        """Connection to database and creates a cursor."""
        mydb = mysql.connector.connect(
            host=globals.HOST,
            user=globals.USER,
            passwd=globals.PASSWORD,
            database=globals.DB_NAME
        )
        return mydb

    def products_for_beverage(self):
        """50 most popular products sold in beverage category in France."""
        request_beverage = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0"
                                        "=categories&tag_contains_0=contains&tag_0=boissons&sort_by"
                                        "=unique_scans_n&page_size=50&json=true")
        request_beverage_text = request_beverage.text
        data_beverage = json.loads(request_beverage_text)
        # json.dump(data_beverage, open('data.json', "w"), indent=4)    # visualize data in data.json
        products_list = data_beverage["products"]  # products_list = list de dictionnaires
        # json.dump(products_list, open('data.json', "w"), indent=4)    # visualize data in data.json

        products_no_empty_fields = []
        for p in products_list:
            if p.get('product_name_fr') \
                    and p.get('generic_name_fr') \
                    and p.get('nutrition_grade_fr') \
                    and p.get('brands') \
                    and p.get('stores') \
                    and p.get('url') \
                    and p.get('categories') is not None:
                products_no_empty_fields.append(p)

        # json.dump(products_no_empty_fields, open('data.json', "w"), indent=4)    # visualize data in data.json
        # 32 products with no empty fields

        # Renaming products fields
        clean_products = []
        for product in products_no_empty_fields:
            product['product_name_fr'] = \
                product['product_name_fr'].strip().lower().capitalize()  # str
            product['categories'] = \
                [name.strip().lower().capitalize()
                 for name in product['categories'].split(',')]  # list
            product['stores'] = \
                [store.strip().upper()
                 for store in product['stores'].split(',')]  # list
            product['nutrition_grade_fr'] = \
                product['nutrition_grade_fr'].strip().upper()
            clean_products.append(product)
            # json.dump(clean_products, open('data.json', "w"), indent=4)  # visualize data in data.json

            # Au final, on a :
            # - Les produits filtrés avec tous les champs, parmis les 50 boissons les plus vendus en France
            # - Les produits sont dans la liste clean_products
            # - Les noms, affichages des champs on été modifiés pour la lisibilité

        final_products = []
        for one_product_dict in clean_products:
            # print(one_product_dict['product_name_fr'])
            my_product = Product(one_product_dict)  # execute Product class
            # print(my_product.name)  # .name  permet de lire le nom de l'instance my_product de la classe Product
            final_products.append(my_product)
            # print(final_products)  # Les instances de la class Product sont bien dans la liste

        def insert_product(one_product):
            """Comment."""

            # data_product = {'name': one_product.name,
            #                 'description': one_product.description,
            #                 'grade': one_product.grade,
            #                 'brand': one_product.brands,
            #                 'store': one_product.stores[0],  # download only first store in stores list
            #                 'url': one_product.url,
            #                 }

            ################  <<   AJOUT "beverage" dans le champs category pour identifier les boissons

            data_product = {'name': one_product.name,
                            'description': one_product.description,
                            'grade': one_product.grade,
                            'brand': one_product.brands,
                            'store': one_product.stores[0],  # download only first store in stores list
                            'url': one_product.url,
                            'category': globals.category_field_beverage,
                            }

            ################ >>

            self.cursor.execute(sql_queries.INSERT_PRODUCTS, data_product)
            self.mydb.commit()

        for one_product in final_products:
            # print(one_product.url)
            insert_product(one_product)

    def products_for_meal(self):
        """50 most popular products sold in beverage category in France."""
        request_meal = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0"
                                    "=categories&tag_contains_0=contains&tag_0=plats_prepares&sort_by"
                                    "=unique_scans_n&page_size=50&json=true")
        request_meal_text = request_meal.text
        data_meal = json.loads(request_meal_text)
        # json.dump(data_beverage, open('data.json', "w"), indent=4)    # visualize data in data.json
        products_list = data_meal["products"]  # products_list = list de dictionnaires
        # json.dump(products_list, open('data.json', "w"), indent=4)    # visualize data in data.json

        products_no_empty_fields = []
        for p in products_list:
            if p.get('product_name_fr') \
                    and p.get('generic_name_fr') \
                    and p.get('nutrition_grade_fr') \
                    and p.get('brands') \
                    and p.get('stores') \
                    and p.get('url') \
                    and p.get('categories') is not None:
                products_no_empty_fields.append(p)

        # json.dump(products_no_empty_fields, open('data.json', "w"), indent=4)    # visualize data in data.json
        # 32 products with no empty fields

        # Renaming products fields
        clean_products = []
        for product in products_no_empty_fields:
            product['product_name_fr'] = \
                product['product_name_fr'].strip().lower().capitalize()  # str
            product['categories'] = \
                [name.strip().lower().capitalize()
                 for name in product['categories'].split(',')]  # list
            product['stores'] = \
                [store.strip().upper()
                 for store in product['stores'].split(',')]  # list
            product['nutrition_grade_fr'] = \
                product['nutrition_grade_fr'].strip().upper()
            clean_products.append(product)
            # json.dump(clean_products, open('data.json', "w"), indent=4)  # visualize data in data.json

        final_products = []
        for one_product_dict in clean_products:
            # print(one_product_dict['product_name_fr'])
            my_product = Product(one_product_dict)  # execute Product class
            # print(my_product.name)  # .name  permet de lire le nom de l'instance my_product de la classe Product
            final_products.append(my_product)
            # print(final_products)  # Les instances de la class Product sont bien dans la liste

        def insert_product(one_product):
            """Comment."""

            data_product = {'name': one_product.name,
                            'description': one_product.description,
                            'grade': one_product.grade,
                            'brand': one_product.brands,
                            'store': one_product.stores[0],  # download only first store in stores list
                            'url': one_product.url,
                            'category': globals.category_field_meal,
                            }

            self.cursor.execute(sql_queries.INSERT_PRODUCTS, data_product)
            self.mydb.commit()

        for one_product in final_products:
            # print(one_product.url)
            insert_product(one_product)

    def products_for_meat(self):
        """50 most popular products sold in beverage category in France."""
        request_meat = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0"
                                    "=categories&tag_contains_0=contains&tag_0=viandes&sort_by"
                                    "=unique_scans_n&page_size=50&json=true")
        request_meat_text = request_meat.text
        data_meat = json.loads(request_meat_text)
        products_list = data_meat["products"]

        products_no_empty_fields = []
        for p in products_list:
            if p.get('product_name_fr') \
                    and p.get('generic_name_fr') \
                    and p.get('nutrition_grade_fr') \
                    and p.get('brands') \
                    and p.get('stores') \
                    and p.get('url') \
                    and p.get('categories') is not None:
                products_no_empty_fields.append(p)

        clean_products = []
        for product in products_no_empty_fields:
            product['product_name_fr'] = \
                product['product_name_fr'].strip().lower().capitalize()  # str
            product['categories'] = \
                [name.strip().lower().capitalize()
                 for name in product['categories'].split(',')]  # list
            product['stores'] = \
                [store.strip().upper()
                 for store in product['stores'].split(',')]  # list
            product['nutrition_grade_fr'] = \
                product['nutrition_grade_fr'].strip().upper()
            clean_products.append(product)

        final_products = []
        for one_product_dict in clean_products:
            my_product = Product(one_product_dict)
            final_products.append(my_product)

        def insert_product(one_product):
            """Comment."""

            data_product = {'name': one_product.name,
                            'description': one_product.description,
                            'grade': one_product.grade,
                            'brand': one_product.brands,
                            'store': one_product.stores[0],  # download only first store in stores list
                            'url': one_product.url,
                            'category': globals.category_field_meat,
                            }

            self.cursor.execute(sql_queries.INSERT_PRODUCTS, data_product)
            self.mydb.commit()

        for one_product in final_products:
            insert_product(one_product)

    def products_for_cheese(self):
        """50 most popular products sold in beverage category in France."""
        request_cheese = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0"
                                      "=categories&tag_contains_0=contains&tag_0=fromages&sort_by"
                                      "=unique_scans_n&page_size=50&json=true")
        request_cheese_text = request_cheese.text
        data_cheese = json.loads(request_cheese_text)
        products_list = data_cheese["products"]

        products_no_empty_fields = []
        for p in products_list:
            if p.get('product_name_fr') \
                    and p.get('generic_name_fr') \
                    and p.get('nutrition_grade_fr') \
                    and p.get('brands') \
                    and p.get('stores') \
                    and p.get('url') \
                    and p.get('categories') is not None:
                products_no_empty_fields.append(p)

        # Renaming products fields
        clean_products = []
        for product in products_no_empty_fields:
            product['product_name_fr'] = \
                product['product_name_fr'].strip().lower().capitalize()  # str
            product['categories'] = \
                [name.strip().lower().capitalize()
                 for name in product['categories'].split(',')]  # list
            product['stores'] = \
                [store.strip().upper()
                 for store in product['stores'].split(',')]  # list
            product['nutrition_grade_fr'] = \
                product['nutrition_grade_fr'].strip().upper()
            clean_products.append(product)

        final_products = []
        for one_product_dict in clean_products:
            my_product = Product(one_product_dict)
            final_products.append(my_product)

        def insert_product(one_product):
            """Comment."""

            data_product = {'name': one_product.name,
                            'description': one_product.description,
                            'grade': one_product.grade,
                            'brand': one_product.brands,
                            'store': one_product.stores[0],  # download only first store in stores list
                            'url': one_product.url,
                            'category': globals.category_field_cheese,
                            }

            self.cursor.execute(sql_queries.INSERT_PRODUCTS, data_product)
            self.mydb.commit()

        for one_product in final_products:
            insert_product(one_product)

    def products_for_dessert(self):
        """50 most popular products sold in beverage category in France."""
        request_dessert = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0"
                                       "=categories&tag_contains_0=contains&tag_0=desserts&sort_by"
                                       "=unique_scans_n&page_size=50&json=true")
        request_dessert_text = request_dessert.text
        data_dessert = json.loads(request_dessert_text)
        products_list = data_dessert["products"]

        products_no_empty_fields = []
        for p in products_list:
            if p.get('product_name_fr') \
                    and p.get('generic_name_fr') \
                    and p.get('nutrition_grade_fr') \
                    and p.get('brands') \
                    and p.get('stores') \
                    and p.get('url') \
                    and p.get('categories') is not None:
                products_no_empty_fields.append(p)

        # Renaming products fields
        clean_products = []
        for product in products_no_empty_fields:
            product['product_name_fr'] = \
                product['product_name_fr'].strip().lower().capitalize()  # str
            product['categories'] = \
                [name.strip().lower().capitalize()
                 for name in product['categories'].split(',')]  # list
            product['stores'] = \
                [store.strip().upper()
                 for store in product['stores'].split(',')]  # list
            product['nutrition_grade_fr'] = \
                product['nutrition_grade_fr'].strip().upper()
            clean_products.append(product)

        final_products = []
        for one_product_dict in clean_products:
            my_product = Product(one_product_dict)
            final_products.append(my_product)

        def insert_product(one_product):
            """Comment."""

            data_product = {'name': one_product.name,
                            'description': one_product.description,
                            'grade': one_product.grade,
                            'brand': one_product.brands,
                            'store': one_product.stores[0],  # download only first store in stores list
                            'url': one_product.url,
                            'category': globals.category_field_dessert,
                            }

            self.cursor.execute(sql_queries.INSERT_PRODUCTS, data_product)
            self.mydb.commit()

        for one_product in final_products:
            insert_product(one_product)


class Category_has_product:
    """Comment."""

    def __init__(self):
        """Initiate Category Class."""
        self.mydb = self.connect_to_database_p5_off()
        self.cursor = self.mydb.cursor()
        self.get_beverage_ids_list()
        self.get_meal_ids_list()
        self.get_meat_ids_list()
        self.get_cheese_ids_list()
        self.get_dessert_ids_list()

    def connect_to_database_p5_off(self):
        """Connection to database and creates a cursor."""
        mydb = mysql.connector.connect(
            host=globals.HOST,
            user=globals.USER,
            passwd=globals.PASSWORD,
            database=globals.DB_NAME
        )
        return mydb

    def get_beverage_ids_list(self):
        # get all ids of products in product table with category name = beverage
        self.cursor.execute(sql_queries.SELECT_BEVERAGE_PRODUCT_ID)
        beverage_ids = self.cursor.fetchall()  # list of tuples
        beverage_ids_list = [i[0] for i in beverage_ids]  # transform list of tuples into list of integers

        # print(beverage_ids_list)
        # insert in table category_has_product
        def insert_in_category_has_product(beverage_product_id):
            """comment."""
            # Get beverage id in category table
            self.cursor.execute(sql_queries.SELECT_BEVERAGE_CATEGORY_ID)
            beverage_category_id = self.cursor.fetchone()[0]  # [0] returns "int" not tuple

            data_product_id = {'product_id': beverage_product_id,
                               'category_id': beverage_category_id,
                               }

            self.cursor.execute(sql_queries.INSERT_PRODUCT_CATEGORY, data_product_id)
            self.mydb.commit()

        for beverage_product_id in beverage_ids_list:
            insert_in_category_has_product(beverage_product_id)

    def get_meal_ids_list(self):
        # get all ids of products in product table with category name = Plats Préparés
        self.cursor.execute(sql_queries.SELECT_MEAL_PRODUCT_ID)
        meal_ids = self.cursor.fetchall()  # list of tuples
        meal_ids_list = [i[0] for i in meal_ids]  # transform list of tuples into list of integers

        # print(beverage_ids_list)

        # insert in table category_has_product
        def insert_in_category_has_product(meal_product_id):
            """comment."""

            # Get beverage id in category table
            self.cursor.execute(sql_queries.SELECT_MEAL_CATEGORY_ID)
            meal_category_id = self.cursor.fetchone()[0]  # [0] returns "int" not tuple

            data_product_id = {'product_id': meal_product_id,
                               'category_id': meal_category_id,
                               }

            self.cursor.execute(sql_queries.INSERT_PRODUCT_CATEGORY, data_product_id)
            self.mydb.commit()

        for meal_product_id in meal_ids_list:
            insert_in_category_has_product(meal_product_id)

    def get_meat_ids_list(self):
        # get all ids of products in product table with category name = Plats Préparés
        self.cursor.execute(sql_queries.SELECT_MEAT_PRODUCT_ID)
        meat_ids = self.cursor.fetchall()
        meat_ids_list = [i[0] for i in meat_ids]

        def insert_in_category_has_product(meat_product_id):
            """comment."""

            # Get beverage id in category table
            self.cursor.execute(sql_queries.SELECT_MEAT_CATEGORY_ID)
            meat_category_id = self.cursor.fetchone()[0]  # [0] returns "int" not tuple

            data_product_id = {'product_id': meat_product_id,
                               'category_id': meat_category_id,
                               }

            self.cursor.execute(sql_queries.INSERT_PRODUCT_CATEGORY, data_product_id)
            self.mydb.commit()

        for meat_product_id in meat_ids_list:
            insert_in_category_has_product(meat_product_id)

    def get_cheese_ids_list(self):
        # get all ids of products in product table with category name = Plats Préparés
        self.cursor.execute(sql_queries.SELECT_CHEESE_PRODUCT_ID)
        cheese_ids = self.cursor.fetchall()
        cheese_ids_list = [i[0] for i in cheese_ids]

        def insert_in_category_has_product(cheese_product_id):
            """comment."""

            # Get beverage id in category table
            self.cursor.execute(sql_queries.SELECT_CHEESE_CATEGORY_ID)
            cheese_category_id = self.cursor.fetchone()[0]  # [0] returns "int" not tuple

            data_product_id = {'product_id': cheese_product_id,
                               'category_id': cheese_category_id,
                               }

            self.cursor.execute(sql_queries.INSERT_PRODUCT_CATEGORY, data_product_id)
            self.mydb.commit()

        for cheese_product_id in cheese_ids_list:
            insert_in_category_has_product(cheese_product_id)

    def get_dessert_ids_list(self):
        # get all ids of products in product table with category name = Plats Préparés
        self.cursor.execute(sql_queries.SELECT_DESSERT_PRODUCT_ID)
        dessert_ids = self.cursor.fetchall()
        dessert_ids_list = [i[0] for i in dessert_ids]

        def insert_in_category_has_product(dessert_product_id):
            """comment."""

            # Get beverage id in category table
            self.cursor.execute(sql_queries.SELECT_DESSERT_CATEGORY_ID)
            dessert_category_id = self.cursor.fetchone()[0]  # [0] returns "int" not tuple

            data_product_id = {'product_id': dessert_product_id,
                               'category_id': dessert_category_id,
                               }

            self.cursor.execute(sql_queries.INSERT_PRODUCT_CATEGORY, data_product_id)
            self.mydb.commit()

        for dessert_product_id in dessert_ids_list:
            insert_in_category_has_product(dessert_product_id)


# ##########################################################################################################
#                                     << Execute
############################################################################################################

# """Execute class Create_empty_database"""
# create_new_database = Create_empty_database()
#
# """Execute class Category"""
# create_categories = Category()
#
# """Execute class Download_products"""
# download_products = Download_products()
#
# """Execute class Category_has_product"""
# fill_category_has_product = Category_has_product()

"""Execute class Category_has_product"""
display = Display()

# ##########################################################################################################
#                                     Execute >>
############################################################################################################
