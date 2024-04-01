import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def bxp_mes(lista_files):
    ''' Grafica boxplots con datos mensuales comparando los datos llenados y los originales'''
    
    nombres_estaciones_plot = [x[:-4] + '[' for x in lista_files]
    nombres_estaciones_plot = [x[:x.index('[') + len('[')-1] for x in nombres_estaciones_plot]
    
    plt.style.use('default')
    dataframe_llenado = pd.DataFrame([])
    numi = 0 
    for i in np.arange(numi,len(lista_files),1):
        data = pd.read_csv('../PRE_SALIDAS/DATA_LLENADO/' + lista_files[i]); data = data[['Fecha', 'Valor']]; data = data.set_index('Fecha');data.index = pd.to_datetime(data.index)
        data = data.groupby(data.index.strftime('%Y-%m')).sum()
        data.index = pd.to_datetime(data.index)
        data = data.rename(columns={'Valor': nombres_estaciones_plot[i]})
        dataframe_llenado = pd.concat([dataframe_llenado,data], axis = 1)
    dataframe_llenado = pd.melt(dataframe_llenado,var_name='Estacion',value_name = 'Valores')    
    
    
    plt.style.use('default')
    dataframe_completo = pd.DataFrame([])
    for i in np.arange(numi,len(lista_files),1):
        data = pd.read_csv('../PRE_SALIDAS/DATA_COMPLETA/' + lista_files[i]); data = data[['Fecha', 'Valor']]; data = data.set_index('Fecha');data.index = pd.to_datetime(data.index)
        data = data.groupby(data.index.strftime('%Y-%m')).sum()
        data.index = pd.to_datetime(data.index)
        data = data.rename(columns={'Valor': nombres_estaciones_plot[i]})
        dataframe_completo = pd.concat([dataframe_completo,data], axis = 1)
        
    dataframe_completo = pd.melt(dataframe_completo,var_name='Estacion',value_name = 'Valores')    
    
    
    dataframe_completo['Tipo'] = 'Original'
    dataframe_llenado['Tipo'] = 'Llenado'
    
    dataframe_plot = pd.concat([dataframe_completo,dataframe_llenado], axis = 0)
    
    flierprops = dict(marker='.', markersize=3)
    plt.figure(figsize = (15,5), dpi  = 150)
    sns.boxplot(data = dataframe_plot, x = 'Estacion', y = 'Valores', hue = 'Tipo',flierprops=flierprops)
    plt.xticks(rotation = 90); plt.ylabel('mm/mes');plt.xlabel(''); plt.title('Precipitación mensual', fontsize=16, y = 1.15)
    plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc='lower left',
                    mode='expand', borderaxespad=0, ncol=2);
    #plt.savefig(folder_input + 'PRE_SALIDAS/IMG/' + 'pre_mensual_llen-orig.png', dpi = 300, bbox_inches="tight")


def bxp_anio(lista_files):
    ''' Grafica boxplots con datos anuales comparando los datos llenados y los originales'''
    
    plt.style.use('default')
    dataframe_llenado = pd.DataFrame([])
    
    nombres_estaciones_plot = [x[:-4] + '[' for x in lista_files]
    nombres_estaciones_plot = [x[:x.index('[') + len('[')-1] for x in nombres_estaciones_plot]
    numi = 0 
    
    for i in np.arange(numi,len(lista_files),1):
        data = pd.read_csv('../PRE_SALIDAS/DATA_LLENADO/' + lista_files[i]); data = data[['Fecha', 'Valor']]; data = data.set_index('Fecha');data.index = pd.to_datetime(data.index)
        data = data.where(data<150,150)
        #data = data.groupby(data.index.strftime('%Y-%m')).sum()
        data.index = pd.to_datetime(data.index)
        data = data.rename(columns={'Valor': nombres_estaciones_plot[i]})
        dataframe_llenado = pd.concat([dataframe_llenado,data], axis = 1)
    dataframe_llenado = pd.melt(dataframe_llenado,var_name='Estacion',value_name = 'Valores')    
    
    
    plt.style.use('default')
    dataframe_completo = pd.DataFrame([])
    for i in np.arange(numi,len(lista_files),1):
        data = pd.read_csv('../PRE_SALIDAS/DATA_COMPLETA/' + lista_files[i]); data = data[['Fecha', 'Valor']]; data = data.set_index('Fecha');data.index = pd.to_datetime(data.index)
        data = data.where(data<150,150)
        #data = data.groupby(data.index.strftime('%Y-%m')).sum()
        data.index = pd.to_datetime(data.index)
        data = data.rename(columns={'Valor': nombres_estaciones_plot[i]})
        dataframe_completo = pd.concat([dataframe_completo,data], axis = 1)
        
    dataframe_completo = pd.melt(dataframe_completo,var_name='Estacion',value_name = 'Valores')    
    
    
    dataframe_completo['Tipo'] = 'Original'
    dataframe_llenado['Tipo'] = 'Llenado'

    dataframe_plot = pd.concat([dataframe_completo,dataframe_llenado], axis = 0)

    dataframe = dataframe_plot.copy()
    ######out
    df_outliers = pd.DataFrame([])
    for i in np.arange(0,len(dataframe_plot.Estacion.unique()),1):
        df = dataframe[dataframe['Estacion'] == dataframe_plot.Estacion.unique()[i]]
        Q1 = df['Valores'].quantile(0.25)
        Q3 = df['Valores'].quantile(0.75)
        IQR = Q3 - Q1    #IQR is interquartile range. 
        filtro = (df['Valores'] < Q1 - 1.5 * IQR) | (df['Valores'] > Q3 + 1.5 *IQR)
        df = df.loc[filtro]
        df_outliers = pd.concat([df_outliers,df])
    ###### out
    flierprops = dict(marker='.', markersize=3)    
    plt.figure(figsize = (20,8),dpi  = 150)
    gs = gridspec.GridSpec(4, 1, wspace=0.0, hspace=0.0)

    ax1 = plt.subplot(gs[0])
    plt.title('Precipitación diaria (Original - Llenado)',fontsize = 16)
    sns.boxplot(x='Estacion',y='Valores',data=df_outliers,hue = 'Tipo',flierprops=flierprops,showfliers=True,ax = ax1)
    ax1.yaxis.set_label_position("right")
    ax1.yaxis.tick_right()
    plt.xticks(rotation=90)
    plt.ylabel('mm/dia', fontsize = 14)
    plt.legend([],[])
    #plt.grid(linestyle='-')
    ax2 = plt.subplot(gs[1:])
    sns.boxplot(x='Estacion',y='Valores',data=dataframe,hue = 'Tipo',flierprops=flierprops,showfliers=False,ax = ax2)
    plt.ylabel('mm/dia',fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.xticks(fontsize = 14, rotation=90)
    plt.xlabel('');
    print(df_outliers.describe())
    #plt.savefig(folder_input + 'PRE_SALIDAS/IMG/' + 'pre_diaria_llen-orig.png', dpi = 300, bbox_inches="tight")
    plt.show()