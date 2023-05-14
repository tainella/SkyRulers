from shiny import App, ui, render
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

#shiny run --reload C:\My_files\S7\app.py

type_of_engine = ['CF34-8E5', 'CFM56-7B26', 'CFM56-5B4', 'CFM56-5B3', 'CFM56-7B27/B1']
parametr = ['BRAT','DEGT', 'DELFN', 'DELN1', 'DELVSV', 'DPOIL', 'EGTC', 'EGTHDM', 'EGTHDM_D',
            'GEGTMC', 'GN2MC', 'GPCN25', 'GWFM', 'PCN12', 'PCN12I', 'PCN1AR', 'PCN1BR', 'PCN1K',
            'PCN2C', 'SLOATL', 'SLOATL_D', 'VSVNOM', 'WBE', 'WBI', 'WFMP', 'ZPCN25_D', 'ZT49_D',
            'ZTLA_D', 'ZTNAC_D', 'ZWF36_D']
phase_of_flight = ['take-off', 'cruise']

app_ui = ui.page_fluid(ui.h1("Predictive calculation of engine parameters"),
                       ui.panel_title(ui.input_file("file1", "Choose a csv file to upload:", multiple=False)
                       ),
                       ui.input_date_range("date_range", "Date range input"),
                       ui.layout_sidebar(
                            ui.panel_sidebar(
                                ui.input_selectize("type", "Engine type", type_of_engine),
                                ui.input_selectize("parametr_el", "Parameter for rendering", parametr),
                                ui.input_radio_buttons("x3", "Flight phase", phase_of_flight)
                            ),
                            ui.panel_main(
                                #ui.h1("Plots should be here"),
                                ui.output_plot("a_scatter_plot"),
                            ),
                       ),
)   

def server(input, output, session):
    
    # Надо как-то получить имя самого файла для проверки на csv

    def file_content():
        file = input.file1()
        if not file:
            return 
        if file[0]["type"] not in  ["text/csv", "xml"]:
            return "Wrong file extension"
        # if filename.ends_with()
        return pd.read_csv(file[0]["datapath"])
    
    # НЕ могу победить координаты по осям
    @output
    @render.text
    def time_scale():
        print(input.date_range())
        return input.date_range()
    
    # Понять, как выбрать правильно значения параметра для графика из файла
    @output
    @render.plot
    def a_scatter_plot():
        df = file_content()
        if isinstance(df, pd.DataFrame): 
            if len(df.columns.to_list()) == 3:
                pred = df['predictions']
                true_val = df['true']

                #time = time_scale() #шкала времени

                #add lines to plot
                plt.plot(true_val, label='original_data', color='green')
                plt.plot(pred, label='predicted_data', color='red')

                # значения оси времени
                # datelist = pd.date_range(time_scale()[0], time_scale()[1]).tolist()
                # plt.xticks(datelist)

                #names of axes
                plt.xlabel('time')
                plt.ylabel(input.parametr_el())

                #place legend on the plot
                plt.legend( title='Metric') 

                #plt.show()
                return plt.plot(true_val, label='original_data', color='green'), plt.plot(pred, label='predicted_data', color='red')
            else:
                pred = df['predictions']

                #time = time_scale() #шкала времени

                #add lines to plot
                plt.plot(pred, label='predicted_data', color='green')

                # значения оси времени
                # datelist = pd.date_range(time_scale()[0], time_scale()[1]).tolist()
                # plt.xticks(datelist)

                #names of axes
                plt.xlabel('time')
                plt.ylabel(input.parametr_el())

                #place legend on the plot
                plt.legend( title='Metric') 

                #plt.show()
                return plt.plot(pred, label='predicted_data', color='green')


        

app = App(app_ui, server)