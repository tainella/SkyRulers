from shiny import App, ui, render, reactive
import shinyswatch
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from datetime import date
import seaborn as sns
import numpy as np
import os
import sys
from loguru import logger

sys.path.append('../src/')
import pipeline

phase_of_flight = ['takeoff', 'cruise']
type_of_engine = [ "CF34-8E", "CFM56-7", "CFM56-5B"]
parametr = {"takeoff_CFM56-7": 
            ['DELFN',
            'DELN1',
            'EGTHDM',
            'EGTHDM_D',
            'PCN12',
            'PCN12I',
            'PCN1AR',
            'PCN1BR',
            'PCN1K',
            'SLOATL',
            'SLOATL_D',
            'ZPCN25_D',
            'ZT49_D'],

            "takeoff_CFM56-5B":
            ['DELFN',
            'DELN1',
            'EGTHDM',
            'EGTHDM_D',
            'PCN12',
            'PCN12I',
            'PCN1AR',
            'PCN1BR',
            'PCN1K',
            'SLOATL',
            'SLOATL_D',
            'WBE',
            'ZPCN25_D',
            'ZT49_D'],

            "takeoff_CF34-8E": 
            ['EGTHDM',
            'EGTHDM_D',
            'PCN12',
            'PCN1K',
            'SLOATL',
            'SLOATL_D',
            'ZPCN25_D',
            'ZT49_D',
            'ZWF36_D'],

            "cruise_CFM56-7": 
            ['DEGT',
            'DPOIL',
            'EGTC',
            'EGTHDM',
            'GEGTMC',
            'GN2MC',
            'GPCN25',
            'GWFM',
            'PCN12',
            'PCN12I',
            'PCN1K',
            'PCN2C',
            'SLOATL',
            'WBI',
            'WFMP',
            'ZPCN25_D',
            'ZT49_D',
            'ZWF36_D'],

            "cruise_CFM56-5B" : 
            ['DEGT',
            'DELVSV',
            'DPOIL',
            'EGTC',
            'EGTHDM',
            'GEGTMC',
            'GN2MC',
            'GPCN25',
            'GWFM',
            'PCN12',
            'PCN12I',
            'PCN1K',
            'PCN2C',
            'SLOATL',
            'VSVNOM',
            'WBE',
            'WBI',
            'WFMP',
            'ZPCN25_D',
            'ZT49_D',
            'ZTNAC_D',
            'ZWF36_D'],

            "cruise_CF34-8E":  
            ['DEGT',
            'EGTC',
            'GPCN25',
            'GWFM',
            'PCN12',
            'PCN12I',
            'PCN1K',
            'PCN2C',
            'WBI',
            'WFMP',
            'ZPCN25_D',
            'ZT49_D',
            'ZTLA_D',
            'ZWF36_D']}

app_ui = ui.page_fluid(shinyswatch.theme.superhero(),
                       ui.h2("Predictive calculation of engine parameters"),
                       ui.layout_sidebar(
                            ui.panel_sidebar(
                                ui.input_file("file1", "Choose a csv file to upload:", multiple=False),
                                ui.input_radio_buttons("flight_phase", "Flight phase", phase_of_flight),
                                ui.input_selectize("family", "Engine family", type_of_engine),
                                ui.output_ui("ui_selectize"),
                                ui.input_date_range("range_of_date", "Date range input"),
                            ),
                            ui.panel_main(
                                # Вывод текста при необходимости отладки
                                ui.output_text("my_text"),
                                ui.output_plot("line_plot")
                            ),
                       ),
)

def server(input, output, session):
    
    @output
    @render.ui
    def ui_selectize():
        x=selected_parametr()
        return ui.input_selectize(
            "in_select",
            label=f"Select parametr ({len(x)} options)",
            choices=x,
            selected=None,
        )
    
    # Вывод текста при необходимости отладки
    @output
    @render.text
    def my_text():
        if not isinstance(file_content(), pd.DataFrame):
            return "Загрузите файл для начала работы"
        df = file_content()
        if "error" in df.columns.to_list():
            buf = ','.join(df['error'])
            return f"НЕ ХВАТАЕТ КОЛОНОК: \n {buf}"

    def selected_parametr():
        return parametr[f"{input.flight_phase()}_{input.family()}"]
    
    def file_content():
        file = input.file1()
        if not file:
            return
        df = pd.read_csv(file[0]["datapath"],parse_dates=True)
        
        if file[0]["type"] not in ["text/csv", "xml"]:
            return "Wrong file extension"
        df.to_csv('../data/tmp.csv', index = False)
        pipeline.run(input.flight_phase(), input.family(), input.in_select())
        df = pd.read_csv('../data/result.csv')
        return df

    @output
    @render.plot
    def line_plot():
        try:
            df = file_content()
            if isinstance(df, pd.DataFrame):
                if "error" in df.columns.to_list():
                    logger.exception("НЕПРАВИЛЬНЫЕ КОЛОНКИ", df['error'])
                elif len(df.columns.to_list()) == 3:

                    df['flight_datetime']=pd.to_datetime(df['flight_datetime'])
                    df = df.loc[(df['flight_datetime'] >= np.datetime64(input.range_of_date()[0])) & (((df['flight_datetime'])) <= np.datetime64(input.range_of_date()[1]))]

                    df.sort_values(by="flight_datetime", inplace=True)
                    df.index=df['flight_datetime']
                    fig, ax=plt.subplots()

                    data=df.resample('W').sum()
                    x_dates=data.index.strftime("%Y-%m-%d").unique()
                    ax.set_xticklabels(labels=x_dates, rotation=20)
                    ax1 = sns.lineplot(data=data['true'], color='g', label = "true values")
                    ax = sns.lineplot(data=data['predictions'], color='r', label = 'prediction')
                    ax.set (xlabel='Time', ylabel=input.in_select(), title='Sensor readings')
                    sns.set_theme(style="darkgrid")
                    plt.legend(title='Metric')
                    return fig
                
                else:
                    logger.exception('!!!!!!!!!!!!!!', df.columns.to_list())
                    df['flight_datetime']=pd.to_datetime(df['flight_datetime'])
                    df = df.loc[(df['flight_datetime'] >= np.datetime64(input.range_of_date()[0])) & (((df['flight_datetime'])) <= np.datetime64(input.range_of_date()[1]))]
                    
                    df.sort_values(by="flight_datetime", inplace=True)
                    df.index=df['flight_datetime']
                    fig, ax=plt.subplots()

                    data=df.resample('W').sum()
                    x_dates=data.index.strftime("%Y-%m-%d").unique()
                    ax.set_xticklabels(labels=x_dates, rotation=20)
                    ax = sns.lineplot(data=data['predictions'], color='r', label = 'prediction')
                    ax.set(xlabel='Time', ylabel=input.in_select(), title='Sensor readings')
                    sns.set_theme(style="darkgrid")
                    plt.legend(title='Metric')
                    return fig
        except:
            logger.exception("AAAAA")
            
app = App(app_ui, server)