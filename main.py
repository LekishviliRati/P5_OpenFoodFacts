# -*- coding: utf-8 -*-
"""Launch the application."""

from display import Display
from back_end import init_database

if __name__ == '__main__':
    init_database()
    display = Display()
    display.display_menu()
