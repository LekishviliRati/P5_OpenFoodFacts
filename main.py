# -*- coding: utf-8 -*-

import mysql.connector
# import Category  --> ne fontionne pas, le bon syntaxe : from Category import *
import requests
import json
from configuration import TABLES, globals


############################################################################################################
#                                    << CREATE EMPTY DATABASE
############################################################################################################

# """Connect to database"""
# my_db = mysql.connector.connect(
#     host=globals.HOST,
#     user=globals.USER,
#     passwd=globals.PASSWORD,
# )
#
# """Create a cursor on my_db"""
# cursor = my_db.cursor()
#
# req = 'CREATE database {}'.format(globals.DB_NAME)
# cursor.execute(req)
#
# cursor.execute(TABLES['category'])
# cursor.execute(TABLES['product'])
# cursor.execute(TABLES['category_has_product'])

############################################################################################################
#                                     CREATE EMPTY DATABASE >>
############################################################################################################

#####################################<< CLASSES  ###########################################################

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


class Product:
    """Comment."""

    def __init__(self):
        """Initiate Category Class."""
        self.mydb = self.connect_to_database_p5_off()
        self.cursor = self.mydb.cursor()
        self.products_for_boissons()
        # self.products_for_plats()
        # self.products_for_viandes()
        # self.products_for_fromages()
        # self.products_for_desserts()

    def connect_to_database_p5_off(self):
        """Connection to database and creates a cursor."""
        mydb = mysql.connector.connect(
            host=globals.HOST,
            user=globals.USER,
            passwd=globals.PASSWORD,
            database=globals.DB_NAME
        )
        return mydb

    def products_for_boissons(self):
        """Insert in database 50 most popular products sold in beverage category in France."""
        request_beverage = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0"
                                        "=categories&tag_contains_0=contains&tag_0=boissons&sort_by"
                                        "=unique_scans_n&page_size=50&json=true")
        request_beverage_text = request_beverage.text
        data_beverage = json.loads(request_beverage_text)
        # json.dump(data_beverage, open('data.json', "w"), indent=4)
        products_list_in_beverage_dict = data_beverage["products"]
        # print(type(products_list_in_beverage_dict))
        d = products_list_in_beverage_dict

        def is_key_present(x):
            if x in d:
                print(type(x))
            else:
                print("key is not in dictionnary")

        is_key_present("product_name_fr:")


# def products_for_plats(self):
#     """Insert 50 most popular products sold in dishes category in France."""
#     request_dishes = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0"
#                                     "=categories&tag_contains_0=contains&tag_0=plats_prepares&sort_by"
#                                     "=unique_scans_n&page_size=50&json=true")
#
# def products_for_viandes(self):
#     """Insert 50 most popular products sold in meat category in France."""
#     request_meat = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0"
#                                     "=categories&tag_contains_0=contains&tag_0=viandes&sort_by"
#                                     "=unique_scans_n&page_size=50&json=true")
#
# def products_for_fromages(self):
#     """Insert 50 most popular products sold in cheese category in France."""
#     request_cheese = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0"
#                                     "=categories&tag_contains_0=contains&tag_0=fromages&sort_by"
#                                     "=unique_scans_n&page_size=50&json=true")
#
# def products_for_desserts(self):
#     """Insert 50 most popular products sold in dessert category in France."""
#     request_dessert = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0"
#                                     "=categories&tag_contains_0=contains&tag_0=desserts&sort_by"
#                                     "=unique_scans_n&page_size=50&json=true")


#####################################  CLASSES >>#######################################################################


"""Execute class Category"""
# create_categories = Category()

"""Execute class Product"""
# Insert_products = Product()
