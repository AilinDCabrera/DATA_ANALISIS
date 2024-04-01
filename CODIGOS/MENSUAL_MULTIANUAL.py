import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def mm_estaciones(dataframe, numf,numi):
    #cc = cm.Spectral_r(np.linspace(0,1,10))
    #plt.rcParams.update({'font.size': 16,'font.weight' : 'bold'})
    cc = cm.Blues(np.linspace(0,1,numf+1-numi))
    cc = cc[1:]
    dataframe.T.sort_values(by = 'oct').T.plot.bar(figsize=(10,6), colormap = 'Spectral',zorder=10);
    plt.xlabel('Mes',fontsize=15)
    plt.ylabel('mm/mes',fontsize=15)
    plt.title('Precipitación mensual media multianual', fontsize = 20)
    plt.legend(fontsize=14,loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(axis = 'y', zorder = -1)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    #plt.legend(fontsize=14)
    #plt.savefig(folder_input + 'PRE_SALIDAS/IMG/' + 'g-' + str(numi) + '-' + str(numf) + '.png', dpi = 300, bbox_inches="tight")

    
def mm_global(dataframe):
    plt.style.use('default')
    plt.figure(figsize=(10,5), dpi = 150)
    plt.bar(dataframe.index,dataframe.mean(axis=1), zorder = 10, color = '#19458E')
    plt.xlabel('Mes')
    plt.ylabel('mm/mes')
    plt.title('Precipitación mensual media multianual', fontsize = 12)
    plt.grid(axis = 'y', zorder = -1)
    

def mensual_multianual(lista_files, tipo, var):
    '''calcula la precipitacion mensual media multianual
        tipo: 'estaciones' - una grafica que incluye todas las estaciones por separado 
        tipo: 'global' - grafica e promedio de todas las estaciones
    '''

    nombres_estaciones_plot = [x[:-4] + '[' for x in lista_files]
    nombres_estaciones_plot = [x[:x.index('[') + len('[')-1] for x in nombres_estaciones_plot]
    
    months = ["ene", "feb", "mar", 'abr', "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
    plt.style.use('default')
    numi = 0
    numf = len(lista_files)
    
    for i in np.arange(numi,numf,1):
        if i == numi:
            data = pd.read_csv(f'../{var}_SALIDAS/DATA_LLENADO/{lista_files[i]}'); data = data[['Fecha', 'Valor']]; data = data.set_index('Fecha');data.index = pd.to_datetime(data.index)
            if var == 'PRE':
                data = data.groupby(data.index.strftime('%Y-%m')).sum()
            elif var == 'TEM':
                data = data.groupby(data.index.strftime('%Y-%m')).mean()
            data.index = pd.to_datetime(data.index)
            data = data.groupby(data.index.strftime('%b')).mean()
            data = data.rename(columns={'Valor': nombres_estaciones_plot[numi]})
            
            
            data = data.reset_index()
            data['Fecha'] = pd.Categorical(data['Fecha'], categories=months, ordered=True)
            data = data.sort_values('Fecha')
            data = data.set_index('Fecha')
    
            dataframe = data
        else:
            data = pd.read_csv(f'../{var}_SALIDAS/DATA_LLENADO/{lista_files[i]}'); data = data[['Fecha', 'Valor']]; data = data.set_index('Fecha');data.index = pd.to_datetime(data.index)
            if var == 'PRE':
                data = data.groupby(data.index.strftime('%Y-%m')).sum()
            elif var == 'TEM':
                data = data.groupby(data.index.strftime('%Y-%m')).mean()
            data.index = pd.to_datetime(data.index)
            data = data.groupby(data.index.strftime('%b')).mean()
            
            data = data.rename(columns={'Valor': nombres_estaciones_plot[i]})
            #dataframe = pd.merge(dataframe.reset_index(),data.reset_index(), left_index=False, right_index=False)
            
            data = data.reset_index()
            data['Fecha'] = pd.Categorical(data['Fecha'], categories=months, ordered=True)
            data = data.sort_values('Fecha')
            data = data.set_index('Fecha')
    
    
            dataframe = pd.concat([dataframe, data], axis = 1)
            
    if tipo == 'estaciones':
        mm_estaciones(dataframe, numf, numi)
        
    elif tipo == 'global':
        mm_global(dataframe)
