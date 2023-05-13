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
                                ui.input_selectize("parametr", "Parameter for rendering", parametr),
                                ui.input_radio_buttons("x3", "Flight phase", phase_of_flight)
                            ),
                            ui.panel_main(
                                #ui.h1("Plots should be here"),
                                ui.output_plot("a_scatter_plot"),
                            ),
                       ),
)   

def server(input, output, session):
    
    @output
    @render.text
    def file_content():
        MAX_SIZE = 500000
        file_infos = input.file1()
        if not file_infos:
            return

        out_str = ""
        for file_info in file_infos:
            out_str += (
                "=" * 47
                + "\n"
                + file_info["name"]
                + "\nMIME type: "
                #+ str(mimetypes.guess_type(file_info["name"])[0])
            )
            if file_info["size"] > MAX_SIZE:
                out_str += f"\nTruncating at {MAX_SIZE} bytes."

            out_str += "\n" + "=" * 47 + "\n"

            if input.type() == "Text":
                with open(file_info["datapath"], "r") as f:
                    out_str += f.read(MAX_SIZE)
            else:
                with open(file_info["datapath"], "rb") as f:
                    data = f.read(MAX_SIZE)
                    #out_str += format_hexdump(data)

        return out_str
    
    # НЕ могу победить координаты по осям
    @output
    @render.text
    def time_scale():
        print(input.date_range())
        return input.date_range()
    
    # Не могу победить импорт названия параметра из списка в обозначение оси на графике
    @output
    @render.text
    def parametr():
        return f"parametr {input.parametr()}"

    @output
    @render.plot
    def a_scatter_plot():
        data = pd.DataFrame({'Original_data':[11, 17, 16, 18, 22, 25, 26, 24, 29], #исходные значения параметра
        'Predicted_data':[5, 7, 7, 9, 12, 9, 9, 4, 8] #вычисленные значения параметра
        })

        original_data = data["Original_data"]
        predicted_data = data["Predicted_data"]

        #time = time_scale() #шкала времени

        #add lines to plot
        plt.plot(original_data, label='original_data', color='green')
        plt.plot(predicted_data, label='predicted_data', color='red')

        # значения оси времени
        # datelist = pd.date_range(time_scale()[0], time_scale()[1]).tolist()
        # plt.xticks(datelist)

        #names of axes
        plt.xlabel('time')
        plt.ylabel("parametr")

        #place legend on the plot
        plt.legend( title='Metric') 

        #plt.show()
        return plt.plot(original_data, label='original_data', color='green'), plt.plot(predicted_data, label='predicted_data', color='red')

app = App(app_ui, server)