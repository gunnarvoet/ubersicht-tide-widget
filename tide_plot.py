#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import pandas as pd
from datetime import date, timedelta, datetime
import urllib2

# set color for the plot
cc = 'w'

# Define location
# this needs to be changed depending on the desired location
# go to
# http://tidesandcurrents.noaa.gov/
# or
# http://tidesandcurrents.noaa.gov/map
# to find the location id
api_location = '9410230'; # La Jolla

# Set times
t1 = date.today() - timedelta(1)
api_begin_date = t1.strftime('%Y%m%d')
t2 = date.today() + timedelta(1)
api_end_date = t2.strftime('%Y%m%d')

# Plot settings
font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 11,
        'sans-serif' : 'Helvetica Neue',
        'weight': 'light'}

plt.rc('font', **font)
xtick = {'color' : cc}
plt.rc('xtick', **xtick)
ytick = {'color' : cc}
plt.rc('ytick', **ytick)
axes = {'labelcolor' : cc}
plt.rc('axes', **axes)

# Prepare plot
fig = plt.figure(figsize=(10,1.8))

# Get tide data from NOOA
api_address = "http://tidesandcurrents.noaa.gov/api/datagetter?begin_date="+\
               api_begin_date+"&end_date="+api_end_date+"&station="+api_location+\
               "&product=predictions&datum=msl&units=english&time_zone=lst&application=web_services&format=csv"

try:
    response = urllib2.urlopen(api_address)
    test = response.read()
    from StringIO import StringIO
    test2 = StringIO(test)
    df = pd.read_csv(test2)
    # Set time strings as index for the data frame
    df = df.set_index(pd.DatetimeIndex(df['Date Time']))
    # Rename column
    df.rename(columns={' Prediction' : 'tide'}, inplace = True)
    # Remove time column
    del df['Date Time']

    # Add a subplot
    ax = fig.add_subplot(111)

    # Set title
    ttl = 'Tide @ La Jolla, CA'
    fig.suptitle(ttl, fontsize=12, fontweight='normal', color=cc, family='sans-serif')

    idx = df.index.date
    plt.plot_date(df.index, df['tide'],marker=None, linestyle='-',color=cc,linewidth=2)

    # Plot current time
    t = datetime.now()
    s = df['tide']
    d = s.asof(t)
    plt.plot(t,d,marker='o',color='r',linewidth='0',markersize=8,alpha=0.5)

    # time label settings
    ax.xaxis.set_minor_locator(dates.DayLocator(interval=1))
    ax.xaxis.set_minor_formatter(dates.DateFormatter('\n%d-%a'))
    ax.xaxis.set_major_locator(dates.HourLocator(interval=12))
    ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))

    # Remove grid lines (dotted lines inside plot)
    ax.grid(False)

    ax.set_ylabel('ft')
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_position(('outward', 10))
    ax.spines['left'].set_smart_bounds(True)
    ax.spines['bottom'].set_position(('outward', 10))
    ax.spines['bottom'].set_smart_bounds(True)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['top'].set_color(None)

    ax.tick_params(axis='x', colors=cc)
    ax.tick_params(axis='y', colors=cc)

    ax.xaxis.label.set_color(cc)
    ax.yaxis.label.set_color(cc)

    # Remove plot frame
    ax.set_frame_on(False)

    # Save figure
    plt.savefig('tide.widget/tide.png', bbox_inches='tight',transparent=True,dpi=fig.dpi)

# Avoid a bunch of error messages when no internet connection:
except urllib2.URLError as e:
    ttl = 'no internet connection'
    fig.suptitle(ttl, fontsize=12, fontweight='normal', color=cc, family='sans-serif')
    plt.savefig('tide.widget/tide.png', bbox_inches='tight',transparent=True,dpi=fig.dpi)