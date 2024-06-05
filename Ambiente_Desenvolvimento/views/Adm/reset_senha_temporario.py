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
            
bd = BancoDeDados("\\\\10.16.96.144\\novo_auto_barcode\\database\\database_producao.sqlite")


while True:
    try:
        idUsuario = int(input("ID do usuario: "))
        novaSenha = input("Nova senha: ")
        novaSenha = cryptocode.encrypt(f"{novaSenha}", "Pge@123")
        break
    
    except:
        print()
        print("Campo invalilido")
        print()
        
bd.alterar_database(f"""UPDATE users SET password = '{novaSenha}', reset_senha = 'True' WHERE id = {idUsuario}""")

print()
print("Senha alterada com sucesso!!")
print()
print()
