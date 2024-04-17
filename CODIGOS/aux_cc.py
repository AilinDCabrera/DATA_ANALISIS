from scipy.interpolate import interp1d
#from pygam import LinearGAM
import pandas as pd
import xarray as xr
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)


def crear_df_modelos(modelos,clon,clat,fecha_ini,fecha_fin,var = 'pr',multi = 86400):
    dataframe_modelos = pd.DataFrame([])
    for i in range(0,len(modelos),1):
        modelos[i] = modelos[i].sel(time=slice(fecha_ini, fecha_fin))
        try:
            modelos[i] = modelos[i].assign_coords(time = modelos[i].indexes['time'].to_datetimeindex())
        except:
            pass
        df_modelo = modelos[i][var].sel(lon = clon, lat = clat, method = 'nearest').to_dataframe()[[var]]
        dataframe_modelos = pd.concat([dataframe_modelos,df_modelo],axis = 1)
        
    dataframe_modelos.index = pd.to_datetime(dataframe_modelos.index)
    dataframe_modelos = dataframe_modelos * multi
    dataframe_modelos = pd.DataFrame(dataframe_modelos.mean(axis = 1).round(1), columns = ['Modelo'])
    dataframe_modelos = dataframe_modelos.replace(0.1,0)

    return dataframe_modelos


class linear_reg(object):
    def fit(obs, modeled, var = 'pr'):
        data_ls = pd.concat([obs,modeled[['Modelo']]], axis = 1)
        data_ls['month'] = data_ls.index.strftime('%m')
        if var == 'pr':
            data_ls_month = data_ls.groupby(data_ls.index.strftime('%Y-%m')).sum(); data_ls_month.index = pd.to_datetime(data_ls_month.index)
        else:
            data_ls_month = data_ls.groupby(data_ls.index.strftime('%Y-%m')).mean(); data_ls_month.index = pd.to_datetime(data_ls_month.index)
        data_ls_month = data_ls_month.groupby(data_ls_month.index.strftime('%m')).mean()
        factor_ls_month = data_ls_month['Valor']/data_ls_month['Modelo']
        
        correction = factor_ls_month
        return correction

    def error(obs, modeled,correction):
        modeled['month']  = modeled.index.strftime('%m')
        modeled['factor'] = modeled['month'].map(correction)
        modeled = modeled.round(1)
        df_modelo = pd.DataFrame([])
        df_modelo['pred'] = modeled['Modelo'] * modeled['factor']
        df_modelo.index   = pd.to_datetime(df_modelo.index.strftime('%Y-%m-%d'))
        df_unido = pd.concat([obs.rename({'Valor':'real'},axis =1),df_modelo],axis = 1)

        rmse = np.sqrt(((df_unido['real'] - df_unido['pred'])**2).sum()/len(df_unido))
        corr = df_unido.corr().values[0,1].round(2)
        return rmse, corr

    def predict(modeled,correction):
        modeled['month']  = modeled.index.strftime('%m')
        modeled['factor'] = modeled['month'].map(correction)
        modeled['pred']   = modeled['Modelo'] * modeled['factor']
        modeled = modeled.round(2)
        return modeled[['pred']]


class quantile_reg(object):
    def fit(obs,modeled):

        obs = obs[np.logical_not(np.isnan(obs))]
        data_size = obs.shape[0]

        obs_sorted = np.sort(obs).squeeze()
        train_sorted = np.sort(np.array(modeled).squeeze())

        train_interp = interp1d(np.arange(1, train_sorted.shape[0] + 1), train_sorted)
        train_sorted = train_interp(np.linspace(1, train_sorted.shape[0], data_size))

        correction = np.array(train_sorted - obs_sorted)
        return correction

    def error(obs,modeled,predict_qm):
        modeled['pred'] = predict_qm
        modeled.index   = pd.to_datetime(modeled.index.strftime('%Y-%m-%d'))
        df_unido = pd.concat([modeled,obs],axis = 1)
        rmse = np.sqrt(((df_unido['Valor'] - df_unido['pred'])**2).sum()/len(df_unido))
        corr = df_unido.corr().values[0,1].round(2)
        return rmse, corr


    def predict(modeled,correction):
        modeled = np.array(modeled).reshape(-1, ).tolist()
        model_sorted = sorted(modeled)
        adjusted = []
        for i in range(len(model_sorted)):
            rank = model_sorted.index(modeled[i]) / float(len(model_sorted))
            rank = int(rank * correction.shape[0])
            adjusted.append(modeled[i] - correction[rank])
            
        adjusted = np.array(adjusted)
        return np.where(adjusted<0,0,adjusted)


def qm_mensual(data_org,dataframe_modelos,dataframe_modelos_hist):
    months = ["ene", "feb", "mar", 'abr', "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
    #months = ["ene.", "feb.", "mar.", 'abr.', "may.", "jun.", "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]
    dataframe_modelos_down = pd.DataFrame([])
    for i in np.arange(0,len(months),1):
        coef_qm_mes       = quantile_reg.fit(data_org[data_org['mes'] == months[i]]['Valor'].values,dataframe_modelos_hist[dataframe_modelos_hist['mes'] == months[i]]['Modelo'].values)
        predict_qm_mes = quantile_reg.predict(dataframe_modelos.copy()[dataframe_modelos['mes'] == months[i]]['Modelo'].values,coef_qm_mes)

        df_aux = pd.DataFrame(np.c_[predict_qm_mes], columns = ['Valor'])
        df_aux['Fecha'] = dataframe_modelos.copy()[dataframe_modelos['mes'] == months[i]].index
        df_aux = df_aux.set_index('Fecha')

        dataframe_modelos_down = pd.concat([dataframe_modelos_down,df_aux],axis = 0)
        
    return dataframe_modelos_down
