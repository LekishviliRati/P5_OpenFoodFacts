# -*- coding: utf-8 -*-

import mysql.connector
import requests
import json
from database import Product
from configuration import globals, sql_queries


class Download_products:
    """
    Download products  from OpenFoodFacts API
    and insert them in local database.
    """

    def __init__(self):
        """Initiate Download_products class."""
        self.mydb = self.connect_to_database_p5_off()
        self.cursor = self.mydb.cursor()    # Creation of cursor.
        self.products_for_beverage()
        self.products_for_meal()
        self.products_for_meat()
        self.products_for_cheese()
        self.products_for_dessert()

    @staticmethod
    def connect_to_database_p5_off():
        """Connection to database."""
        mydb = mysql.connector.connect(
            host=globals.HOST,
            user=globals.USER,
            passwd=globals.PASSWORD,
            database=globals.DB_NAME
        )
        return mydb

    def products_for_beverage(self):
        """
        Download 50 most popular products,
        sold in beverage category in France.
        """
        request_beverage = requests.get(sql_queries.BEVERAGE_API_REQUEST)
        request_beverage_text = request_beverage.text
        data_beverage = json.loads(request_beverage_text)
        products_list = data_beverage["products"]
        # products_list is a dictionary.

        # Filter to avoid empty cases.
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

        # Renaming products fields.
        clean_products = []
        for product in products_no_empty_fields:
            product['product_name_fr'] = \
                product[
                    'product_name_fr'
                ].strip().lower().capitalize()  # string
            product['categories'] = \
                [name.strip().lower().capitalize()
                 for name in product[
                     'categories'
                 ].split(',')]  # list
            product['stores'] = \
                [store.strip().upper()
                 for store in product[
                     'stores'
                 ].split(',')]  # list
            product['nutrition_grade_fr'] = \
                product[
                    'nutrition_grade_fr'
                ].strip().upper()
            clean_products.append(product)

        # List of  clean products, will be used to insert product in database.
        final_products = []
        for one_product_dict in clean_products:
            my_product = Product(one_product_dict)
            final_products.append(my_product)

        def insert_product(one_product):
            """Insert products in Database."""

            # Match of 'one_product' attributes and database columns.
            data_product = {'name': one_product.name,
                            'description': one_product.description,
                            'grade': one_product.grade,
                            'brand': one_product.brands,
                            'store': one_product.stores[0],
                            # download first store in stores list
                            'url': one_product.url,
                            'category': globals.category_field_beverage,
                            }
            try:
                self.cursor.execute(sql_queries.INSERT_PRODUCTS, data_product)
                self.mydb.commit()
            except self.mydb.Error as err:
                print(f"Erreur lors de l'insertion des boissons'. "
                      f"Détails de l'erreur : {err}")

        for one_product in final_products:
            insert_product(one_product)

    def products_for_meal(self):
        """
        Download 50 most popular products,
        sold in meal category in France.
        """
        request_meal = requests.get(sql_queries.MEAL_API_REQUEST)
        request_meal_text = request_meal.text
        data_meal = json.loads(request_meal_text)
        products_list = data_meal["products"]
        # products_list = list de dictionnaires

        # Filter to avoid empty cases.
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

        # Renaming products fields.
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

        # List of  clean products, will be used to insert product in database.
        final_products = []
        for one_product_dict in clean_products:
            my_product = Product(one_product_dict)
            final_products.append(my_product)

        def insert_product(one_product):
            """Insert products in Database."""

            # Match of 'one_product' attributes and database columns.
            data_product = {'name': one_product.name,
                            'description': one_product.description,
                            'grade': one_product.grade,
                            'brand': one_product.brands,
                            'store': one_product.stores[0],
                            # download first store in stores list
                            'url': one_product.url,
                            'category': globals.category_field_meal,
                            }

            try:
                self.cursor.execute(sql_queries.INSERT_PRODUCTS, data_product)
                self.mydb.commit()
            except self.mydb.Error as err:
                print(f"Erreur lors de l'insertion des plats préparés'. "
                      f"Détails de l'erreur : {err}")

        for one_product in final_products:
            insert_product(one_product)

    def products_for_meat(self):
        """
        Download 50 most popular products,
        sold in meat category in France.
        """
        request_meat = requests.get(sql_queries.MEAT_API_REQUEST)
        request_meat_text = request_meat.text
        data_meat = json.loads(request_meat_text)
        products_list = data_meat["products"]

        # Filter to avoid empty cases.
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

        # Renaming products fields.
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

        # List of  clean products, will be used to insert product in database.
        final_products = []
        for one_product_dict in clean_products:
            my_product = Product(one_product_dict)
            final_products.append(my_product)

        def insert_product(one_product):
            """Insert products in Database."""

            # Match of 'one_product' attributes and database columns.
            data_product = {'name': one_product.name,
                            'description': one_product.description,
                            'grade': one_product.grade,
                            'brand': one_product.brands,
                            'store': one_product.stores[0],
                            # download first store in stores list
                            'url': one_product.url,
                            'category': globals.category_field_meat,
                            }

            try:
                self.cursor.execute(sql_queries.INSERT_PRODUCTS, data_product)
                self.mydb.commit()
            except self.mydb.Error as err:
                print(f"Erreur lors de l'insertion des viandes'. "
                      f"Détails de l'erreur : {err}")

        for one_product in final_products:
            insert_product(one_product)

    def products_for_cheese(self):
        """
        Download 50 most popular products,
        sold in cheese category in France.
        """
        request_cheese = requests.get(sql_queries.CHEESE_API_REQUEST)
        request_cheese_text = request_cheese.text
        data_cheese = json.loads(request_cheese_text)
        products_list = data_cheese["products"]

        # Filter to avoid empty cases.
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

        # Renaming products fields.
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

        # List of  clean products, will be used to insert product in database.
        final_products = []
        for one_product_dict in clean_products:
            my_product = Product(one_product_dict)
            final_products.append(my_product)

        def insert_product(one_product):
            """Insert products in Database."""

            # Match of 'one_product' attributes and database columns.
            data_product = {'name': one_product.name,
                            'description': one_product.description,
                            'grade': one_product.grade,
                            'brand': one_product.brands,
                            'store': one_product.stores[0],
                            # download first store in stores list
                            'url': one_product.url,
                            'category': globals.category_field_cheese,
                            }

            try:
                self.cursor.execute(sql_queries.INSERT_PRODUCTS, data_product)
                self.mydb.commit()
            except self.mydb.Error as err:
                print(f"Erreur lors de l'insertion des fromages'. "
                      f"Détails de l'erreur : {err}")

        for one_product in final_products:
            insert_product(one_product)

    def products_for_dessert(self):
        """
        Download 50 most popular products,
        sold in dessert category in France.
        """
        request_dessert = requests.get(sql_queries.DESSERT_API_REQUEST)
        request_dessert_text = request_dessert.text
        data_dessert = json.loads(request_dessert_text)
        products_list = data_dessert["products"]

        # Filter to avoid empty cases.
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

        # Renaming products fields.
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

        # List of  clean products, will be used to insert product in database.
        final_products = []
        for one_product_dict in clean_products:
            my_product = Product(one_product_dict)
            final_products.append(my_product)

        def insert_product(one_product):
            """Insert products in Database."""

            # Match of 'one_product' attributes and database columns.
            data_product = {'name': one_product.name,
                            'description': one_product.description,
                            'grade': one_product.grade,
                            'brand': one_product.brands,
                            'store': one_product.stores[0],
                            # download first store in stores list
                            'url': one_product.url,
                            'category': globals.category_field_dessert,
                            }

            try:
                self.cursor.execute(sql_queries.INSERT_PRODUCTS, data_product)
                self.mydb.commit()
            except self.mydb.Error as err:
                print(f"Erreur lors de l'insertion des desserts'. "
                      f"Détails de l'erreur : {err}")

        for one_product in final_products:
            insert_product(one_product)
