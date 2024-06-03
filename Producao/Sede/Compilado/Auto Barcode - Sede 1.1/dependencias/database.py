import sqlite3
import cryptocode

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
            
bd = BancoDeDados("\\\\10.16.100.201\\Servidor_SCR\\Novo_AutoBarcode\\database\\database_producao_sede.sqlite")