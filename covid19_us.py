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
    result = [int(x) for x in datestr.split('/')]
    return date(result[2]+2000, result[0], result[1])


cases = pd.read_csv('https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv')
deaths = pd.read_csv('https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_deaths_usafacts.csv')
population = pd.read_csv('https://usafactsstatic.blob.core.windows.net/public/data/covid-19'
                         '/covid_county_population_usafacts.csv')

states = cases.State.unique()
dates_ = [x for x in cases.columns if '/' in x]
dates = [makedate(x) for x in cases.columns if '/' in x]
columns = ['Date', 'State', 'new_cases', 'total_cases', 'new_deaths',
           'total_deaths']
cases_state = pd.DataFrame(columns=columns)

for state in states:
    c_last = 0
    d_last = 0
    for day_, day in zip(dates_, dates):
        c_cum = cases[(cases.State == state)][day_].sum()
        c_new, c_last = c_cum - c_last, c_cum
        d_cum = deaths[(deaths.State == state)][day_].sum()
        d_new, d_last = d_cum - d_last, d_cum
        cases_state = cases_state.append({'Date': day, 'State': state,
                                          'new_cases': c_new,
                                          'total_cases': c_cum,
                                          'new_deaths': d_new,
                                          'total_deaths': d_cum},
                                         ignore_index=True)

cases_state['DateIso'] = cases_state.Date.apply(lambda x: x.isoformat())

states_to_plot = ['MD', 'NY', 'FL', 'WA', 'TX', 'LA', 'CA']
tooltips = [('State', '@State'),
            ('Date', '@DateIso'),
            ('New Cases', '@new_cases'),
            ('Total Cases', '@total_cases')]

fig0 = bkp.figure(plot_width=1200, plot_height=600,
                  title='Total Cases',
                  x_axis_label='Date',
                  y_axis_label='# Cases',
                  x_axis_type='datetime', y_axis_type='log',
                  tooltips=tooltips)

colors = (c for c in Category10[10])
for state in states_to_plot:
    plotdata = ColumnDataSource(cases_state[cases_state.State == state])
    c = next(colors)
    fig0.circle('Date', 'total_cases', source=plotdata, color=c,
               legend_label=state)
    fig0.line('Date', 'total_cases', source=plotdata, color=c,
              legend_label=state)

fig1 = bkp.figure(plot_width=1200, plot_height=600,
                  title='New Cases',
                  x_axis_label='Date',
                  y_axis_label='# Cases',
                  x_axis_type='datetime', y_axis_type='log',
                  # x_range=fig0.x_range, y_range=fig0.y_range,
                  tooltips=tooltips)

colors = (c for c in Category10[10])
for state in states_to_plot:
    plotdata = ColumnDataSource(cases_state[cases_state.State == state])
    c = next(colors)
    fig1.circle('Date', 'new_cases', source=plotdata, color=c,
                legend_label=state)
    fig1.line('Date', 'new_cases', source=plotdata, color=c,
                legend_label=state)

fig2 = bkp.figure(plot_width=1200, plot_height=600,
                  title='New Cases vs. Total Cases',
                  x_axis_label='Total Cases',
                  y_axis_label='New Cases',
                  x_axis_type='log', y_axis_type='log',
                  # x_range=fig0.x_range, y_range=fig0.y_range,
                  tooltips=tooltips)

colors = (c for c in Category10[10])
for state in states_to_plot:
    plotdata = ColumnDataSource(cases_state[cases_state.State== state])
    c = next(colors)
    fig2.circle('total_cases', 'new_cases', source=plotdata, color=c,
                legend_label=state)
    fig2.line('total_cases', 'new_cases', source=plotdata, color=c,
                legend_label=state)

tooltips = [('Country', '@State'),
            ('Date', '@DateIso'),
            ('New Deaths', '@new_deaths'),
            ('Total Deaths', '@total_deaths')]

fig3 = bkp.figure(plot_width=1200, plot_height=600,
                  title='Total Deaths',
                  x_axis_label='Date',
                  y_axis_label='# Deaths',
                  x_axis_type='datetime', y_axis_type='log',
                  # x_range=fig0.x_range, y_range=fig0.y_range,
                  tooltips=tooltips)

colors = (c for c in Category10[10])
for state in states_to_plot:
    plotdata = ColumnDataSource(cases_state[cases_state.State == state])
    c = next(colors)
    fig3.circle('Date', 'total_deaths', source=plotdata, color=c,
                legend_label=state)
    fig3.line('Date', 'total_deaths', source=plotdata, color=c,
              legend_label=state)

fig4 = bkp.figure(plot_width=1200, plot_height=600,
                  title='New Deaths',
                  x_axis_label='Date',
                  y_axis_label='# Deaths',
                  x_axis_type='datetime', y_axis_type='log',
                  # x_range=fig0.x_range, y_range=fig0.y_range,
                  tooltips=tooltips)

colors = (c for c in Category10[10])
for state in states_to_plot:
    plotdata = ColumnDataSource(cases_state[cases_state.State == state])
    c = next(colors)
    fig4.circle('Date', 'new_deaths', source=plotdata, color=c,
                legend_label=state)
    fig4.line('Date', 'new_deaths', source=plotdata, color=c,
              legend_label=state)

fig5 = bkp.figure(plot_width=1200, plot_height=600,
                  title='New Deaths vs. Total Deaths',
                  x_axis_label='Total Deaths',
                  y_axis_label='New Deaths',
                  x_axis_type='log', y_axis_type='log',
                  # x_range=fig0.x_range, y_range=fig0.y_range,
                  tooltips=tooltips)

colors = (c for c in Category10[10])
for state in states_to_plot:
    plotdata = ColumnDataSource(cases_state[cases_state.State == state])
    c = next(colors)
    fig5.circle('total_deaths', 'new_deaths', source=plotdata, color=c,
                legend_label=state)
    fig5.line('total_deaths', 'new_deaths', source=plotdata, color=c,
              legend_label=state)


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

bkp.output_file('covid19_us.html')
bkp.show(Column(fig0, fig1, fig2, fig3, fig4, fig5))

# from IPython import embed
# embed() # drop into an IPython session.
