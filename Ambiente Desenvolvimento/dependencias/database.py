import sqlite3
import cryptocode
from dependencias.apotamento_ambiente import aponta_database

class BancoDeDados:
    def __init__(self, database):
        self.database = database
        
    def alterar_database(self, query):
        banco = sqlite3.connect(self.database)
        cursor = banco.cursor()
        cursor.execute(query)
        
        banco.commit()
        
    def consultar_database(self, query):
            banco = sqlite3.connect(self.database)
            cursor = banco.cursor()
            cursor.execute(query)
            
            return cursor.fetchall()
            
bd = BancoDeDados(aponta_database)