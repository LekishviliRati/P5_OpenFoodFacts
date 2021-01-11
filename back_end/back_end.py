# -*- coding: utf-8 -*-
"""
Manage :
- Creation of empty database
- Downloading data from OpenFoodFacts API.
- Insertion of data into database
"""

import mysql.connector
from database import Create_empty_database, Category_has_product
from data import Download_products
from configuration import globals


def init_database():
    """Initialise database if not exists yet."""

    try:
        mysql.connector.connect(
            host=globals.HOST,
            user=globals.USER,
            passwd=globals.PASSWORD,
            database=globals.DB_NAME
        )
        pass

    except Exception:
        Create_empty_database()
        Download_products()
        Category_has_product()
