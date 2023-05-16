from shiny import App, ui, render
import shinyswatch
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import seaborn as sns

#shiny run --reload C:\My_files\S7\app.py

type_of_engine = [ "CF34-8E", "CFM56-7", "CFM56-5B"]
parametr = ['BRAT','DEGT', 'DELFN', 'DELN1', 'DELVSV', 'DPOIL', 'EGTC', 'EGTHDM', 'EGTHDM_D',
            'GEGTMC', 'GN2MC', 'GPCN25', 'GWFM', 'PCN12', 'PCN12I', 'PCN1AR', 'PCN1BR', 'PCN1K',
            'PCN2C', 'SLOATL', 'SLOATL_D', 'VSVNOM', 'WBE', 'WBI', 'WFMP', 'ZPCN25_D', 'ZT49_D',
            'ZTLA_D', 'ZTNAC_D', 'ZWF36_D']
phase_of_flight = ['take-off', 'cruise']

app_ui = ui.page_fluid(shinyswatch.theme.superhero(),
                       ui.h2("Predictive calculation of engine parameters"),
                       #ui.panel_title(ui.input_file("file1", "Choose a csv file to upload:", multiple=False)
                       ui.layout_sidebar(
                            ui.panel_sidebar(
                                ui.input_file("file1", "Choose a csv file to upload:", multiple=False),
                                ui.input_date_range("range_of_date", "Date range input"),
                                ui.input_selectize("type", "Engine family", type_of_engine),
                                ui.input_selectize("parametr_el", "Parameter for rendering", parametr),
                                ui.input_radio_buttons("x3", "Flight phase", phase_of_flight)
                            ),
                            ui.panel_main(
                                #ui.h1(datetime.isocalendar()),
                                ui.output_plot("a_scatter_plot"),
                            ),
                       ),
)   

def server(input, output, session):
    def file_content():
        file = input.file1()
        if not file:
            return 
        if file[0]["type"] not in  ["text/csv", "xml"]:
            return "Wrong file extension"
        return pd.read_csv(file[0]["datapath"],parse_dates=True)
    
    @output
    @render.plot
    def a_scatter_plot():
        df = file_content()
        if isinstance(df, pd.DataFrame): 
            if len(df.columns.to_list()) == 3:
                # pred = df['predictions']
                # true_val = df['true']

                # #add lines to plot
                # plt.plot(true_val, label='original_data', color='green')
                # plt.plot(pred, label='predicted_data', color='red')

                # # значения оси времени
                # # datelist = pd.date_range(input.range_of_date[0], input.range_of_date[1], periods=5).tolist()
                # # plt.xticks(datelist)

                # #names of axes
                # plt.xlabel('time')
                # plt.ylabel(input.parametr_el())

                # #place legend on the plot
                # plt.legend( title='Metric') 

                #plt.show()
                #return plt.plot(true_val, label='original_data', color='green'), plt.plot(pred, label='predicted_data', color='red')
                df = pd.read_csv('C:\\My_files\\S7\\test_answer.csv', parse_dates=['flight_datetime'])

                df['flight_datetime']=pd.to_datetime(df['flight_datetime'])
                df.sort_values(by="flight_datetime", inplace=True)
                df.index=df['flight_datetime']
                #df['flight_datetime']=df['flight_datetime'].astype('datetime64[as]')
                fig, ax=plt.subplots()


                data=df.resample('W').sum()
                x_dates=data.index.strftime("%Y-%m-%d").unique()
                ax.set_xticklabels(labels=x_dates, rotation=60)
                sns.set_theme(style="darkgrid")
                sns.lineplot(data=data['predictions'], hue="")
                return fig
            else:
                df = pd.read_csv('C:\\My_files\\S7\\test_answer.csv', parse_dates=['flight_datetime'])

                df['flight_datetime']=pd.to_datetime(df['flight_datetime'])
                df.sort_values(by="flight_datetime", inplace=True)
                df.index=df['flight_datetime']
                #df['flight_datetime']=df['flight_datetime'].astype('datetime64[as]')
                fig, ax=plt.subplots()


                data=df.resample('W').sum()
                x_dates=data.index.strftime("%Y-%m-%d").unique()
                ax.set_xticklabels(labels=x_dates, rotation=60)
                sns.set_theme(style="darkgrid")
                sns.lineplot(data=data['predictions'])
                #plt.show()
                return fig
app = App(app_ui, server)