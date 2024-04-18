import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
import zipfile

    
def extrac_zip(path_var_org,list_zip):
    for i in np.arange(0,len(list_zip),1):
        zipdata = zipfile.ZipFile(path_var_org + list_zip[i])
        zipinfos = zipdata.infolist()
        for zipinfo in zipinfos:
            zipinfo.filename = 'datos' + str(i) + '.csv'
            zipdata.extract(zipinfo,path_var_org)
            
def dividir_ideam(path_to_csv_org, path_to_csv,var):
    list_csv_org = os.listdir(path_to_csv_org)
    list_csv_org = [k for k in list_csv_org if '.csv' in k]
    
    for k in np.arange(0,len(list_csv_org),1):
        data_total = pd.read_csv(path_to_csv_org + list_csv_org[k])
        data_total.set_index('Fecha',inplace=True)
        nombres    = data_total['NombreEstacion'].unique()
        data_total

        for i in np.arange(0,len(nombres),1):
            data_filtrada = data_total[data_total['NombreEstacion'] == nombres[i]].copy()
            if var == 'TEM': #si la variable es temperatura, y los maximos y minimos estann en e mismo csv guarda CVSs distintos para la maxima y la mínima
                
                data_filtrada_max = data_filtrada[data_filtrada['DescripcionSerie'] == 'Temperatura máxima diaria']
                data_filtrada_min = data_filtrada[data_filtrada['DescripcionSerie'] == 'Temperatura mínima diaria']
                data_filtrada_max = data_filtrada_max[~data_filtrada_max.index.duplicated()] #Eliminar fechas duplicadas
                data_filtrada_min = data_filtrada_min[~data_filtrada_min.index.duplicated()] #Eliminar fechas duplicadas
                
                data_filtrada_max = data_filtrada_max.reset_index()
                data_filtrada_min = data_filtrada_min.reset_index()

                new_name_MAX = nombres[i].replace('[','MAX [')
                new_name_MIN = nombres[i].replace('[','MIN [')
                if len(data_filtrada_max)>0:
                    data_filtrada_max.to_csv(path_to_csv + new_name_MAX + '.csv', index = False)
                if len(data_filtrada_min)>0:
                    data_filtrada_min.to_csv(path_to_csv + new_name_MIN + '.csv', index = False)

            else:
                data_filtrada = data_filtrada.reset_index()
                data_filtrada.to_csv(path_to_csv + nombres[i] + '.csv', index = False)



def extraer_data(var):

    #descomprimir zip
    """
    Este codigo lee archivos comprimidos y los guarda en una carpeta en donde cada csv corresponde  auna estacion la carpeta debe llamarse con la inicial de la variable + '_ORG'. Ejemplo: PRE_ORG para el caso de la precipitacion
    """
    
    folder_input = os.getcwd()[:-7]
    
    # definicion de rutas
    path_var_org = folder_input + f'{var}_ORG/'
    path_var     = folder_input + f'{var}/'
    
    Path(path_var).mkdir(parents=True, exist_ok=True)

    list_zip = os.listdir(path_var_org)
    list_zip = [k for k in list_zip if '.zip' in k]
    # extraer datos
    extrac_zip(path_var_org,list_zip)
    #dividir 
    dividir_ideam(path_var_org,path_var,var)