# -*- coding: utf-8 -*-
"""Create new empty database (without downloaded products in it)."""

import mysql.connector
from configuration import TABLES, globals, sql_queries


class Create_empty_database:
    """Create empty database."""

    def __init__(self):
        """Initiate Create empty database Class."""
        self.mydb = self.connect_to_database()
        self.cursor = self.mydb.cursor()    # Creation of cursor.
        self.create_new_database()
        self.insert_categories()

    @staticmethod
    def connect_to_database():
        """Connection to database."""
        mydb = mysql.connector.connect(
            host=globals.HOST,
            user=globals.USER,
            passwd=globals.PASSWORD,
        )
        return mydb

    def create_new_database(self):
        """Create tables of new database."""
        try:
            req = sql_queries.CREATE_NEW_DATABASE
            self.cursor.execute(req)
            self.cursor.execute(TABLES['category'])
            self.cursor.execute(TABLES['product'])
            self.cursor.execute(TABLES['category_has_product'])

        except mysql.connector.Error as err:
            print(f"Erreur lors de l'exécution de 'create_new_database'. "
                  f"Détails de l'erreur : {err}")

    def insert_categories(self):
        """Insert categories names in database p5_off."""

        try:
            self.cursor.execute(sql_queries.USE_DATABASE)
            data = [
                (globals.CATEGORIES[0],),
                (globals.CATEGORIES[1],),
                (globals.CATEGORIES[2],),
                (globals.CATEGORIES[3],),
                (globals.CATEGORIES[4],),
            ]

            self.cursor.executemany(sql_queries.INITIALISE_CATEGORIES_NAMES,
                                    data
                                    )
            self.mydb.commit()

        except mysql.connector.Error as err:
            print(f"Erreur lors de l'exécution de 'insert_categories'. "
                  f"Détails de l'erreur : {err}")
