import pandas as pd
import numpy as np
import os
from copy import deepcopy

import matplotlib.pyplot as plt
import seaborn as sns

import pint
from pint import UnitRegistry

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from math import sqrt

def scale(data):
    # fit scaler
    scaler = StandardScaler()
    scaler = scaler.fit(data)
    # transform train
    data_scaled = scaler.transform(data)
    return data_scaled

# inverse scaling for a forecasted value
def invert_scale(scaler, data):
    inverted = scaler.inverse_transform(data)
    return inverted

def to_CI(df):
    def celc(x):
        ureg = UnitRegistry()
        Q_ = ureg.Quantity
        home = Q_(x, ureg.degC)
        return home.to('degK')

    def ream(x):
        ureg = UnitRegistry()
        Q_ = ureg.Quantity
        home = Q_(x, ureg.degR)
        return home.to('degK')
    
    celc_features = ['ZT1AB', 'ZTNAC', 'ZTOIL', 'ZT1A', 'GEGTMC', 'ZTNAC_D']
    ream_features = ['ZTAMB']
    
    for cl in celc_features:
        if cl in df.columns.to_list():
            df[cl] = pd.Series(celc(df[cl].values))
            
    for cl in ream_features:
        if cl in df.columns.to_list():
            df[cl] = pd.Series(ream(df[cl].values))
    
    return df

def preprocess_file(df, corr_ther, targets):
    def delete_corr(df, ther):
        was_corr = []
        corr = df.corr()
        for row in corr.iterrows():
            for v_ind in range(len(row[1])):
                if row[1][v_ind] > ther and row[1][v_ind] < 1: #ПЕРЕСЧИТАТЬ
                    if (row[0] not in was_corr) and (row[1].index[v_ind] not in was_corr):
                        print(row[0], row[1].index[v_ind], row[1][v_ind])
                        was_corr.append(row[0])
        print(len(was_corr))
        return was_corr
    #удалить лишние
    df = df.drop(['flight_datetime', 'engine_id'], axis = 1)
    
    #виды фичей
    to_categorical = ['IAIE','IBE','IBP','IAI','BRAT','engine_type','n1_modifier',
                  'IVS12','number_blades','engine_position','engine_family', 'manufacturer',
                  'aircraft_family','aircraft_type','aircraft_grp','ac_manufacturer']
    numerical = list(set(df.columns.to_list()) - set(to_categorical) - set(targets))
    
    #убрать те у которых больше 2/3 пропущены значения
    for cl in numerical:
        if (cl in df.columns.to_list()) and (len(df[cl]) * 2 / 3 < df[cl].isna().sum()):
            df = df.drop([cl], axis = 1)
    #обновить список числовых фияей
    numerical = list(set(df.columns.to_list()) - set(to_categorical))
    #заполнить оставшиеся пропуски нулями
    df = df.fillna(0)
    
    #перевести в систему СИ
    df = to_CI(df)

    #убрать скоррелированные фичи
    was_corr = ['ZXM', 'DELN1', 'EGTHDM_D', 'PCN12', 'ZPCN12', 'PCN1AR']
    df.drop(was_corr, axis = 1)
    #обновить список числовых фияей
    numerical = list(set(df.columns.to_list()) - set(to_categorical) - set(targets))
    
    #скалировать данные
    scaled_features = StandardScaler().fit_transform(df[numerical].values)
    scaled_features_df = pd.DataFrame(scaled_features, index=df[numerical].index, columns=df[numerical].columns)
    
    scaled_features_df
    #исправить типы данных категориальных фичей
    for cl in to_categorical:
        if cl in df.columns.to_list():
            df[cl] = df[cl].astype(object)
            #One Hot Encoding
            one_hot = pd.get_dummies(df[cl])
            scaled_features_df = pd.concat([scaled_features_df,one_hot], axis=1)
    
    scaled_features_df = pd.concat([scaled_features_df,df[targets]], axis=1)
    
    return scaled_features_df
