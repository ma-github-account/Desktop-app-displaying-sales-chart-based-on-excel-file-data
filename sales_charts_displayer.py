


import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
    
root = tk.Tk()
root.title('Sales chart')
root.columnconfigure(0, weight=1)

ttk.Label(
  root,
  text="Sales chart",
  font=("TkDefaultFont", 16)
).grid()

interval_info = ttk.LabelFrame(root, text='Month or week interval choice setting')
interval_info.grid(sticky=(tk.W + tk.E))
for i in range(2):
  interval_info.columnconfigure(i, weight=1 )

interval_radiobutton_value = tk.StringVar()
ttk.Label(interval_info , text='Select month or week interval').grid(row=0, column=0)
labframe = ttk.Frame(interval_info)
for lab in ('Month', 'Week'):
  ttk.Radiobutton(
    labframe, value=lab, text=lab, variable=interval_radiobutton_value
).pack(side=tk.LEFT, expand=True)
labframe.grid(row=1, column=0, sticky=(tk.W + tk.E))

chart_settings_info = ttk.LabelFrame(root, text='Chart display settings')
chart_settings_info.grid(sticky=(tk.W + tk.E))
for i in range(2):
  chart_settings_info.columnconfigure(i, weight=1 )

xlabel_checkbutton_value = tk.BooleanVar(value=False)
ttk.Checkbutton(
  chart_settings_info, variable=xlabel_checkbutton_value,
  text='Show x label'
).grid(row=5, column=0, sticky=tk.W, pady=5)

ylabel_checkbutton_value = tk.BooleanVar(value=False)
ttk.Checkbutton(
  chart_settings_info, variable=ylabel_checkbutton_value,
  text='Show y label'
).grid(row=6, column=0, sticky=tk.W, pady=5)

title_checkbutton_value = tk.BooleanVar(value=False)
ttk.Checkbutton(
  chart_settings_info, variable=title_checkbutton_value,
  text='Show title'
).grid(row=5, column=1, sticky=tk.W, pady=5)

legend_checkbutton_value = tk.BooleanVar(value=False)
ttk.Checkbutton(
  chart_settings_info, variable=legend_checkbutton_value,
  text='Show legend'
).grid(row=6, column=1, sticky=tk.W, pady=5)

reload_button_frame = ttk.LabelFrame(root, text='Reload button')
reload_button_frame.grid(sticky=(tk.W + tk.E))
for i in range(3):
  reload_button_frame.columnconfigure(i, weight=1 )

ttk.Label(reload_button_frame , text='Click Reload button to refresh chart after setting changes').pack(side=tk.TOP)
Reload_button = ttk.Button(reload_button_frame, text='RELOAD')
Reload_button.pack(side=tk.LEFT)

def display_chart(interval, title, xlabel_option, ylabel_option, legend_option):

	fig = Figure(figsize = (10, 8),
	            dpi = 100)
	
	stock = pd.read_csv('sales_data.csv', header=None, delimiter=',')
	
	stock.columns = ['date','Model1','Model2','Model3']

	if interval == "Month":
	
		stock['date'] = pd.to_datetime(stock['date'], format='%d-%m-%Y')[-30:]

	elif interval == "Week":

		stock['date'] = pd.to_datetime(stock['date'], format='%d-%m-%Y')[-7:]

	else:
	
		stock['date'] = pd.to_datetime(stock['date'], format='%d-%m-%Y')[0:]
	
	indexed_stock = stock.set_index('date')
	ts1 = indexed_stock['Model1']
	ts2 = indexed_stock['Model2']
	ts3 = indexed_stock['Model3']
	
	plot1 = fig.add_subplot(111)
	
	plot1.plot(ts1, label='Model1',color='green')
	plot1.plot(ts2, label='Model2',color='blue')
	plot1.plot(ts3, label='Model3',color='red')

	if interval == "Month":
	
		plot1.xaxis.set_major_locator(mdates.DayLocator(interval=5))

	elif interval == "Week":

		plot1.xaxis.set_major_locator(mdates.DayLocator(interval=2))

	else:
	
		plot1.xaxis.set_major_locator(mdates.DayLocator(interval=5))

	plot1.title.set_text(title)

	if legend_option == True:

		plot1.legend(loc='upper left')

	if xlabel_option == True:

		plot1.set_xlabel('Date')

	if ylabel_option == True:

		plot1.set_ylabel('Amount of sold units')

	return fig

fig = display_chart(interval = "Month", title = "Sales chart", xlabel_option = True, ylabel_option = True, legend_option = True)

canvas = FigureCanvasTkAgg(fig, master = root)

canvas.draw()

canvas.get_tk_widget().grid(row=20, column=0)

def on_reset():

	interval_value = interval_radiobutton_value.get()
	xlabel_value = xlabel_checkbutton_value.get()
	ylabel_value = ylabel_checkbutton_value.get()
	title_value = title_checkbutton_value.get()
	legend_value = legend_checkbutton_value.get()

	if title_value == True:

		title_string = "Sales chart"

	else:

		title_string = ""

	fig = display_chart(interval = interval_value, title = title_string, xlabel_option = xlabel_value, ylabel_option = ylabel_value, legend_option = legend_value)
	
	canvas = FigureCanvasTkAgg(fig, master = root)
	
	canvas.draw()
	
	canvas.get_tk_widget().grid(row=20, column=0)

Reload_button.configure(command=on_reset)

root.mainloop()


























