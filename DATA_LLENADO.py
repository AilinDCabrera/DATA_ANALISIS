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


# dia completo
dia_completo = [d.strftime('%Y-%m-%d') for d in pd.date_range(año_ini+ mes_ini + dia_ini, año_fin + mes_fin + dia_fin, freq='1D')]
tiempo = pd.DataFrame(dia_completo, columns = ['Fecha'])
tiempo = tiempo.set_index('Fecha');tiempo.index = pd.to_datetime(tiempo.index)


data_pre_cer = pd.read_csv('../PP_CERREJON_1990_2023.csv') #Hacer que las estaciones queden aquí en un solo dataframe
estaciones = data_pre_cer.columns.unique().tolist()[1:]

año_ini = '1995'
mes_ini = '01'
dia_ini = '01'

año_fin = '2023'
mes_fin = '06'
dia_fin = '30'


fecha_inicio = []
fecha_fin    = []
"""Llamar datos csv por estación"""
for i in np.arange(0,len(lista_files),1):
    data = pd.read_csv(path_pre + lista_files[i]); data = data[['Fecha', 'Valor']]; data = data.set_index('Fecha');data.index = pd.to_datetime(data.index)
    data = data.loc[año_ini + '-' + mes_ini +  '-' + dia_ini: año_fin + '-' + mes_fin +  '-' + dia_fin]
    fecha_inicio = np.append(fecha_inicio,data.index[0].strftime('%Y-%m-%d'))
    fecha_fin    = np.append(fecha_fin,data.index[-1].strftime('%Y-%m-%d'))
    salida = pd.concat([data, tiempo], axis=1)
    
df_fechas = pd.DataFrame({'FECHA_INICIAL':fecha_inicio, 'FECHA_FINAL':fecha_fin})
df_fechas['FECHA_INICIAL'] = año_ini + '-' + mes_ini +  '-' + dia_ini
df_fechas['FECHA_FINAL']   = año_fin + '-' + mes_fin +  '-' + dia_fin
df_fechas


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

    if lista_files[i][:-4] not in estaciones: # Solo estaciones del IDEAM
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
    
        #df_valor     = pd.concat([df_valor,valor],axis = 1)
        df_latitude  = pd.concat([df_latitude,lat],axis = 1)
        df_longitude = pd.concat([df_longitude,lon],axis = 1)
        
        df_latitude = df_latitude.fillna(method = 'backfill')
        df_latitude = df_latitude.fillna(method = 'pad')
    
        df_longitude = df_longitude.fillna(method = 'backfill')
        df_longitude = df_longitude.fillna(method = 'pad')

    df_valor     = pd.concat([df_valor,valor],axis = 1)
    
fechas_iterar = df_valor.index

df_valor2 = df_valor.copy()