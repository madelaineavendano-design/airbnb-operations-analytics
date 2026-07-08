# Databricks notebook source
#importamos todas las librerias necesarias
import pandas as pd
import math 
from datetime import datetime


# COMMAND ----------

#=================================================================
# 1. FUNCIÓN DE NEGOCIO Y FECHA DEL SISTEMA
# =================================================================
# Capturamos exactamente la fecha  de hoy en formato año-mes-dia
fecha_hoy=datetime.now().strftime("%Y-%m-%d")
#definimos nuestra funcion matematica en la nube
def calcular_personal_necesaria(cantidad_deptos, capacidad_max):
    if cantidad_deptos==0:
        return 0
    elif cantidad_deptos==1:
        return 1
    else:
        #formula:redondeo hacia arriba(deptos/capacidad) + 1 persona base
        return math.ceil(cantidad_deptos/capacidad_max) + 1

                                


# COMMAND ----------

# =================================================================
# 2. EXTRACCIÓN Y LIMPIEZA CON PANDAS
# =================================================================
#definimos la ruta donde guardamos el archivo en la nube
ruta_archivo="/Volumes/workspace/default/datos/datos.csv"
#usamos Pandas para leer el csv y transformarlo en una tabla(dataframe)
df_maritza=pd.read_csv(ruta_archivo)
#limpieza vectorizada
df_maritza['estado']= df_maritza['estado'].str.strip().str.upper()



# COMMAND ----------

# =================================================================
# 3. TRANSFORMACIÓN Y CÁLCULO
# =================================================================
#la funcion lend() nos dice cuantas filas quedaron en estas tablas filtradas
total_R=len(df_maritza[df_maritza['estado']=='R'])
total_L=len(df_maritza[df_maritza['estado']=='L'])
personal_R= calcular_personal_necesaria(total_R, 6)
personal_L= calcular_personal_necesaria(total_L, 8)
personal_total=personal_R+personal_L



# COMMAND ----------

# =================================================================
# 4. CARGA (LOAD) Y CREACIÓN DE REPORTE DINÁMICO
# =================================================================
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
#inyectamos la variable de la fecha en el nombre del archivo
ruta_salida= f"/Volumes/workspace/default/datos/reporte_{fecha_hoy}.csv"
df_reporte.to_csv(ruta_salida, index=False)
print(f"Exito: El reporte de hoy ha sido generado y guardado como: {ruta_salida}")


