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


from loguru import logger

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

def preprocess_file(df, to_categorical, need_features):
    #Пропуски в полученных данных
    df = df.fillna(0)

    #отсортировать колонки в правильном порядке, если неправильно csv
    df = df[sorted(df.columns)]
    
    #виды фичей 
    numerical = list(set(df.columns.to_list()) - set(to_categorical))
    
    #перевести в систему СИ
    df = to_CI(df)

    #исправить типы данных категориальных фичей
    scaled_features_df = deepcopy(df[numerical])
    for cl in to_categorical:
        
        df[cl] = df[cl].astype(object)
        #One Hot Encoding
        one_hot = pd.get_dummies(df[cl], prefix = cl)
        scaled_features_df = scaled_features_df.join(one_hot)
    df = deepcopy(scaled_features_df)

    #проверка что в переданном файле есть всё что нам нужно
    missed_cl = []
    for cl in need_features:
        if cl not in df.columns.to_list():
            missed_cl.append(cl)
    if len(missed_cl) > 0:
        return missed_cl
    
    #удалить лишние
    drop_features = list(set(df.columns.to_list()) - set(need_features))
    df = df.drop(drop_features, axis = 1)
    
    return df