from sklearn.impute import KNNImputer
import matplotlib.pyplot as plt
from pandas import ExcelWriter
from pathlib import Path
import pandas as pd
import numpy as np
import locale
import zipfile
import sys 
import os
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')


def distance_matrix(x0, y0, x1, y1):
    obs = np.vstack((x0, y0)).T
    interp = np.vstack((x1, y1)).T

    d0 = np.subtract.outer(obs[:,0], interp[:,0])
    d1 = np.subtract.outer(obs[:,1], interp[:,1])

    return np.hypot(d0, d1)
    

def simple_idw(x, y, z, xi, yi):
    dist = distance_matrix(x,y, xi,yi)
    #print(dist)
    
    weights = 1.0/dist #**2
    weights /= weights.sum(axis=0)

    zi = np.dot(weights.T, z)
    return zi
    

def crear_csv_llenado(df_valor, lista_files,tiempo,df_fechas):
    X = df_valor.values
    imputer = KNNImputer(n_neighbors=2, weights="distance")
    salida = imputer.fit_transform(X)
    salida = pd.DataFrame(salida)
    
    for i in np.arange(0,len(lista_files),1):
        salida_unica = pd.DataFrame(salida[i]).rename({i:'Valor'},axis = 1)
        salida_unica.index = tiempo.index
        salida_unica = salida_unica.loc[df_fechas['FECHA_INICIAL'][i]:df_fechas['FECHA_FINAL'][i]]
        salida_unica.to_csv('../PRE_SALIDAS/DATA_LLENADO/' + lista_files[i])


def llenado(path_pre, lista_files):
    
    Path('../PRE_SALIDAS/DATA_LLENADO/').mkdir(parents=True, exist_ok=True)   #Crear carpeta de salida de datos llenados

    # dia completo
    año_ini = '1995'
    mes_ini = '01'
    dia_ini = '01'
    
    año_fin = '2023'
    mes_fin = '06'
    dia_fin = '30'
    
    dia_completo = [d.strftime('%Y-%m-%d') for d in pd.date_range(año_ini+ mes_ini + dia_ini, año_fin + mes_fin + dia_fin, freq='1D')]
    tiempo = pd.DataFrame(dia_completo, columns = ['Fecha'])
    tiempo = tiempo.set_index('Fecha');tiempo.index = pd.to_datetime(tiempo.index)
    
    
    fecha_inicio = []
    fecha_fin    = []
    
    '''Llamar datos csv por estación'''
    
    for i in np.arange(0,len(lista_files),1):
        data = pd.read_csv(path_pre + lista_files[i])
        data = data[['Fecha','Valor']]; data = data.set_index('Fecha');data.index = pd.to_datetime(data.index)
        data = data.loc[año_ini + '-' + mes_ini +  '-' + dia_ini: año_fin + '-' + mes_fin +  '-' + dia_fin]
        fecha_inicio = np.append(fecha_inicio,data.index[0].strftime('%Y-%m-%d'))
        fecha_fin    = np.append(fecha_fin,data.index[-1].strftime('%Y-%m-%d'))
        salida = pd.concat([data, tiempo], axis=1)
        
    df_fechas = pd.DataFrame({'FECHA_INICIAL':fecha_inicio, 'FECHA_FINAL':fecha_fin})
    df_fechas['FECHA_INICIAL'] = año_ini + '-' + mes_ini +  '-' + dia_ini
    df_fechas['FECHA_FINAL']   = año_fin + '-' + mes_fin +  '-' + dia_fin
    
    
    df_valor     = tiempo.copy()
    df_latitude  = tiempo.copy()
    df_longitude = tiempo.copy()
    
    for i in np.arange(0,len(lista_files),1):
        data  = pd.read_csv(path_pre + lista_files[i])
        
        valor = data[['Fecha', 'Valor']]
        valor = valor.rename({'Valor': i}, axis = 1)
        valor = valor.set_index('Fecha')
        valor.index = pd.to_datetime(valor.index)
        valor = valor.loc[año_ini + '-' + mes_ini +  '-' + dia_ini: año_fin + '-' + mes_fin +  '-' + dia_fin]
        
        lat   = data[['Fecha', 'Latitud']]
        lat   = lat.rename({'Latitud': i}, axis = 1)
        lat   = lat.set_index('Fecha')
        lat.index = pd.to_datetime(lat.index)
        lat = lat.loc[año_ini + '-' + mes_ini +  '-' + dia_ini: año_fin + '-' + mes_fin +  '-' + dia_fin]
        
        lon   = data[['Fecha', 'Longitud']]
        lon   = lon.rename({'Longitud': i}, axis = 1)
        lon   = lon.set_index('Fecha')
        lon.index = pd.to_datetime(lon.index)
        lon = lon.loc[año_ini + '-' + mes_ini +  '-' + dia_ini: año_fin + '-' + mes_fin +  '-' + dia_fin]
    
        df_valor     = pd.concat([df_valor,valor],axis = 1)
        df_latitude  = pd.concat([df_latitude,lat],axis = 1)
        df_longitude = pd.concat([df_longitude,lon],axis = 1)
        
        df_latitude = df_latitude.bfill()
        df_latitude = df_latitude.ffill()  
    
        df_longitude = df_latitude.bfill()
        df_longitude = df_latitude.ffill()  

    fechas_iterar = df_valor.index
    suma = 0
    for row in np.arange(0,len(fechas_iterar),1):
        suma += 1; progress = int(suma/len(df_valor) * 100)
        sys.stdout.write('\r')
        sys.stdout.write('[%-20s] %d%%' % ('=' * progress, progress))
        sys.stdout.flush()
        
        array = pd.DataFrame(df_valor.loc[fechas_iterar[row]]).T.values
        index_nan = np.argwhere(np.isnan(array))[:,1]
        
        if len(index_nan) != 0:
            index_no_nan = np.argwhere(~np.isnan(array))[:,1]
            
            x = pd.DataFrame(df_longitude.loc[fechas_iterar[row]]).T[index_no_nan].values
            y = pd.DataFrame(df_latitude.loc[fechas_iterar[row]]).T[index_no_nan].values
            z = pd.DataFrame(df_valor.loc[fechas_iterar[row]]).T[index_no_nan].values
    
            index_remplazar = pd.DataFrame(df_longitude.loc[fechas_iterar[row]]).T.index
    
            for col in np.arange(0,len(index_nan),1):
                xi = pd.DataFrame(df_longitude.loc[fechas_iterar[row]]).T[index_nan[col]].values
                yi = pd.DataFrame(df_latitude.loc[fechas_iterar[row]]).T[index_nan[col]].values
                zi = simple_idw(x[0],y[0],z[0],xi,yi)
                df_valor.loc[index_remplazar,index_nan[col]] = zi
                
    crear_csv_llenado(df_valor,lista_files,tiempo,df_fechas)
