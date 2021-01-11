# -*- coding: utf-8 -*-

class Product:
    """Intantiate products from a given list."""

    def __init__(self, clean_product):
        """Product fields."""
        self.name = clean_product['product_name_fr']
        self.description = clean_product['generic_name_fr']
        self.grade = clean_product['nutrition_grade_fr']
        self.brands = clean_product['brands']
        self.stores = clean_product['stores']
        self.url = clean_product['url']
