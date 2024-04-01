import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def cargar2(lista,num,nombres_estaciones_plot,rango_tiempo,var):

    tiempo_ini = rango_tiempo[0]
    tiempo_fin  = rango_tiempo[1]
    
    data = pd.read_csv(f'../{var}_SALIDAS/DATA_COMPLETA/{lista[num]}')
    data = data[['Fecha', 'Valor']]; data = data.set_index('Fecha');data.index = pd.to_datetime(data.index)
    data = data.loc[tiempo_ini:tiempo_fin]
    data.columns = [nombres_estaciones_plot[num]]
    return(data)
    
def correlacion(lista_files,rango_tiempo,var):
    numi = 0
    numf = len(lista_files)
    nombres_estaciones_plot = [x[:-4] + '[' for x in lista_files]
    nombres_estaciones_plot = [x[:x.index('[') + len('[')-1] for x in nombres_estaciones_plot]
    
    for i in np.arange(numi,numf,1):
        if i == numi:
            dataframe = cargar2(lista_files,i,nombres_estaciones_plot,rango_tiempo,var)
        else:
            data00 = cargar2(lista_files,i,nombres_estaciones_plot,rango_tiempo,var)
            dataframe = pd.concat([dataframe,data00],axis=1)
    
    
    plt.style.use('default')
    sns.set(font_scale = 1)
    
    cbar_kws = {"shrink":.8} 
    colormap = 'Spectral_r'
    
    plt.figure(figsize=(12, 12), dpi = 300)
    g = sns.heatmap(dataframe.corr(),square=True, annot=True, fmt=".2f", cbar_kws = cbar_kws, linewidth = 2, cmap = colormap, vmin = 0, vmax=1)
    
    plt.title('Coeficiente de Correlación de Pearson', fontsize = 14, fontweight='bold')
    #plt.xlabel('Estaciones', fontsize = 12,fontweight='bold' )
    #plt.ylabel('Estaciones', fontsize = 12, fontweight='bold')
    g.set_yticklabels(labels=g.get_yticklabels(), va='center')