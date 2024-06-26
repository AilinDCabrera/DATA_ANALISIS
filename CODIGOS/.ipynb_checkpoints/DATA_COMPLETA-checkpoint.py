from pathlib import Path
import numpy as np
import pandas as pd

def completar_data(path_pre, lista_files, rango_tiempo, var):

    '''Completa las fechas faltantes del conjunto de datos'''

    tiempo_ini = rango_tiempo[0]
    tiempo_fin  = rango_tiempo[1]
    
    Path(f'../{var}_SALIDAS/DATA_COMPLETA_SIN_DEPURAR').mkdir(parents=True, exist_ok=True)

    dia_completo = [d.strftime('%Y-%m-%d') for d in pd.date_range(tiempo_ini, tiempo_fin, freq='1D')]
    tiempo = pd.DataFrame(dia_completo, columns = ['Fecha'])
    tiempo = tiempo.set_index('Fecha');tiempo.index = pd.to_datetime(tiempo.index)
    
    for i in np.arange(0,len(lista_files),1):
        print(lista_files[i])
        data = pd.read_csv(path_pre + lista_files[i])
        data = data[['Fecha', 'Valor']]; data = data.set_index('Fecha'); data.index = pd.to_datetime(data.index)
        data = data.loc[tiempo_ini:tiempo_fin]
        
        salida = pd.concat([data, tiempo], axis=1)
        salida.to_csv(f'../{var}_SALIDAS/DATA_COMPLETA_SIN_DEPURAR/{lista_files[i]}')