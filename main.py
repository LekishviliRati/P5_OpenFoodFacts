# -*- coding: utf-8 -*-

import mysql.connector
# import Category  --> ne fontionne pas, le bon syntaxe : from Category import *
from Product import *
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


############################################################################################################
#                                    << DOWNLOAD PRODUCTS CLASS
############################################################################################################

class Download_products:
    """Comment."""

    def __init__(self):
        """Initiate Category Class."""
        self.mydb = self.connect_to_database_p5_off()
        self.cursor = self.mydb.cursor()
        self.products_for_boissons()

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

        # for one_product in final_products:
        #     # print(one_product.url)
        #     insert_product(one_product)

        ############  <<  REMPLIR LA TABLE CATGEROY_HAS_PRODUCT

        # get all ids of products in product table with category name = beverage
        self.cursor.execute("SELECT id FROM product where category = 'Boissons';")  # Ce n'est plus Beverage
        beverage_ids = self.cursor.fetchall()  # list of tuples
        beverage_ids_list = [i[0] for i in beverage_ids]  # transform list of tuples into list of integers

        print(beverage_ids_list)

        # insert in table category_has_product
        def insert_in_category_has_product(beverage_product_id):
            """comment."""

            # Get beverage id in category table
            self.cursor.execute(sql_queries.SELECT_BEVERAGE_CATEGORY_ID)
            beverage_category_id = self.cursor.fetchone()[0]     # [0] returns "int" not tuple

            data_product_id = {'product_id': beverage_product_id,
                               'category_id': beverage_category_id,
                               }

            self.cursor.execute(sql_queries.INSERT_PRODUCT_CATEGORY, data_product_id)
            self.mydb.commit()

        # for beverage_product_id in beverage_ids_list:
        #     insert_in_category_has_product(beverage_product_id)

        ############  ça ofnctionne, insert les id dans la table de laison >>


        ########### Esai pour requête left join

        # self.cursor.execute("SELECT product.id, product.name FROM product "
        #                     "LEFT JOIN category_has_product "
        #                     "ON"
        #                     "product.id = category_has_product.product_id "
        #                     "RIGHT JOIN category "
        #                     "ON "
        #                     "category.id = category_has_product.category_id "
        #                     "WHERE category.id = 1 "
        #                     "GROUP BY product.id;"
        #                     )

        # Get beverage ID in Tuple not integer
        self.cursor.execute(sql_queries.SELECT_BEVERAGE_CATEGORY_ID)
        beverage_category_id_tuple = self.cursor.fetchone()

        # Utiliser LEFT JOIN / RIGHT JOIN pour aller chercher les produits en fonction la catégorie Boissons
        self.cursor.execute(sql_queries.SELECT_PRODUCTS_FROM_CATEGORY, beverage_category_id_tuple)
        product_id = self.cursor.fetchall()  # list of tuples
        product_ids_list = [i[0] for i in product_id]  # transform list of tuples into list of integers
        print(product_ids_list)


# def insert_ids_in_category_has_product(one_product_id):
#     """This function will insert product ID in table category has product"""
#
#     data_product_id = {'product_id': one_product_id.id,
#                        'category_id': 1
#                        }
#
#     self.cursor.execute(sql_queries.INSERT_PRODUCT_CATEGORY, data_product_id)
#     self.mydb.commit()
#
# for product_id in final_products:
#     product_id = product_id.url
#     insert_ids_in_category_has_product(product_id)


############################################################################################################
#                                     DOWNLOAD PRODUCT CLASS >>
############################################################################################################


############################################################################################################
#                                     << read category_id
#############################################################################################################
# def connect_to_database_p5_off():
#     """Connection to database and creates a cursor."""
#     mydb = mysql.connector.connect(
#         host=globals.HOST,
#         user=globals.USER,
#         passwd=globals.PASSWORD,
#         database=globals.DB_NAME
#     )
#     return mydb
#
#
# mydb = connect_to_database_p5_off()
# cursor = mydb.cursor()
#
# cursor.execute(sql_queries.SELECT_BEVERAGE_CATEGORY_ID)
#
# beverage_category_id = cursor.fetchone()[0]     # [0] permet de retourner la premieère valeur "int" et non un tuple
# print(beverage_category_id)

# ###########################################################################################################
#                                     read category_id >>
#############################################################################################################


############################################################################################################
#                                    << API REQUESTS
############################################################################################################

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

############################################################################################################
#                                    API REQUESTS >>
############################################################################################################


# ###########################################################################################################
#                                     << Execute
#############################################################################################################

# """Execute class Create_empty_database"""
# create_new_database = Create_empty_database()
#
# """Execute class Category"""
# create_categories = Category()

"""Execute class Download_products"""
download_products = Download_products()

# ###########################################################################################################
#                                     Execute >>
#############################################################################################################
