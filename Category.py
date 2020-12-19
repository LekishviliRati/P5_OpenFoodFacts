# -*- coding: utf-8 -*-

"""

"""

import mysql.connector
from configuration import globals


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