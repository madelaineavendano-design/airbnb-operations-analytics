# Databricks notebook source
# MAGIC %skip
# MAGIC %sql
# MAGIC --1. usamos el catalogo por defecto en tu workspace
# MAGIC USE CATALOG workspace;
# MAGIC --2. creamos un esquema exclusivo para el proyecto de maritza
# MAGIC CREATE SCHEMA IF NOT EXISTS operaciones_airbnb;
# MAGIC --3. creamos los volumenes para la arquitectura medallon
# MAGIC CREATE VOLUME IF NOT EXISTS operaciones_airbnb.bronze;
# MAGIC CREATE VOLUME IF NOT EXISTS operaciones_airbnb.silver;
# MAGIC CREATE VOLUME IF NOT EXISTS operaciones_airbnb.gold;
# MAGIC
# MAGIC
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

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
# 2. CAPA BRONZE (Datos crudos/raw)
# =================================================================
#el csv original se deposita aca
ruta_archivo="/Volumes/workspace/operaciones_airbnb/bronze/operaciones_historico_2025_2026.csv"
#extraemos el archivo crudo exactamente como viene
df_bronze=pd.read_csv(ruta_archivo)
#analisis exploratorio o eda
print("1. informacion estructural")
df_bronze.info()
#conteo de datos vacios por columna
print("2. conteo de datos nulos")
print(df_bronze.isnull().sum())
#conteo de los diferentes estados que se escribieron
print("3. conteo de estados")
print(df_bronze['estado'].value_counts(dropna=False))

      




# COMMAND ----------

# =================================================================
# 3. CAPA SILVER (DATOS LIMPIOS Y VALIDADOS)
# =================================================================
#Creamos una copia para no dañar los datos originales
df_silver=df_bronze.copy()
#A) limpieza estructural
#eliminar filas donde el 'estado' este vacio
df_silver.dropna(subset=['estado'], inplace=True)
#eliminar duplicados (mismo departamento en la misma fecha)
df_silver.drop_duplicates(subset=['departamento','fecha_operacion'], keep='last', inplace=True)
#limpieza vectorizada
df_silver['estado']= df_silver['estado'].str.strip().str.upper()
#filtramos solo lo que el negocio permite
df_silver=df_silver[df_silver['estado'].isin(['L','R', 'O'])]
ruta_silver="/Volumes/workspace/operaciones_airbnb/silver/datos_silver.parquet"
df_silver.to_parquet(ruta_silver, index=False)
print("datos procesados exitosamente hasta la capa silver")





# COMMAND ----------

# =================================================================
# 4. CAPA GOLD (Metricas de negocio y reportes)
# =================================================================
#contamos usando nuestra tabla limpia (silver)
#la funcion len() nos dice cuantas filas quedaron en estas tablas filtradas
total_R=len(df_silver[df_silver['estado']=='R'])
total_L=len(df_silver[df_silver['estado']=='L'])
#calculamos con la funcion de negocio ya cargada en memoria
personal_R= calcular_personal_necesaria(total_R, 6)
personal_L= calcular_personal_necesaria(total_L, 8)
personal_total=personal_R+personal_L
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
ruta_salida= f"/Volumes/workspace/operaciones_airbnb/gold/reporte_{fecha_hoy}.parquet"
df_reporte.to_parquet(ruta_salida, index=False)
print(f"Exito: El reporte gold ha sido generado y guardado como: {ruta_salida}")


