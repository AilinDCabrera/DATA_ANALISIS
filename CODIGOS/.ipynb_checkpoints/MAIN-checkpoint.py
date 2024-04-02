import pandas as pd
import numpy as np
import os
import sys

if __name__ == "__main__":
    '''Modulo principal para correr todos los códigos'''
    
    from DATA_LLENADO import llenado
    from DATA_COMPLETA import completar_data
    from GRAFICAR_DATOS_FALTANTES import datos_faltantes
    from GRAFICAR_CORRELACION import correlacion
    from CORRECCION_DATA import correccion
    from PRUEBA_HOMOGENEIDAD import test_pettitt
    from BOXPLOT import boxplots
    from MENSUAL_MULTIANUAL import mensual_multianual
    from CURVAS_DOBLE_MASA import curvas_doble_masa
    from BXP_COMPARACION import bxp_mes
    from BXP_COMPARACION import bxp_anio


    rango_tiempo = ['1995-01-01','2023-06-30']   #Fechas del periodo de tiempo a evaluar
    var = 'PRE'   # Variable a evaluar. Si es precipitación marcar como 'PRE', si es temperatura marcar como 'TEM'
    file_data = "../datos/"  #Carpeta de ubicación de los datos, cada estación en un csv por separado, el nombre del csv es el mismo de la estación
    
    lista_files = [i for i in os.listdir(file_data) if i != '.DS_Store']  #Seleccionar CSVs y excluir archivo oculto de macOS.
    
    llenado(file_data, lista_files,rango_tiempo,var)
    completar_data(file_data, lista_files,rango_tiempo,var)
    datos_faltantes(lista_files,rango_tiempo,var)
    correlacion(lista_files,rango_tiempo,var)
    correccion(lista_files,rango_tiempo,var) 
    test_pettitt(lista_files,var)
    boxplots(lista_files,var) 
    mensual_multianual(lista_files,'estaciones',var)
    mensual_multianual(lista_files,'global',var)
    curvas_doble_masa(lista_files) #Solo para precipitación
    bxp_mes(lista_files) #Solo para precipitación
    bxp_anio(lista_files) #Solo para precipitación