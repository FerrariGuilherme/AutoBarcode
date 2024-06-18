from dependencias.database import bd

print(len(bd.consultar_database(f"SELECT processo FROM 'processos.historico' WHERE processo = '0000000-00.0000.8.26.0045'")))

#print(a)

