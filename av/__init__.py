"""
Модуль автоматического посещения занятий
"""

__version__ = '1.0.0'
__author__ = 'bonchara'

from av.auto_visit import System, db_connection
from av.main import App

__all__ = ['System', 'App', 'db_connection']
