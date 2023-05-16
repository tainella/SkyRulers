import os
import sys
import getopt
import pandas as pd
import numpy as np
import os
import json

from sklearn.preprocessing import StandardScaler
from math import sqrt

import torch

sys.path.append('../src/')
import preprocess
import LinearModel
import ClassificationModel
from EngineDataset import EngineDataset


if __name__ == "__main__":
    PATH_TO_CSV = "/data/tmp.csv"
    PATH_TO_RESULT = "/data/result.csv"

    FLIGHT_MODE = ""
    ENGINE_FAMILY = ""
    TARGET = ""
    CATEGORICAL_FEATURES = []
    NEED_FEATURES = []
    HAVE_TRUE = False
    REGRESSION = True

    argv = sys.argv[1:]
    try:
        options, args = getopt.getopt(argv, "fm:ef:t",
                                   ["fight_mode=",
                                    "engine_family=",
                                    "target="
                                    ])
    except:
        print("Error Message ")

    for name, value in options:
        if name in ['fm', '--fight_mode']:
            FLIGHT_MODE = value
        elif name in ['ef', '--engine_family']:
            ENGINE_FAMILY = value
        elif name in ['t', '--target']:
            TARGET = value

    #Получить список категориальных фичей для данного 
    with open('../data/feature_groups.json') as json_file:
        feature_groups_dict = json.load(json_file)
        for item in feature_groups_dict.items():
            if (FLIGHT_MODE in item[0]) and (ENGINE_FAMILY in item[0]) and (TARGET in item[0]):
                CATEGORICAL_FEATURES = item[1][0]
                NEED_FEATURES = item[1][1]

    #Подготовка данных
    df = pd.read_csv(PATH_TO_CSV)
    if TARGET in df.columns.to_list():
        HAVE_TRUE = True
    
    if TARGET in ['BRAT', 'WBI']:
        REGRESSION = False
    X = preprocess.preprocess_file(df, CATEGORICAL_FEATURES, NEED_FEATURES)

    #Выбор модели и подсчет
    if REGRESSION:
        model = LinearModel.NN()
    else:
        model = ClassificationModel.NN()
    
    model.load_state_dict(torch.load(f'../models/{FLIGHT_MODE}_{ENGINE_FAMILY}_{TARGET}.pt'))
    model.eval()
    y_pred = model(torch.tensor(df.values, dtype=torch.float)).detach().numpy()

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
