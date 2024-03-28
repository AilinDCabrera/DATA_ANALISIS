import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def boxplots(lista_files):
    nombres_estaciones_plot = [x[:-4] + '[' for x in lista_files]
    nombres_estaciones_plot = [x[:x.index('[') + len('[')-1] for x in nombres_estaciones_plot]
    
   #months = ["ene.", "feb.", "mar.", 'abr.', "may.", "jun.", "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]
    months = ["ene", "feb", "mar", 'abr', "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
    PROPS = {
        'boxprops':{'facecolor':'white', 'edgecolor':'black'},
        'medianprops':{'color':'black'},
        'whiskerprops':{'color':'black'},
        'capprops':{'color':'black'}
    }
    #plt.rcParams.update({'font.weight' : 'bold'})
    flierprops = dict(marker='.', markersize=3)
    plt.style.use('seaborn-v0_8-whitegrid')
    for k in np.arange(0,len(lista_files),1):
        data = pd.read_csv('../PRE_SALIDAS/DATA_COMPLETA/' + lista_files[k])
        data = data[['Fecha', 'Valor']]; data = data.set_index('Fecha');data.index = pd.to_datetime(data.index)
        data = data.reset_index()
        dataframe = data.copy()
        dataframe['month'] = dataframe['Fecha'].dt.strftime('%b')
    
        ######out
        df_outliers = pd.DataFrame([])
        for i in np.arange(0,len(months),1):
            dataframe['month'].drop_duplicates()
            df = dataframe[dataframe['month'] == months[i]]
            Q1 = df['Valor'].quantile(0.25)
            Q3 = df['Valor'].quantile(0.75)
            IQR = Q3 - Q1    #IQR is interquartile range. 
            filtro = (df['Valor'] < Q1 - 1.5 * IQR) | (df['Valor'] > Q3 + 1.5 *IQR)
            df = df.loc[filtro]
            df_outliers = pd.concat([df_outliers,df])
        ###### out
    
        plt.figure(figsize=(8,5),dpi = 150)
        gs = gridspec.GridSpec(4, 1, wspace=0.0, hspace=0.0)
    
        ax1 = plt.subplot(gs[0])
        plt.title('Precipitación diaria en ' + str(nombres_estaciones_plot[k]),fontsize = 18)
        sns.boxplot(x='month',y='Valor',data=df_outliers,**PROPS,flierprops=flierprops,showfliers=True,ax = ax1)
        ax1.yaxis.set_label_position("right")
        ax1.yaxis.tick_right()
        plt.ylabel('mm/dia', fontsize = 10)
        #plt.grid(linestyle='-')
        ax2 = plt.subplot(gs[1:])
        sns.boxplot(x='month',y='Valor',data=dataframe,**PROPS,flierprops=flierprops,showfliers=False,ax = ax2)
        plt.grid(axis='y')
        plt.ylabel('mm/dia',fontsize = 16)
        plt.yticks(fontsize = 16)
        plt.xticks(fontsize = 16, rotation=90)
        plt.xlabel('');
        #plt.savefig(folder_input + 'PRE_SALIDAS/IMG/boxplot' + str(k) + '.jpg', dpi = 300, bbox_inches = 'tight')
        print(df_outliers.describe())
        plt.show()