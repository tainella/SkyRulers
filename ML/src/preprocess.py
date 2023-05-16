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

def preprocess_file(df, to_categorical, need_features):
    #проверка что в переданном файле есть всё что нам нужно
    for cl in need_features:
        if cl not in df.columns.to_list():
            print('ОШИБКА ОШИБКА ОШИБКА')
    drop_features = list(set(df.columns.to_list()) - set(need_features))
    #удалить лишние
    df = df.drop(drop_features, axis = 1)

    #Пропуски в полученных данных
    if sum(df.isna()) > 0:
        print('Данные содержат пропуски, результат подсчета будет не точен')
        df = df.fillna(0)

    #отсортировать колонки в правильном порядке, если неправильно csv
    df = df[sorted(df.columns)]
    
    #виды фичей 
    numerical = list(set(df.columns.to_list()) - set(to_categorical))
    
    #перевести в систему СИ
    df = to_CI(df)
    
    #скалировать данные
    scaled_features = scale(df[numerical].values)
    scaled_features_df = pd.DataFrame(scaled_features, index=df[numerical].index, columns=df[numerical].columns)
    
    #исправить типы данных категориальных фичей
    for cl in to_categorical:
        df[cl] = df[cl].astype(object)
        #One Hot Encoding
        one_hot = pd.get_dummies(df[cl])
        scaled_features_df = scaled_features_df.join(one_hot)
    
    return scaled_features_df