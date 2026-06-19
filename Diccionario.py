#diccionario:"departamento": "dias ocupados"
estado_deptos={
    "102":0 ,
    "118":3 ,
    "123":0 ,
    "147":1 ,
    "156":0 ,
}
print("--- INICIANDO algoritmo de limpieza ---")
total_limpiezas=0  
#.items() nos permite sacar tanto el nombre (depto) como el numero (dia)
for depto, dias in estado_deptos.items():
    if dias==0:
        print(f"alerta roja: el depto {depto} debe limpiarse hoy de 12hrs a 15hrs")
        total_limpiezas=total_limpiezas+1 #aqui sumamos 1
    else:
        print(f"el depto {depto} sigue ocupado por {dias} dias mas. ignorar")
print("--- RESUMEN DEL DIA ---")
print(f"el total de deptos a limpiar hoy: {total_limpiezas}")
