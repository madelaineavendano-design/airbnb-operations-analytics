import math

#estado:"o"= ocupado, "r"= reposicion, "l"= dejar limpio
estado_deptos= {
    "102": "r", "118":"o", "123":"l", "147":"o", "156":"r", "160":"r", "161":"r", "162":"r",  "163":"r", "164":"r" 

}
total_reposicion=0
total_dejar_listo=0
#el bucle revisa y clasifica cada depto
for depto, estado in estado_deptos.items():
    if estado== "r":
        total_reposicion=total_reposicion+1
    elif estado== "l":
        total_dejar_listo+=1
print(f"Total deptos con reposicion: {total_reposicion} y Total deptos dejar listos: { total_dejar_listo}")
 #algoritmo del personal para dejar listo (capacidad max=8) 
if total_dejar_listo==0:
    personal_l=0
elif total_dejar_listo==1:
    personal_l=1 
else:
    personal_l= math.ceil (total_dejar_listo /8)+1

#algoritmo del personal para reposicion (capacidad max=6)
if total_reposicion==0:
    personal_r=0
elif total_reposicion==1:
    personal_r=1 
else:
    # si hay entre 2 y 6 deptos, math.ceil da 1. mas 1 base = 2 personas
    # si hay 7 deptos, math.ceil da 2. mas 1 de base = 3 personas
    personal_r= math.ceil (total_reposicion /6)+1

print("\n--- REPORTE AUTOMÁTICO DE LOGÍSTICA ---")
print(f"Departamentos Reposición: {total_reposicion} -> Personal: {personal_r} personas.")
print(f"Departamentos Dejar Listo: {total_dejar_listo} -> Personal: {personal_l} personas.")
#print(f"TOTAL DE TRABAJADORES PARA MAÑANA:")