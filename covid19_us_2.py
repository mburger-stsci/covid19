import numpy as np
import pandas as pd
from datetime import date
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px


# import bokeh.plotting as bkp
# from bokeh.models import (HoverTool, ColumnDataSource, ColorBar,
#                           LogColorMapper, LogTicker)
# from bokeh.palettes import Magma256, Category10
# from bokeh.io import curdoc
# from bokeh.themes import Theme
# from bokeh.layouts import Column

# curdoc().theme = Theme('/Users/mburger/.bokeh/bokeh.yml')

def makedate(datestr):
    result = [int(x) for x in datestr.split('/')]
    return date(result[2]+2000, result[0], result[1])

today = date.today().isoformat()
savefile = f'data/covid19_us_{today}.pkl'
if os.path.exists(savefile):
    cases_state = pd.read_pickle(savefile)
else:
    cases = pd.read_csv('https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv')
    deaths = pd.read_csv('https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_deaths_usafacts.csv')
    population = pd.read_csv('https://usafactsstatic.blob.core.windows.net/public/data/covid-19'
                             '/covid_county_population_usafacts.csv')

    states = cases.State.unique()
    dates_ = [x for x in cases.columns if '/' in x]
    dates = [makedate(x) for x in cases.columns if '/' in x]
    columns = ['Date', 'State', 'new_cases', 'cases_rolling', 'total_cases',
               'new_deaths', 'deaths_rolling', 'total_deaths']
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
                                              'new_cases': int(c_new),
                                              'total_cases': int(c_cum),
                                              'new_deaths': int(d_new),
                                              'total_deaths': int(d_cum)},
                                             ignore_index=True)
            
        c_rolling = cases_state[cases_state.State == state].new_cases.rolling(
                5).mean().fillna(0)
        d_rolling = cases_state[cases_state.State == state].new_deaths.rolling(
                5).mean().fillna(0)
        cases_state.loc[:, 'cases_rolling'][cases_state.State == state] = c_rolling
        cases_state.loc[:, 'deaths_rolling'][cases_state.State == state] = d_rolling

    cases_state['DateIso'] = cases_state.Date.apply(lambda x: x.isoformat())
    cases_state.new_cases.replace(0, 0.1, inplace=True)
    cases_state.new_deaths.replace(0, 0.1, inplace=True)

    cases_state.set_index('State', inplace=True)
    cases_state.to_pickle(savefile)
    
states_to_plot = ['MD', 'NY', 'FL', 'TX', 'AL', 'AZ', 'CA']

app = dash.Dash('Covid-19 In USA')

layout = {'title': 'Total Cases By State',
          'xaxis_title': 'Date',
          'yaxis_title': '# Cases',
          'yaxis_type': 'log'}

ctotal = px.line(cases_state.loc[states_to_plot],
                 x='Date',
                 y='total_cases',
                 color=cases_state.loc[states_to_plot].index)
ctotal.update_layout(layout)

cnew = px.scatter(cases_state.loc[states_to_plot],
                  x='Date',
                  y='new_cases',
                  color=cases_state.loc[states_to_plot].index)
# cnew.add_trace(cases_state,
#                type='line',
#                x='Date',
#                y='cases_rolling',
#                color=cases_state.loc[states_to_plot].index)
layout['title'] = 'New Cases By State'
cnew.update_layout(layout)

dtotal = px.line(cases_state.loc[states_to_plot],
                 x='Date',
                 y='total_deaths',
                 color=cases_state.loc[states_to_plot].index)
layout['title'] = 'Total Deaths By State'
layout['yaxis_title'] = '# Deaths'
dtotal.update_layout(layout)

dnew = px.line(cases_state.loc[states_to_plot],
               x='Date',
               y='new_deaths',
               color=cases_state.loc[states_to_plot].index)
layout['title'] = 'New Deaths By State'
dnew.update_layout(layout)

app.layout = html.Div(children=[
    html.H1('Covid-19 in USA'),
    dcc.Graph(id='TotalCases',
              figure=ctotal),
    dcc.Graph(id='NewCases',
              figure=cnew),
    dcc.Graph(id='TotalDeaths',
              figure=dtotal),
    dcc.Graph(id='NewDeaths',
              figure=dnew)
    ])

app.run_server(debug=False)

'''

plotdata = ColumnDataSource(cases_state)

states_to_plot = ['MD', 'NY', 'FL', 'TX', 'WI', 'GA']
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
    # fig1.line('Date', 'new_cases', source=plotdata, color=c,
    #             legend_label=state)
    c_mean = cases_state[cases_state.State == state].new_cases.rolling(5).mean().fillna(0)
    fig1.line(x=cases_state[cases_state.State == state].Date,
              y=c_mean, color=c, legend_label=state)

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
    # fig2.line('total_cases', 'new_cases', source=plotdata, color=c,
    #             legend_label=state)
    c_mean = cases_state[cases_state.State == state].new_cases.rolling(5).mean().fillna(0)
    fig2.line(x=cases_state[cases_state.State == state].total_cases,
              y=c_mean, color=c, legend_label=state)

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
#    fig4.line('Date', 'new_deaths', source=plotdata, color=c,
#              legend_label=state)
    d_mean = cases_state[cases_state.State == state].new_deaths.rolling(5).mean().fillna(0)
    fig4.line(x=cases_state[cases_state.State == state].Date,
              y=d_mean, color=c, legend_label=state)

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
    # fig5.line('total_deaths', 'new_deaths', source=plotdata, color=c,
    #           legend_label=state)
    d_mean = cases_state[cases_state.State == state].new_deaths.rolling(5).mean().fillna(0)
    fig5.line(x=cases_state[cases_state.State == state].total_deaths,
              y=d_mean, color=c, legend_label=state)


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
'''
