import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as  plt
import os
import sys
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

def haversine(lat1, lon1, lat2, lon2):
    # Radio de la Tierra en kilómetros
    radio_tierra = 6371.0
    
    # Convertir grados a radianes
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Diferencia de latitud y longitud
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Calcular la distancia usando la fórmula haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = radio_tierra * c
    
    return distancia

def estaciones_mas_cercanas(lat_punto, lon_punto, estaciones):
    # Calcular distancias entre la estacion a llenar y las otras estaciones
    distancias = []
    for estacion, (lat, lon) in estaciones.items():
        distancia = haversine(lat_punto, lon_punto, lat, lon)
        distancias.append((distancia, estacion))
    
    # Ordenar las distancias de menor a mayor
    distancias.sort()
    
    # Tomar los nombres de las dos estaciones más cercanas
    estacion1 = distancias[0][1]
    estacion2 = distancias[1][1]
    
    return estacion1, estacion2




def llenar_datos(lista_files,var):
    dataframes = []
    numi = 0
    coor_estaciones = {}
    
    for i in np.arange(numi,len(lista_files),1):  #llamar datos de las estaciones
        data_est = pd.read_csv(f'../{var}_SALIDAS/DATA_COMPLETA/' + lista_files[i])
        data_coor = pd.read_csv(f'../{var}/' + lista_files[i])
        lat = data_coor["Latitud"][i]
        lon = data_coor["Longitud"][i]
        coor_estaciones[lista_files[i][:-4]] = (lat,lon)
        data_est = data_est[['Fecha', 'Valor']]; data_est = data_est.set_index('Fecha');data_est.index = pd.to_datetime(data_est.index)
        data_est.rename(columns={'Valor':lista_files[i][:-4]},inplace=True)
        dataframes.append(data_est)
    
        
    data_total = pd.concat(dataframes,axis=1) # Asignar todos los datos de las estaciones a un solo dataframe
    name_estaciones = data_total.columns.to_list()
    data_llena1 = data_total.copy()
    
    for estacion in name_estaciones:
        data = data_total.copy()
        data_estacion = data[[estacion]]
        data_select = data.drop(estacion,axis=1)   
        # Calcula el número mínimo de valores no nulos requeridos
        min_non_nulls = len(data_select) * 0.8
        # Selecciona las columnas que tienen menos del 20% de valores NaN
        df_filtrado = data_select.dropna(axis=1, thresh=min_non_nulls)
        #print(len(df_filtrado.columns))
        
        if len(df_filtrado.columns) < 2:
            #print("No hay estaciones suficientes para: ", estacion)
            continue
            
        est_confiables = df_filtrado.columns.to_list()
        coor_estacion = coor_estaciones[estacion]
        dic_filtrado = {clave: valor for clave, valor in coor_estaciones.items() if clave in est_confiables}
        estacion2, estacion3 = estaciones_mas_cercanas(coor_estacion[0], coor_estacion[1], dic_filtrado)
    
        
        data = data[[estacion, estacion2, estacion3]]
        data_not_nan = data.dropna()   #elimina los valores nan para que solo queden los datos de entrenamiento
        x_train = data_not_nan.copy()
        x_train = x_train.drop(estacion, axis=1)    
        y_train = data_not_nan[[estacion]]
        y_train= np.ravel(y_train[estacion])
        
        #lim = int(len(data_not_nan)*0.8) # lineas para probar el modelo
        # x_train = data_not_nan[['EstA','EstB']][:lim]
        # y_train = data_not_nan[['EstC']][:lim].values.flatten()
        
        scaler = StandardScaler(with_mean=True, with_std=True).fit(x_train.values)
        
        xTrainScaled = scaler.transform(x_train)
        
        regr = MLPRegressor(random_state=1,max_iter=5000).fit(xTrainScaled,y_train)
        
        #x_test = data_not_nan[['EstA','EstB']][lim:] #solo activar si se va a evaluar el modelo
        #x_testScaled = scaler.transform(x_test)
        
        # Selecciona los datos para llenar, las dos primeras condiciones seleccionan el input y la tercera indica los datos que deben ser llenados
        filas_llenar = data.loc[(~data[estacion2].isnull()) & (~data[estacion3].isnull()) & (data[estacion].isnull())].copy()
        x_test = filas_llenar[[estacion2,estacion3]]    #ajustar nomrbes de columnas
        x_testScaled = scaler.transform(x_test)
        
        yPredict = regr.predict(x_testScaled)  #Se realiza la prediccion
        
        df_pred = pd.DataFrame(yPredict, index=filas_llenar.index,columns=[estacion])
        
        data_llena1.loc[df_pred.index,estacion] = df_pred[estacion]
    
    impute_it = IterativeImputer()
    pred_II = impute_it.fit_transform(data_llena1)
    data_llena_final = pd.DataFrame(pred_II, index=data.index, columns=data_llena1.columns)
    
    
    for columna in data_llena_final.columns:
        # Crea DataFrame para cada estacion por separado
        df_temporal = pd.DataFrame(data_llena_final[columna], columns=[columna])
        df_temporal.columns.values[0] = 'Valor'
        df_temporal.reset_index(inplace=True)
        ruta = f"../{var}_SALIDAS/DATA_LLENADO/"
        if not os.path.exists(ruta):
            os.makedirs(ruta)
        df_temporal.to_csv(f"{ruta}/{columna}.csv", index=False)