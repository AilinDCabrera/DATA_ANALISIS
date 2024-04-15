import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyhomogeneity as hg
plt.style.use('default')

def test_pettitt(lista_files,var):

    '''Grafica los resultados test pettitt y devuelve los resultados de cada estacion'''
    
    nombres_estaciones_plot = [x[:-4] + '[' for x in lista_files]
    nombres_estaciones_plot = [x[:x.index('[') + len('[')-1] for x in nombres_estaciones_plot]
    
    df_resumen_pettitt = pd.DataFrame([])

    figures = []
    for i in np.arange(0,len(lista_files),1):
        data = pd.read_csv(f'../{var}_SALIDAS/DATA_COMPLETA/{lista_files[i]}')  
        data = data[['Fecha', 'Valor']]; data = data.set_index('Fecha');data.index = pd.to_datetime(data.index)
        try:
            a = fechas_corte[fechas_corte['nombre'] == lista_files[i]]['ini'].values[0]
            b = fechas_corte[fechas_corte['nombre'] == lista_files[i]]['fini'].values[0]
        except:
            pass

        if var == 'PRE':
            data = data.groupby(data.index.strftime('%Y-%m')).sum()
        elif var == 'TEM':
            data = data.groupby(data.index.strftime('%Y-%m')).mean()
        data = data[data['Valor'] >= 0.1]
        time = data.index
        data = data['Valor'].values
        result = hg.pettitt_test(data) 
        ff = pd.to_datetime(time.values)
        plt.figure(figsize=(10,5),dpi = 150)
        plt.plot(ff,data, color = 'b')
        plt.plot(ff[0:result.cp],[result.avg[0]]*result.cp, linestyle = '--', color = 'r', label = ('µ1 = ' + str(np.round(result.avg[0],2))))
        plt.plot(ff[result.cp:len(data)],[result.avg[1]]*(len(data)-result.cp), linestyle = '--', color= 'g', label = ('µ2 = ' + str(np.round(result.avg[1],2))))
        plt.title('Pettitt Test - Precipitación Mensual - ' + str(nombres_estaciones_plot[i]) , fontsize = 16)
        plt.ylabel('mm/mes',fontsize=16)
        plt.axvline(x=ff[result.cp], color = 'purple', linestyle = '-', alpha=0.3, label = 't = ' + ff[result.cp].strftime('%Y-%m'))
        plt.legend(fontsize=12)
        plt.grid(axis = 'y')
        #plt.savefig(folder_input + 'PRE_SALIDAS/IMG/' + 'p-t' + str(i) + '.jpg', dpi = 300)
        xx = [result[0],result[1],result[2],result[3],result.avg[0],result.avg[1],nombres_estaciones_plot[i]]
        df_tem = pd.DataFrame(xx).T
        df_resumen_pettitt = pd.concat([df_resumen_pettitt,df_tem], axis = 0)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)

        fig = plt.gcf()
        figures.append(fig)
        plt.close(fig)
        #plt.show()

    #df_resumen_pettitt.columns = ['h','cp','p','U','mu1', 'mu2','Name']
    return figures