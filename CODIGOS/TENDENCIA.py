import numpy as np
import matplotlib.pyplot as plt
import pymannkendall as mk
import pandas as pd

def mann_kendall(lista_files,var):
    figures = []
    numi = 0
    for i in np.arange(numi, len(lista_files), 1):  # llamar datos de las estaciones
        data_est = pd.read_csv(f'../{var}_SALIDAS/DATA_LLENADO/' + lista_files[i])
        data_est = data_est[['Fecha', 'Valor']]; data_est = data_est.set_index('Fecha');data_est.index = pd.to_datetime(data_est.index)
        data_mes = data_est.groupby(data_est.index.strftime("%Y-%m")).sum()
        data_mes.index = pd.to_datetime(data_mes.index)
    
        dates = data_mes.index
        data_pre = data_mes["Valor"].values
    
        # Realiza el test de Mann-Kendall
        trend, h, p, z, Tau, s, var_s, slope, intercept = mk.original_test(data_pre)
        slope_r = np.round(slope, 3)
    
        # Imprime los resultados
        # print("p-valor:", p)
    
        plt.figure()
    
        # Grafica los datos
        plt.plot(dates, data_pre, label='Datos')
    
        # Agrega la línea de tendencia
        trend_line = slope * np.arange(len(data_pre)) + intercept
        plt.plot(dates, trend_line, color='red', label='Tendencia')
        plt.text(0.75, 0.83, f'p-valor: {p:.4f}', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')
        plt.text(0.75, 0.77, f'Pendiente: {slope_r}', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')
    
        plt.legend()
        plt.title(lista_files[i][:-4])
        plt.xlabel('Fecha')
        plt.ylabel('mm/mes')
    
        fig = plt.gcf()
        figures.append(fig)
        plt.close(fig)
        # Guarda la gráfica en un archivo 
        # plt.savefig(f'tendencia_{lista_files[i][:-4].png')
    
    return figures