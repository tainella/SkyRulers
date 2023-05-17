import os
import sys
import getopt
import pandas as pd
import numpy as np
import os
import json

from sklearn.preprocessing import StandardScaler
from math import sqrt

import lightgbm

sys.path.append('../src/')
import preprocess

def run(FLIGHT_MODE, ENGINE_FAMILY, TARGET):
    PATH_TO_CSV = "../data/tmp.csv"
    PATH_TO_RESULT = "/data/result.csv"

    CATEGORICAL_FEATURES = []
    NEED_FEATURES = []
    HAVE_TRUE = False
    REGRESSION = True

    #Получить список категориальных фичей для данного 
    with open('/data/feature_groups.json') as json_file:
        feature_groups_dict = json.load(json_file)
        for item in feature_groups_dict.items():
            if (FLIGHT_MODE in item[0]) and (ENGINE_FAMILY in item[0]) and (TARGET in item[0]):
                CATEGORICAL_FEATURES = item[1]

    #ПОМЕНЯТЬ ЧТОБЫ БЫЛО ДЛЯ РАЗНЫХ ФАЙЛОВ РАЗНОЕ
    with open(f'/data/{FLIGHT_MODE}_{ENGINE_FAMILY}_needed.json') as json_file:
        feature_groups_dict = json.load(json_file)
        for item in feature_groups_dict.items():
            if TARGET == item[0]:
                NEED_FEATURES = item[1]

    #Подготовка данных
    df = pd.read_csv(PATH_TO_CSV)
    if TARGET in df.columns.to_list():
        HAVE_TRUE = True
    
    if TARGET in ['BRAT', 'WBI']:
        REGRESSION = False
    
    X = preprocess.preprocess_file(df, CATEGORICAL_FEATURES, NEED_FEATURES)
    
    if not isinstance(X, list):
        #Выбор модели и подсчет
        if not REGRESSION:
            result_df = pd.DataFrame({'error' : ['Классификация']})
            result_df.to_csv(PATH_TO_RESULT, index = False)
        else:
            model = lightgbm.Booster(model_file=f'../models/{FLIGHT_MODE}_{ENGINE_FAMILY}_{TARGET}.txt')
            y_pred = model.predict(X.values)

            #Подготовка файла результа
            if HAVE_TRUE:
                result_df = pd.DataFrame({
                    'flight_datetime' : df['flight_datetime'],
                    'predictions' : y_pred,
                    'true' : df[TARGET]
                })
            else:
                result_df = pd.DataFrame({
                    'flight_datetime' : df['flight_datetime'],
                    'predictions' : y_pred
                })

            result_df.to_csv(PATH_TO_RESULT, index = False)
    else:
        result_df = pd.DataFrame({'error' : X})
        result_df.to_csv(PATH_TO_RESULT, index = False)

