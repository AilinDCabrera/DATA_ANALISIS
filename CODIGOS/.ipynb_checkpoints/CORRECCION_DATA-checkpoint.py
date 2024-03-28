import numpy as np
import pandas as pd

'''Asignan nan a los valores anomalos para la fecha correspondiente, recrea los archivos de data completa'''

def correccion(lista_files):
    año_ini = '1995'
    mes_ini = '01'
    dia_ini = '01'
    
    año_fin = '2023'
    mes_fin = '06'
    dia_fin = '30'
    
    dia_completo = [d.strftime('%Y-%m-%d') for d in pd.date_range(año_ini+ mes_ini + dia_ini, año_fin + mes_fin + dia_fin, freq='1D')]
    tiempo = pd.DataFrame(dia_completo, columns = ['Fecha'])
    tiempo = tiempo.set_index('Fecha');tiempo.index = pd.to_datetime(tiempo.index)
    

    '''Asigna nan a los valores menores a 0 y mayores a 150'''
    for k in np.arange(0,len(lista_files),1):
        data = pd.read_csv('../PRE_SALIDAS/DATA_COMPLETA/' + lista_files[k])
        data = data[['Fecha', 'Valor']]; data = data.set_index('Fecha');data.index = pd.to_datetime(data.index)
        nuevos_valores = []
        for i in np.arange(0,len(data),1):
            valor = data['Valor'].iloc[i]
            if valor<0 or valor>150:
                valor = np.nan
                data[i:i+1] = valor

        '''Calcula el valor máximo permitido (maxi) como la media más 10 veces la desviación estándar de los valores'''
        data = data.dropna()
    
        maxi =data['Valor'].mean() + 10*data['Valor'].std()
        data2 = data[(data['Valor'] < maxi) & (data['Valor'] >= 0)] #Filtra los datos que se encuentran en los valores permitidos

        '''Crea dataframes con fechas diarias del periodo a evaluar, de manera que hay registro de los días en los que no hay datos '''
        
        data = data.loc['1995-01-01':'2023-06-30']
        salida = pd.concat([data, tiempo], axis=1)
        salida.to_csv('../PRE_SALIDAS/DATA_COMPLETA/' + lista_files[k])










