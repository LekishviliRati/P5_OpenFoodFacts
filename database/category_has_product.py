# -*- coding: utf-8 -*-
"""Link categories and products."""

import mysql.connector
from configuration import globals, sql_queries


class Category_has_product:
    """
    Insert category_id and product_id
    in category_has_product.
    """

    def __init__(self):
        """Initiate Category Class."""
        self.mydb = self.connect_to_database_p5_off()
        self.cursor = self.mydb.cursor()  # Creation of cursor.
        self.get_beverage_ids_list()
        self.get_meal_ids_list()
        self.get_meat_ids_list()
        self.get_cheese_ids_list()
        self.get_dessert_ids_list()

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

    def get_beverage_ids_list(self):
        """
        Get all ids of beverages in product table
        and insert them in category_has_product
        one by one with category Id.
        """

        def insert_in_category_has_product(beverage_product_id):
            """Insert products Ids in category_has_product."""
            try:
                # Get beverage id in category table
                self.cursor.execute(sql_queries.SELECT_BEVERAGE_CATEGORY_ID)
                beverage_category_id = self.cursor.fetchone()[0]
                # [0] returns "int" not tuple

                data_product_id = {'product_id': beverage_product_id,
                                   'category_id': beverage_category_id,
                                   }
                self.cursor.execute(sql_queries.INSERT_PRODUCT_CATEGORY,
                                    data_product_id)
                self.mydb.commit()

            except mysql.connector.Error as err:
                print(f"Erreur lors de l'execution de "
                      f"'insert_in_category_has_product'. "
                      f"Détails de l'erreur : {err}")

        try:
            # Select ids in product table.
            self.cursor.execute(sql_queries.SELECT_BEVERAGE_PRODUCT_ID)
            beverage_ids = self.cursor.fetchall()  # list of tuples
            beverage_ids_list = [i[0] for i in beverage_ids]
            # transform list of tuples into list of integers

            for beverage_product_id in beverage_ids_list:
                insert_in_category_has_product(beverage_product_id)

        except mysql.connector.Error as err:
            print(f"Erreur lors de l'exécution de 'get_beverage_ids_list'. "
                  f"Détails de l'erreur : {err}")

    def get_meal_ids_list(self):
        """
        Get all ids of meals in product table
        and insert them in category_has_product.
        """

        def insert_in_category_has_product(meal_product_id):
            """Insert products IDs in category_has_product."""
            try:
                self.cursor.execute(
                    sql_queries.SELECT_MEAL_CATEGORY_ID
                )
                meal_category_id = self.cursor.fetchone()[0]
                # [0] returns "int" not tuple

                data_product_id = {'product_id': meal_product_id,
                                   'category_id':
                                       meal_category_id,
                                   }
                self.cursor.execute(sql_queries.INSERT_PRODUCT_CATEGORY,
                                    data_product_id)
                self.mydb.commit()

            except mysql.connector.Error as err:
                print(f"Erreur lors de l'exécution de 'get_meal_ids_list'. "
                      f"Détails de l'erreur : {err}")

        try:
            # Select ids in product table.
            self.cursor.execute(sql_queries.SELECT_MEAL_PRODUCT_ID)
            meal_ids = self.cursor.fetchall()
            # list of tuples
            meal_ids_list = [i[0] for i in meal_ids]
            # transform list of tuples into list of integers

            for meal_product_id in meal_ids_list:
                insert_in_category_has_product(meal_product_id)

        except mysql.connector.Error as err:
            print(f"Erreur lors de l'exécution de 'get_meal_ids_list'. "
                  f"Détails de l'erreur : {err}")

    def get_meat_ids_list(self):
        """
        Get all ids of meats in product table
        and insert them in category_has_product.
        """

        def insert_in_category_has_product(meat_product_id):
            """
            Insert products IDs in category_has_product.
            """
            try:
                self.cursor.execute(sql_queries.SELECT_MEAT_CATEGORY_ID)
                meat_category_id = self.cursor.fetchone()[0]
                # [0] returns "int" not tuple

                data_product_id = {'product_id': meat_product_id,
                                   'category_id': meat_category_id,
                                   }
                self.cursor.execute(sql_queries.INSERT_PRODUCT_CATEGORY,
                                    data_product_id)
                self.mydb.commit()

            except mysql.connector.Error as err:
                print(f"Erreur lors de l'exécution de 'get_meat_ids_list'. "
                      f"Détails de l'erreur : {err}")

        try:
            # Select ids in product table.
            self.cursor.execute(sql_queries.SELECT_MEAT_PRODUCT_ID)
            meat_ids = self.cursor.fetchall()
            meat_ids_list = [i[0] for i in meat_ids]

            for meat_product_id in meat_ids_list:
                insert_in_category_has_product(meat_product_id)

        except mysql.connector.Error as err:
            print(f"Erreur lors de l'exécution de 'get_meat_ids_list'. "
                  f"Détails de l'erreur : {err}")

    def get_cheese_ids_list(self):
        """
        Get all ids of cheeses in product table
        and insert them in category_has_product.
        """

        def insert_in_category_has_product(cheese_product_id):
            """Insert products IDs in category_has_product."""
            try:
                self.cursor.execute(sql_queries.SELECT_CHEESE_CATEGORY_ID)
                cheese_category_id = self.cursor.fetchone()[0]
                # [0] returns "int" not tuple

                data_product_id = {'product_id': cheese_product_id,
                                   'category_id':
                                       cheese_category_id,
                                   }
                self.cursor.execute(sql_queries.INSERT_PRODUCT_CATEGORY,
                                    data_product_id)
                self.mydb.commit()

            except mysql.connector.Error as err:
                print(f"Erreur lors de l'exécution de 'get_cheese_ids_list'. "
                      f"Détails de l'erreur : {err}")

        try:
            # Select ids in product table.
            self.cursor.execute(sql_queries.SELECT_CHEESE_PRODUCT_ID)
            cheese_ids = self.cursor.fetchall()
            cheese_ids_list = [i[0] for i in cheese_ids]
            for cheese_product_id in cheese_ids_list:
                insert_in_category_has_product(cheese_product_id)

        except mysql.connector.Error as err:
            print(f"Erreur lors de l'exécution de 'get_cheese_ids_list'. "
                  f"Détails de l'erreur : {err}")

    def get_dessert_ids_list(self):
        """
        Get all ids of desserts in product table
        and insert them in category_has_product.
        """

        def insert_in_category_has_product(dessert_product_id):
            """Insert products IDs in category_has_product."""
            try:
                self.cursor.execute(sql_queries.SELECT_DESSERT_CATEGORY_ID)
                dessert_category_id = self.cursor.fetchone()[0]
                # [0] returns "int" not tuple

                data_product_id = {'product_id': dessert_product_id,
                                   'category_id': dessert_category_id,
                                   }
                self.cursor.execute(sql_queries.INSERT_PRODUCT_CATEGORY,
                                    data_product_id)
                self.mydb.commit()

            except mysql.connector.Error as err:
                print(f"Erreur lors de l'exécution de 'get_dessert_ids_list'. "
                      f"Détails de l'erreur : {err}")

        try:
            # Select ids in product table.
            self.cursor.execute(sql_queries.SELECT_DESSERT_PRODUCT_ID)
            dessert_ids = self.cursor.fetchall()
            dessert_ids_list = [i[0] for i in dessert_ids]

            for dessert_product_id in dessert_ids_list:
                insert_in_category_has_product(dessert_product_id)

        except mysql.connector.Error as err:
            print(f"Erreur lors de l'exécution de 'get_dessert_ids_list'. "
                  f"Détails de l'erreur : {err}")
