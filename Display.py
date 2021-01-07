# -*- coding: utf-8 -*-

import mysql.connector
import requests
from configuration import TABLES, globals, sql_queries
from main import *
from configuration import TABLES, globals, sql_queries


class Display:
    """Manages Display"""

    def __init__(self):
        """Initiate Category Class."""
        self.mydb = self.connect_to_database_p5_off()
        self.cursor = self.mydb.cursor()
        self.display_menu()

    def connect_to_database_p5_off(self):
        """Connection to database and creates a cursor."""
        mydb = mysql.connector.connect(
            host=globals.HOST,
            user=globals.USER,
            passwd=globals.PASSWORD,
            database=globals.DB_NAME
        )
        return mydb

    def display_menu(self):
        """Display home page"""

        print("\n*** MENU PRINCIPAL ***")
        print("\n"
              "1 > Rechercher un produit de substitution.\n"
              "2 > Consulter mes favoris.\n"
              "3 > Restaurer ma liste de favoris.\n"
              "4 > Initialiser ou Réinitialiser la base de données.\n"
              "Q > Quitter le programme.\n")

        home_page_answer = input(
            "Veuillez sélectionnez votre choix : "
        )

        if home_page_answer.upper() == "Q":
            self.quit_program()
        elif home_page_answer == "1":
            self.display_categories()
            # self.display_menu()
        elif home_page_answer == "2":
            self.display_favorite_list()
            # self.display_menu()
        elif home_page_answer == "3":
            self.clean_favorite_list()
        #     self.display_menu()
        # elif home_page_answer == "4":
        #     self.quit_program()
        else:
            print(
                "Désolé ! Je n'ai pas compris votre choix... \n"
            )

            self.display_menu()

    def quit_program(self):
        """This function closes the program."""

        print("A bientôt")

    def display_categories(self):
        """This function displays categories."""

        self.cursor.execute(sql_queries.SELECT_CATEGORIES)
        categories = self.cursor.fetchall()
        category_ids_list = []

        print("\n*** CATEGORIES *** \n")
        for category in categories:
            print(
                f"{category[0]} > {category[1]}"
            )

        for i, category in categories:
            category_ids_list.append(str(i))

        print("\n"
              "[M] Retour au menu principal.\n"
              "[Q] Quitter le programme. \n"
              )

        self.category_choice(category_ids_list)

    def category_choice(self, category_ids_list):
        """Allows user to select a category."""

        category_answer = input("Veuillez sélectionner une catégorie : ")

        if category_answer in category_ids_list:  # rep is a str
            self.products_by_category(category_answer)
        elif category_answer.upper() == "M":
            self.display_menu()
        elif category_answer.upper() == "Q":
            self.quit_program()
        else:
            print(
                "Désolé, je n'ai pas compris votre choix... "
            )
            self.category_choice(category_ids_list)

    def products_by_category(self, category_answer):
        """Displays products by chosen category"""

        products_list = []
        self.cursor.execute(sql_queries.SELECT_UNHEALTHY_PRODUCTS_FROM_CATEGORY, (category_answer,))
        products_result = self.cursor.fetchall()
        print("\n*** PRODUITS A EVITER *** \n")
        for product in products_result:
            print(f"----- \n"
                  f"IDENTIFIANT: {product[0]}\n"
                  f"NOM: {product[1]}\n"
                  f"DESCRIPTION: {product[2]}\n"
                  f"NUTRI-SCORE: {product[3]}\n"
                  f"MARQUE: {product[4]}\n"
                  f"MAGASIN: {product[5]}\n"
                  f"URL: {product[6]}\n")

        # products_list will be used to display substitutes
        for product in products_result:
            products_list.append(str(product[0]))

        print("\n"
              "[M] Retour au menu principal.\n"
              "[Q] Quitter le programme. \n"
              )

        self.select_product(products_list)

    def select_product(self, products_list):
        """Allows to select a product"""

        select_product_answer = input("Choisissez un produit en entrant l'identifiant : ")

        if select_product_answer in products_list:
            self.find_substitute(select_product_answer)
        elif select_product_answer.upper() == "M":
            self.display_menu()
        elif select_product_answer.upper() == "Q":
            self.quit_program()
        else:
            print("Désolé, je n'ai pas compris votre choix...")
            self.select_product(products_list)

            print(
                  "[M] Retour au menu principal.\n"
                  "[Q] Quitter le programme. \n"
                  )

    def find_substitute(self, selected_product_id):
        """Finds healthier substitutes."""

        print("\n *** LISTE DE SUBSTITUTS *** \n ")

        # Get grade and category of selected unhealthy product
        self.cursor.execute(sql_queries.PRODUCT_TO_SUBSTITUTE, (selected_product_id,))
        product_to_substitute = self.cursor.fetchall()
        product_to_substitute_grade = [i[0] for i in product_to_substitute]
        product_to_substitute_category = [i[1] for i in product_to_substitute]

        # String variables needed to execute next research in database
        str_substitute_grade = " "
        str_substitute_category = " "

        str_substitute_grade = str_substitute_grade.join(product_to_substitute_grade)
        str_substitute_category = str_substitute_category.join(product_to_substitute_category)

        self.cursor.execute(sql_queries.SELECT_SUBSTITUTES, (str_substitute_category, str_substitute_grade))
        product_to_substitute_list = self.cursor.fetchall()

        # Print substitutes
        for product in product_to_substitute_list:
            print(f"--- Substitut ---\n"
                  f"IDENTIFIANT: {product[0]}\n"
                  f"NOM PRODUIT: {product[1]}\n"
                  f"DESCRIPTION: {product[2]}\n"
                  f"NUTRISCORE: {product[3]}\n"
                  f"MARQUE: {product[4]}\n"
                  f"MAGASIN: {product[5]}\n"
                  f"URL: {product[6]}\n")

            print(
                  "[M] Retour au menu principal.\n"
                  "[Q] Quitter le programme.\n"
                  )

        substitute_answer = input("Choisissez un substitut en entrant l'identifiant : ")

        substitutes_id_list = []

        for substitute in product_to_substitute_list:
            substitutes_id_list.append(str(substitute[0]))

        if substitute_answer in substitutes_id_list:
            self.display_substitute(substitute_answer)
        elif substitute_answer.upper() == "M":
            self.display_menu()
        elif substitute_answer.upper() == "Q":
            self.quit_program()
        else:
            print(
                "Désolé, je n'ai pas compris votre choix... "
            )
            self.find_substitute(selected_product_id)

    def display_substitute(self, substitute_answer):
        """Displays selected substitute."""

        self.cursor.execute(sql_queries.SELECT_SUBSTITUTE, (substitute_answer,))
        selected_substitute = self.cursor.fetchone()

        print("\n*** SUBSTITUT CHOISI ***\n")

        print(
            f"IDENTIFIANT........: {selected_substitute[0]}\n"
            f"NOM PRODUIT........: {selected_substitute[1]}\n"
            f"DESCRIPTION........: {selected_substitute[2]}\n"
            f"NUTRISCORE ........: {selected_substitute[3]}\n"
            f"MARQUE ............: {selected_substitute[4]}\n"
            f"MAGASIN ...........: {selected_substitute[5]}\n"
            f"URL ...............: {selected_substitute[6]}\n"
        )

        self.switch_to_favorite(selected_substitute)

    def switch_to_favorite(self, selected_substitute):
        """Allows user to define selected product as favorite."""

        # Will be used to change selected substitute into favorite
        selected_substitute_id = selected_substitute[0]

        print("\n --- DERNIERE ETAPE ---"
              "\nQue souhaitez-vous faire ?\n\n"
              "[S] - Sauvegarder le substitut.\n"
              "[M] Retour au menu principal.\n"
              "[Q] Quitter le programme.\n")

        favorite_answer = input("Veuillez indiquer votre choix : ")

        if favorite_answer.upper() == "S":
            self.cursor.execute(sql_queries.UPDATE_TO_FAVORITE, (selected_substitute_id,))
            self.mydb.commit()
            print("\nVotre substitut a été ajouté à vos favoris.")
            self.display_menu()
        elif favorite_answer.upper() == "M":
            self.display_menu()
        elif favorite_answer.upper() == "Q":
            self.quit_program()
        else:
            print(
                "Désolé ! Je n'ai pas compris votre choix... "
            )
            self.switch_to_favorite(selected_substitute)

    def display_favorite_list(self):
        """Displays favorite list."""

        self.cursor.execute(sql_queries.SELECT_FAVORITE)
        favorite_list = self.cursor.fetchall()

        print(
            "\n*** FAVORIS *** \n "
        )

        for favorite in favorite_list:
            print("--- Favoris ---\n"
                  f"IDENTIFIANT........: {favorite[0]}\n"
                  f"NOM SUBSTITUT......: {favorite[1]}\n"
                  f"NUTRISCORE.........: {favorite[2]}\n"
                  f"CODE BARRE.........: {favorite[3]}\n"
                  f"MARQUE.............: {favorite[4]}\n"
                  f"URL................: {favorite[5]}\n"
                  f"LIEU(X) DE VENTE...: {favorite[6]}\n")

        favorite_id_list = []
        for favorite_id in favorite_list:
            favorite_id_list.append(str(favorite_id[0]))

        print("\n"
              "[M] Retour au menu principal.\n"
              "[Q] Quitter le programme. \n"
              )

        self.select_favorite_product(favorite_id_list)

    def select_favorite_product(self, favorite_id_list):
        """Allows to select a product in favorite list."""

        select_from_product_favorite_list = input(
            "Choisissez un produit en entrant l'identifiant : "
        )

        if select_from_product_favorite_list in favorite_id_list:
            self.display_substitute_from_favorite_list(select_from_product_favorite_list)
        elif select_from_product_favorite_list.upper() == "M":
            self.display_menu()
        elif select_from_product_favorite_list.upper() == "Q":
            self.quit_program()
        else:
            print("Désolé, je n'ai pas compris votre choix...")
            self.select_product(favorite_id_list)

    def display_substitute_from_favorite_list(self, select_from_product_favorite_list):
        """Displays product chosen from favorite list."""

        self.cursor.execute(sql_queries.SELECT_SUBSTITUTE, (select_from_product_favorite_list,))
        selected_substitute = self.cursor.fetchone()

        print("\n*** SUBSTITUT CHOISI ***\n")

        print(
            f"IDENTIFIANT........: {selected_substitute[0]}\n"
            f"NOM PRODUIT........: {selected_substitute[1]}\n"
            f"DESCRIPTION........: {selected_substitute[2]}\n"
            f"NUTRISCORE ........: {selected_substitute[3]}\n"
            f"MARQUE ............: {selected_substitute[4]}\n"
            f"MAGASIN ...........: {selected_substitute[5]}\n"
            f"URL ...............: {selected_substitute[6]}\n"
        )

        self.switch_to_non_favorite(selected_substitute)

    def switch_to_non_favorite(self, selected_substitute):
        """Allows user to set selected product as non-favorite."""

        # Will be used to change selected substitute into favorite
        selected_substitute_id = selected_substitute[0]

        print(
              "\nQue souhaitez-vous faire ?\n\n"
              "[S] - Supprimer de la liste des favoris.\n"
              "[M] Retour au menu principal.\n"
              "[Q] Quitter le programme.\n")

        answer = input("Veuillez indiquer votre choix : ")

        if answer.upper() == "S":
            self.cursor.execute(sql_queries.UPDATE_TO_NON_FAVORITE, (selected_substitute_id,))
            self.mydb.commit()
            print("\nVotre substitut a été retiré à vos favoris.")
            self.display_menu()
        elif answer.upper() == "M":
            self.display_menu()
        elif answer.upper() == "Q":
            self.quit_program()
        else:
            print(
                "Désolé ! Je n'ai pas compris votre choix... "
            )
            self.switch_to_non_favorite(selected_substitute)

    def clean_favorite_list(self):
        """Allows to delete all products from favorite list"""

        self.cursor.execute(sql_queries.CLEAN_FAVORITE_LIST)

        print("\nVous venez de nettoyer la liste des favoris.\n")

        print("\n"
              "[M] Retour au menu principal.\n"
              "[Q] Quitter le programme. \n"
              )

        answer = input("Que souhaitez vous faire : ")

        if answer.upper() == "M":
            self.display_menu()
        elif answer.upper() == "Q":
            self.quit_program()


test = Display()
###############
