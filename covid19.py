import numpy as np
import pandas as pd
import bokeh.plotting as bkp
import numpy as np
from datetime import date
from bokeh.models import (HoverTool, ColumnDataSource, ColorBar,
                          LogColorMapper, LogTicker)
from bokeh.palettes import Magma256, Category10
from bokeh.io import curdoc
from bokeh.themes import Theme
from bokeh.layouts import Column

curdoc().theme = Theme('/Users/mburger/.bokeh/bokeh.yml')

def makedate(datestr):
    result = [int(x) for x in datestr.split('-')]

    return date(*result)


data = pd.read_csv('https://covid.ourworldindata.org/data/ecdc/full_data.csv')
data['Date'] = data.date.apply(lambda x:
                            date(*[int(y) for y in x.split('-')]))

codes_to_plot = ['United States', 'Sweden', 'United Kingdom', 'Spain']
tooltips = [('Country', '@location'),
            ('Date', '@date'),
            ('New Cases', '@new_cases'),
            ('Total Cases', '@total_cases')]

fig0 = bkp.figure(plot_width=1200, plot_height=600,
                  title='Total Cases',
                  x_axis_label='Date',
                  y_axis_label='# Cases',
                  x_axis_type='datetime', y_axis_type='log',
                  tooltips=tooltips)

colors = (c for c in Category10[10])
for code in codes_to_plot:
    plotdata = ColumnDataSource(data[data.location == code])
    c = next(colors)
    fig0.circle('Date', 'total_cases', source=plotdata, color=c,
               legend_label=code)
    fig0.line('Date', 'total_cases', source=plotdata, color=c,
              legend_label=code)
print('figure 0')

fig1 = bkp.figure(plot_width=1200, plot_height=600,
                  title='New Cases',
                  x_axis_label='Date',
                  y_axis_label='# Cases',
                  x_axis_type='datetime', y_axis_type='log',
                  tooltips=tooltips)

colors = (c for c in Category10[10])
for code in codes_to_plot:
    plotdata = ColumnDataSource(data[data.location == code])
    c = next(colors)
    fig1.circle('Date', 'new_cases', source=plotdata, color=c,
                legend_label=code)
    # fig1.line('Date', 'new_cases', source=plotdata, color=c,
    #            legend_label=code)
    c_mean = data[data.location == code].new_cases.rolling(5).mean().fillna(0)
    fig1.line(x=data[data.location == code].Date, y=c_mean, color=c, legend_label=code)
print('figure 1')

fig2 = bkp.figure(plot_width=1200, plot_height=600,
                  title='New Cases vs. Total Cases',
                  x_axis_label='Total Cases',
                  y_axis_label='New Cases',
                  x_axis_type='log', y_axis_type='log',
                  tooltips=tooltips)

colors = (c for c in Category10[10])
for code in codes_to_plot:
    plotdata = ColumnDataSource(data[data.location == code])
    c = next(colors)
    fig2.circle('total_cases', 'new_cases', source=plotdata, color=c,
                legend_label=code)
    # fig2.line('total_cases', 'new_cases', source=plotdata, color=c,
    #             legend_label=code)
    c_mean = data[data.location == code].new_cases.rolling(5).mean().fillna(0)
    fig2.line(x=data[data.location == code].total_cases, y=c_mean, color=c, legend_label=code)
print('figure 2')

tooltips = [('Country', '@location'),
            ('Date', '@date'),
            ('New Deaths', '@new_deaths'),
            ('Total Deaths', '@total_deaths')]

fig3 = bkp.figure(plot_width=1200, plot_height=600,
                  title='Total Deaths',
                  x_axis_label='Date',
                  y_axis_label='# Deaths',
                  x_axis_type='datetime', y_axis_type='log',
                  tooltips=tooltips)

colors = (c for c in Category10[10])
for code in codes_to_plot:
    plotdata = ColumnDataSource(data[data.location == code])
    c = next(colors)
    fig3.circle('Date', 'total_deaths', source=plotdata, color=c,
                legend_label=code)
    fig3.line('Date', 'total_deaths', color=c, source=plotdata, 
              legend_label=code)
print('figure 3')

fig4 = bkp.figure(plot_width=1200, plot_height=600,
                  title='New Deaths',
                  x_axis_label='Date',
                  y_axis_label='# Deaths',
                  x_axis_type='datetime', y_axis_type='log',
                  tooltips=tooltips)

colors = (c for c in Category10[10])
for code in codes_to_plot:
    plotdata = ColumnDataSource(data[data.location == code])
    c = next(colors)
    fig4.circle('Date', 'new_deaths', source=plotdata, color=c,
                legend_label=code)
    #fig4.line('Date', 'new_deaths', source=plotdata, color=c,
    #          legend_label=code)
    c_mean = data[data.location == code].new_deaths.rolling(5).mean().fillna(0)
    fig4.line(x=data[data.location == code].Date, y=c_mean, color=c, legend_label=code)
print('figure 4')

fig5 = bkp.figure(plot_width=1200, plot_height=600,
                  title='New Deaths vs. Total Deaths',
                  x_axis_label='Total Deaths',
                  y_axis_label='New Deaths',
                  x_axis_type='log', y_axis_type='log',
                  tooltips=tooltips)

colors = (c for c in Category10[10])
for code in codes_to_plot:
    plotdata = ColumnDataSource(data[data.location == code])
    c = next(colors)
    fig5.circle('total_deaths', 'new_deaths', source=plotdata, color=c,
                legend_label=code)
    #fig5.line('total_deaths', 'new_deaths', source=plotdata, color=c,
    #          legend_label=code)
    c_mean = data[data.location == code].new_deaths.rolling(5).mean().fillna(0)
    fig5.line(x=data[data.location == code].total_deaths, y=c_mean, color=c, legend_label=code)
print('figure 5')

fig0.legend.location = "top_left"
fig0.legend.click_policy="hide"
fig1.legend.location = "top_left"
fig1.legend.click_policy="hide"
fig2.legend.location = "top_left"
fig2.legend.click_policy="hide"
fig3.legend.location = "top_left"
fig3.legend.click_policy="hide"
fig4.legend.location = "top_left"
fig4.legend.click_policy="hide"
fig5.legend.location = "top_left"
fig5.legend.click_policy="hide"

bkp.output_file('covid19.html')
bkp.show(Column(fig0, fig1, fig2, fig3, fig4, fig5))
