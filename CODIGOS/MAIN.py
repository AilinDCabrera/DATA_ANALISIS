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
    from OUTLIERS import walsh_test
    from LLENADO_V2 import llenar_datos
    from TENDENCIA import mann_kendall


    rango_tiempo = ['1995-01-01','2023-06-30']   #Fechas del periodo de tiempo a evaluar
    var = 'PRE'   # Variable a evaluar. Si es precipitación marcar como 'PRE', si es temperatura marcar como 'TEM'
    file_data = "../datos/"  #Carpeta de ubicación de los datos, cada estación en un csv por separado, el nombre del csv es el mismo de la estación
    
    lista_files = [i for i in os.listdir(file_data) if i != '.DS_Store']  #Seleccionar CSVs y excluir archivo oculto de macOS.
    
    #llenado(file_data, lista_files,rango_tiempo,var)
    #completar_data(file_data, lista_files,rango_tiempo,var)
    #llenar_datos(lista_files)
    grafico_datos_faltantes = datos_faltantes(lista_files,rango_tiempo,var)
    grafico_correlacion     = correlacion(lista_files,rango_tiempo,var)
    walsh_test(lista_files,var)
    correccion(lista_files,rango_tiempo,var) 
    grafico_test_pettitt    = test_pettitt(lista_files,var)
    grafico_boxplots        = boxplots(lista_files,var) 
    grafico_mm_estaciones   = mensual_multianual(lista_files,'estaciones',var)
    grafico_mm_global       = mensual_multianual(lista_files,'global',var)
    grafico_c_doble_masa    = curvas_doble_masa(lista_files) #Solo para precipitación
    grafico_bxp_mes         = bxp_mes(lista_files) #Solo para precipitación
    grafico_bxp_anio        = bxp_anio(lista_files) #Solo para precipitación
    grafico_tendencia       = mann_kendall(lista_files,var)


