import numpy as np
import pandas as pd
import os

def walsh_test(lista_files, var, alpha=0.05):
    """
    Walsh's Test for Large Sample Sizes
    
    Parameters:
    - data: Array-like object containing the data
    - alpha: Significance level
    
    Returns:
    - outliers: Array containing the indices of the outliers
    """

    for estacion in lista_files:
        data = pd.read_csv(f'../{var}_SALIDAS/DATA_COMPLETA/{estacion}')
        data = data[['Fecha', 'Valor']]; data = data.set_index('Fecha');data.index = pd.to_datetime(data.index)

        data["mes"] = data.index.strftime("%b")
        meses = list(data["mes"].unique())
        
        for mes in meses:
            df_mes = data[data["mes"] == mes]
            df_mes = df_mes.dropna()
            data_mes = sorted(df_mes['Valor'])
            
            n = len(data_mes)
                
            if n <= 60:
                print("Sample size is too small. Walsh's test should not be applied.")
                return []
            elif n <= 220:
                alpha = 0.10
                
            c = int(np.ceil(np.sqrt(2 * n)))
            b2 = 1/alpha
            b = np.sqrt(b2)
            a = (1+b*np.sqrt((c-b2)/(c-1)))/(c-b2-1)
                
            # Step 1: Check if the i smallest points are outliers
            for i in range(n):
                k = i + c
                if data_mes[i] - (1 + a) * data_mes[i + 1] + a * data_mes[k] < 0:
                    outliers_small.append(i)
                elif data_mes[i] - (1 + a) * data_mes[i + 1] + a * data_mes[k] >= 0:
                    if i > 0:
                        thrs_outlier_small =  data_mes[i - 1]
                    else:
                        thrs_outlier_small =  None
                    break
                
            # Step 2: Check if the i largest points are outliers
            for i in range(n,0, -1): 
                k = i + c
                if data_mes[n+1-i] - (1 + a) * data_mes[n - i] + a * data_mes[n +1- k] <= 0:
                    if i < n-1:
                        thrs_outlier_large = data_mes[i + 1]
                    elif i == n-1:
                        thrs_outlier_large = None
                    break
            
            num_outlier_large = (len(df_mes[df_mes['Valor'] >= thrs_outlier_large])/n) * 100
            num_outlier_small = (len(df_mes[df_mes['Valor'] <= thrs_outlier_small])/n) * 100
            
            info_large_outl = (thrs_outlier_large,np.round(num_outlier_large,2))  #tuple with threshold for largest values and its % of outliers 
            info_small_outl = (thrs_outlier_small,np.round(num_outlier_small,2))  #tuple with threshold for small values and its % of outliers
            outliers = {"thrs_small":info_small_outl, "thrs_large": info_large_outl}

            #print(outliers) #(thrs,%)
            
            #Assign Nan to outliers
            
            filtro_mes = data['mes'] == mes
            
            data.loc[filtro_mes & (data['Valor'] >= thrs_outlier_large), 'Valor'] = np.nan
            data.loc[filtro_mes & (data['Valor'] >= thrs_outlier_small), 'Valor'] = np.nan
    
        data.drop('mes',axis=1, inplace=True)
        
        output_file = f'../{var}_SALIDAS/DATA_DEPURADA'
        if not os.path.exists(output_file):
            os.makedirs(output_file)
        
        data.to_csv(f'{output_file}/{estacion}')    

        