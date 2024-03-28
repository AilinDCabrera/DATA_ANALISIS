from pathlib import Path
import numpy as np
import pandas as pd

def completar_data(path_pre, lista_files):
    
    # fecha_ini= '1995-01-01'
    # fecha_fin = '2023-06-30'
    
    # tiempo = pd.DataFrame(index=pd.date_range(fecha_ini, fecha_fin, freq='1D'))
    # tiempo.index.name = 'Fecha'; tiempo.index = pd.to_datetime(tiempo.index)

    año_ini = '1995'
    mes_ini = '01'
    dia_ini = '01'
    
    año_fin = '2023'
    mes_fin = '06'
    dia_fin = '30'
    
    Path('../PRE_SALIDAS/DATA_COMPLETA').mkdir(parents=True, exist_ok=True)

    dia_completo = [d.strftime('%Y-%m-%d') for d in pd.date_range(año_ini+ mes_ini + dia_ini, año_fin + mes_fin + dia_fin, freq='1D')]
    tiempo = pd.DataFrame(dia_completo, columns = ['Fecha'])
    tiempo = tiempo.set_index('Fecha');tiempo.index = pd.to_datetime(tiempo.index)

    # numi = 0
    # numf = len(lista_files)
    
    # nombres_estaciones_plot = [x[:-4] + '[' for x in lista_files]
    # nombres_estaciones_plot = [x[:x.index('[') + len('[')-1] for x in nombres_estaciones_plot]
    
    fecha_inicio = []
    fecha_fin    = []
    
    for i in np.arange(0,len(lista_files),1):
        print(lista_files[i])
        data = pd.read_csv(path_pre + lista_files[i])
        data = data[['Fecha', 'Valor']]; data = data.set_index('Fecha'); data.index = pd.to_datetime(data.index)
        data = data.loc[año_ini + '-' + mes_ini +  '-' + dia_ini: año_fin + '-' + mes_fin +  '-' + dia_fin]
        fecha_inicio = np.append(fecha_inicio,data.index[0].strftime('%Y-%m-%d'))
        fecha_fin    = np.append(fecha_fin,data.index[-1].strftime('%Y-%m-%d'))
        
        salida = pd.concat([data, tiempo], axis=1)
        salida.to_csv('../PRE_SALIDAS/DATA_COMPLETA/' + lista_files[i])
        
    df_fechas = pd.DataFrame({'FECHA_INICIAL':fecha_inicio, 'FECHA_FINAL':fecha_fin})