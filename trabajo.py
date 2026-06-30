import math
import csv
# =======================================================
# 1. NUESTRAS FUNCIONES (Las herramientas)
# =======================================================
def calcular_personal_necesario(cantidad_deptos, capacidad_maxima):
    if cantidad_deptos==0:
        return 0
    elif cantidad_deptos==1:
        return 1
    else :
        #math.ceil redondea hacia arriba, +1 persona base
        return math.ceil(cantidad_deptos/capacidad_maxima)+1
# =======================================================
# 2.EXTRACCION DE DATOS (LEYENDO DESDE ARCHIVO EXTERNO) 
# =======================================================  
#estado:"o"= ocupado, "r"= reposicion, "l"= dejar limpio
estado_deptos={}
# abrimos la puerta al archivo externo
with open ("datos1.csv", mode="r", encoding="utf-8") as archivo:
    #csv.DictReader lee la primera fila como nombres de las comlumnas
    lector=csv.DictReader(archivo)
    #recorremos el archivo fila por fila
    for fila in lector:
        depto= fila["departamento"].strip()
        #limpieza intensiva de la columna estado
        estado= fila["estado"].upper().strip()
        #listas de estados autorizados para el negocio
        estados_validos= ["R", "L", "O"]
        if estado in estados_validos:
            estado_deptos[depto]= estado
        else: 
            print(f"advertincia: el departamento {depto} tiene un estado invalido ('{estado} ')ignorando fila")
print (estado_deptos)        
# =======================================================
# 3. LÓGICA DE CLASIFICACIÓN (El motor)
# =======================================================
total_reposicion=0
total_dejar_listo=0
#el bucle revisa y clasifica cada depto
for depto, estado in estado_deptos.items():
    if estado== "R":
        total_reposicion=total_reposicion+1
    elif estado== "L":
        total_dejar_listo+=1
# =======================================================
# 4. CÁLCULO Y RESULTADOS (Usando nuestra función)
# =======================================================
print(f"Total deptos con reposicion: {total_reposicion} y Total deptos dejar listos: { total_dejar_listo}")
# Llamamos a nuestra función dos veces enviándole parámetros diferentes
personal_r= calcular_personal_necesario(total_reposicion, 6)
personal_l= calcular_personal_necesario(total_dejar_listo, 8)
personal_total= personal_l+ personal_r
#creamos una variable con el texto completo del reporte
reporte_final= f"""
=========================================
      REPORTE DIARIO DE LOGÍSTICA
=========================================
Departamentos reposicion: {total_reposicion} (requiere {personal_r} personas)
Departamentos dejar listos: {total_dejar_listo} (requiere {personal_l} personas)
-----------------------------------------
TOTAL DE TRABAJADORES PARA MAÑANA: {personal_total}
=========================================
"""
print(reporte_final)
print("\n--- REPORTE AUTOMÁTICO DE LOGÍSTICA ---")
print(f"Departamentos Reposición: {total_reposicion} -> Personal: {personal_r} personas.")
print(f"Departamentos Dejar Listo: {total_dejar_listo} -> Personal: {personal_l} personas.")
#print(f"TOTAL DE TRABAJADORES PARA MAÑANA:")
# =======================================================
# 5. GENERACIÓN DEL ARCHIVO (CARGA DE DATOS)
# =======================================================
with open("reporte_para_maritza.txt", mode= "w", encoding= "utf-8") as archivo_salida:
    archivo_salida.write(reporte_final)
print("exito: el archivo 'reporte_para_maritza.txt' ha sido creado con exito" )
