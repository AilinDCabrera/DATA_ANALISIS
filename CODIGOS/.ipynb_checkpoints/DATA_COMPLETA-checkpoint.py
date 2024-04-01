from pathlib import Path
import numpy as np
import pandas as pd

def completar_data(path_pre, lista_files, rango_tiempo, var):

    tiempo_ini = rango_tiempo[0]
    tiempo_fin  = rango_tiempo[1]
    
    Path(f'../{var}_SALIDAS/DATA_COMPLETA').mkdir(parents=True, exist_ok=True)

    dia_completo = [d.strftime('%Y-%m-%d') for d in pd.date_range(tiempo_ini, tiempo_fin, freq='1D')]
    tiempo = pd.DataFrame(dia_completo, columns = ['Fecha'])
    tiempo = tiempo.set_index('Fecha');tiempo.index = pd.to_datetime(tiempo.index)
    
    fecha_inicio = []
    fecha_fin    = []
    
    for i in np.arange(0,len(lista_files),1):
        print(lista_files[i])
        data = pd.read_csv(path_pre + lista_files[i])
        data = data[['Fecha', 'Valor']]; data = data.set_index('Fecha'); data.index = pd.to_datetime(data.index)
        data = data.loc[tiempo_ini:tiempo_fin]
        fecha_inicio = np.append(fecha_inicio,data.index[0].strftime('%Y-%m-%d'))
        fecha_fin    = np.append(fecha_fin,data.index[-1].strftime('%Y-%m-%d'))
        
        salida = pd.concat([data, tiempo], axis=1)
        salida.to_csv(f'../{var}_SALIDAS/DATA_COMPLETA/{lista_files[i]}')
        
    df_fechas = pd.DataFrame({'FECHA_INICIAL':fecha_inicio, 'FECHA_FINAL':fecha_fin})