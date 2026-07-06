# Databricks notebook source
#mi primer codigo en un servidor cloud
mensaje= "sistema coectado a la nube de databricks"
print(mensaje)

# COMMAND ----------

#importamos la libreria estrella de la ingeneria de datos
import pandas as pd

#definimos la ruta donde guardamos el archivo en la nube
ruta_archivo="/Volumes/workspace/default/datos/datos.csv"
#usamos Pandas para leer el csv y transformarlo en una tabla(dataframe)
df_martiza=pd.read_csv(ruta_archivo)
#display() es un comando especial de databricks para ver tablas de forma visual
display(df_martiza) 




# COMMAND ----------

#limpieza masiva de la columna estado
#1 str.strip() quita los espacios de toda la columna
#2 str.upper() convierte todo a mayusculas
df_martiza['estado']=df_martiza['estado'].str.strip().str.upper()
display(df_martiza)

# COMMAND ----------

#filtramos la tabla:traeme solo las filas donde el estado sea exactamente R
tabla_reposicion=df_martiza[df_martiza['estado']=='R']
#hacemos lo mismo para dejar listos L
tabla_dejar_listo=df_martiza[df_martiza['estado']=='L']
display(tabla_reposicion)
#la funcion lend() nos dice cuantas filas quedaron en estas tablas filtradas
total_R=len(tabla_reposicion)
total_L=len(tabla_dejar_listo)
print("total a reponer: ",total_R)
print("total a dejar listo: ",total_L)



# COMMAND ----------

import math
#definimos nuestra funcion matematica en la nube
def calcular_personal_necesaria(cantidad_deptos, capacidad_max):
    if cantidad_deptos==0:
        return 0
    elif cantidad_deptos==1:
        return 1
    else:
        #formula:redondeo hacia arriba(deptos/capacidad) + 1 persona base
        return math.ceil(cantidad_deptos/capacidad_max) + 1
print("funcion de calculo cargada en la memoria de cluster")

    


# COMMAND ----------

personal_R= calcular_personal_necesaria(total_R, 6)
personal_L= calcular_personal_necesaria(total_L, 8)
personal_total=personal_R+personal_L
print(f"--- CÁLCULO EN LA NUBE ---")
print (f"total a reponer:{total_R} deptos y se necesitan {personal_R} personas")
print (f"total a dejar listo:{total_L} deptos y se necesitan {personal_L} personas")
print (f"total de personas necesarias:{personal_total}")




# COMMAND ----------

#1. ocupamos nuestros resultados sueltos en un diccionario estructurado
datos_reporte={
    "tipo_limpieza":["Reposicion (R)", "Dejar listo (L)", "Total"],
    "departamentos_sucios": [total_R, total_L, total_R+total_L],
    "personal_a_contratar": [personal_R, personal_L, personal_total]
}
#2. Pandas convierte majicamente el diccionario en una tabla gerencial
df_reporte=pd.DataFrame(datos_reporte)
#3. Lo mostramos en pantalla
display(df_reporte)


# COMMAND ----------

#definimos la ruta de destino dentro de DataBricks (DBFS). Databricks file systems
ruta_salida="/Volumes/workspace/default/datos/reporte_final.csv"
#exportamos la tabla
#index=False es cruciar para pandas no guarde la columna de numeros (0,1,2)
df_reporte.to_csv(ruta_salida, index=False)
print(f"exito absoluto: el reporte oficial ha sido guardado en la ruta: {ruta_salida}")






# COMMAND ----------

