import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def curvas_doble_masa(lista_files):

    '''Grafica la curva de doble masa de precipitación para cada estacion con la acumulación mensual '''
    
    plt.style.use('default')
    
    nombres_estaciones_plot = [x[:-4] + '[' for x in lista_files]
    nombres_estaciones_plot = [x[:x.index('[') + len('[')-1] for x in nombres_estaciones_plot]

    numi = 0
    numf = len(lista_files)
    dataframe = pd.DataFrame([])
    for i in np.arange(numi,len(lista_files),1):
        
        data = pd.read_csv('../PRE_SALIDAS/DATA_LLENADO/' + lista_files[i]); data = data[['Fecha', 'Valor']]; data = data.set_index('Fecha');data.index = pd.to_datetime(data.index)
        data = data.groupby(data.index.strftime('%Y-%m')).sum()
        data.index = pd.to_datetime(data.index)
        data = data.rename(columns={'Valor': nombres_estaciones_plot[i]})
        dataframe = pd.concat([dataframe,data], axis = 1)
    
    
    props2 = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    
    for i in np.arange(numi,numf,1):
        plt.figure(figsize=(6,6),dpi = 150)
        dataframe2             = dataframe.drop(nombres_estaciones_plot[i], axis = 1)
        dataframe3             = dataframe.cumsum()
        dataframe2['PROMEDIO'] = dataframe2.mean(axis = 1).round(1)
        
        plt.title('PRECIPITACIÓN ACUMULADA', fontsize = 14)
        plt.plot(dataframe3[nombres_estaciones_plot[i]].values, dataframe2['PROMEDIO'].cumsum().values)
        plt.grid(); plt.xlim(0); plt.ylim(0)
        plt.xlabel(nombres_estaciones_plot[i] + '(mm)')
        plt.ylabel('PROMEDIO DE ESTACIONES ' + '(mm)')
        
        texto = pd.concat([dataframe3[nombres_estaciones_plot[i]],dataframe2['PROMEDIO'].cumsum()], axis = 1).corr().values[0,1].round(4)
        #plt.text(0.05, 0.95, texto,fontsize=14,verticalalignment='top', bbox=props2)
        plt.text(0.82,1.02,"r = {}".format(texto), transform=plt.gca().transAxes, bbox=props2)
        plt.xticks(fontsize = 14)
        plt.yticks(fontsize = 14)
        plt.xlim(0,max([np.max(dataframe3[nombres_estaciones_plot[i]].values),np.max(dataframe2['PROMEDIO'].cumsum().values)]))
        plt.ylim(0,max([np.max(dataframe3[nombres_estaciones_plot[i]].values),np.max(dataframe2['PROMEDIO'].cumsum().values)]));
        
        #plt.savefig(folder_input + 'PRE_SALIDAS/IMG/' + 'pre_acumulada' + str(i) +'.png', dpi = 300, bbox_inches="tight")