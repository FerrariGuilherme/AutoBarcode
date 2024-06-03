from dependencias.database import bd

cod_comarca = bd.consultar_database("SELECT * FROM versionamento WHERE atual = 'True'")

print(cod_comarca[0][0])