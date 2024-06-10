from dependencias.database import bd

a = bd.consultar_database(f"SELECT comarca FROM 'sistema.comarca' WHERE comarca_text = '{"0014 - Capital / Execuções Fiscais Estaduais"}'")[0][0]

print(a)

