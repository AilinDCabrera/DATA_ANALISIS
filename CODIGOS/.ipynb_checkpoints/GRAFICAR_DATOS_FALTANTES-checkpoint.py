import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def cargar(lista_files,num,rango_tiempo,var):
    '''Carga los datos de una estación de monitoreo dentro de un rango de tiempo específico y los renombra'''

    tiempo_ini = rango_tiempo[0]
    tiempo_fin  = rango_tiempo[1]
    
    data = pd.read_csv(f'../{var}_SALIDAS/DATA_COMPLETA/{lista_files[num]}')
    data = data[['Fecha', 'Valor']]; data = data.set_index('Fecha');data.index = pd.to_datetime(data.index)
    data = data.loc[tiempo_ini:tiempo_fin]
    data.columns = ['s' + str(num)]
    return(data)

def split_years(dataframe):
    '''Divide los datos por año'''
    dataframe['year'] = dataframe.index.year
    return ([dataframe[dataframe['year'] == y] for y in dataframe['year'].unique()])

def listas(data,num):
    '''Cuenta los valores faltantes por año en una estación específica.'''
    
    dataframe                 = split_years(data.copy())
    numero_years              = len(data.index.year.unique())
    lista_year_faltante       = []
    lista_valor_year_faltante = []

    for i in np.arange(0,numero_years,1):
        year_faltante       = dataframe[i]['year'].iloc[0]
        valor_year_faltante = dataframe[i]['s' + str(num)].isna().sum()
        lista_year_faltante.append(year_faltante)
        lista_valor_year_faltante.append(valor_year_faltante)
        
    return(lista_year_faltante,lista_valor_year_faltante)


def lista_tamaño(valores):
    '''Categoriza la cantidad de valores faltantes en rangos predefinidos.'''
    lista_tamaño = []
    for i in valores:
        if i >= 0 and i < 100:
            lista_tamaño.append(0)
        if i >=100 and i < 200:
            lista_tamaño.append(100)
        if i >=200 and i < 300:
            lista_tamaño.append(200)
        if i >= 300:
            lista_tamaño.append(300)
    return(np.array(lista_tamaño))


def compilado(num,lista_files, rango_tiempo,var):
    '''Calcula y resume los valores faltantes para cada estación'''
    data = cargar(lista_files,num,rango_tiempo,var)
    años,valores = listas(data,num)
    inten = lista_tamaño(valores)
    #print(valores)
    #print(np.round((np.array(valores).sum()/(365*len(años)))*100,2), '%', lista_files[num])
    return(años,inten)

def datos_faltantes(lista_files,rango_tiempo,var):
    '''Visualiza los años con datos faltantes para cada estación'''
    x    = []
    y    = []
    hue  = []
    numi = 0
    numf = len(lista_files)
    
    nombres_estaciones_plot = [x[:-4] + '[' for x in lista_files]
    nombres_estaciones_plot = [x[:x.index('[') + len('[')-1] for x in nombres_estaciones_plot]
    
    for num in np.arange(numi,numf,1):
        años,inten = compilado(num,lista_files,rango_tiempo,var)
        s     = [nombres_estaciones_plot[num]]*len(años)
        x     = años + x
        y     = s + y
        hue  = np.concatenate((hue,inten))
        
    x1 = []
    for i in np.arange(0,len(x),1):
        ts = pd.to_datetime(str(x[i])) 
        x1.append(ts.strftime('%Y'))


    plt.figure(figsize=(14,5), dpi = 300) 
    g = sns.scatterplot(x=x1, y=y[::-1], hue=hue, size = hue, palette='Spectral_r', sizes=(20, 300),legend="full")
    plt.legend(fontsize=18,loc='center right', bbox_to_anchor=(1.23, 0.5))
    
    plt.xticks(rotation=90)
    plt.title('Datos Faltantes de Precipitación', fontsize = 26)
    
    legend = g.legend_
    
    cont = 0
    for i in np.arange(0,len(list(legend.get_texts())),1):
        valor  = int(float(legend.get_texts()[i].get_text()))
        #print(valor)
        if valor == 0:
            legend.get_texts()[cont].set_text('[0-100)');cont += 1
        elif  valor == 100:
            legend.get_texts()[cont].set_text('[100-200)');cont += 1
        elif  valor == 200:
            legend.get_texts()[cont].set_text('[200-300)');cont += 1
        elif  valor == 300: 
            legend.get_texts()[cont].set_text('[300-365]');cont += 1
        
    plt.yticks(fontsize = 20)
    plt.xticks(fontsize = 20)

    fig = plt.gcf()
    plt.close(fig)

    return(fig)
    #plt.savefig(folder_input + 'PRE_SALIDAS/IMG/' +'v-' + str(numi) + '-' + str(numf) + '.jpg', dpi = 300, bbox_inches="tight")