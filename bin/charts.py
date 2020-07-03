from builtins import int

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from datetime import datetime

from matplotlib.patches import ConnectionPatch

from bin.config import PROTOCOLS_CHART_NAME, L4_PROTOCOLS_CHART_NAME, CHARTS_FOLDER, PROTOCOLS_CHART_TITLE, \
    L4_PROTOCOLS_CHART_TITLE, DEST_PORTS_CHART_TITLE, DEST_PORTS_X_LABEL, DEST_PORTS_CHART_NAME, PORT_NAME, COLORS, \
    SUMMARY_CHART_X_LABEL, SUMMARY_CHART_TITLE, LABEL_TITLE_FONT_SIZE, SUMMARY_CHART_NAME


def bytes_per_L4_protocol_chart(data):
    print(f'input data type is: {type(data)}')
    data = data.iloc[:, 9:11]
    protocols = []
    bytes = []
    for key, value in data.items():
        protocols.append(key)
        bytes.append(data.iloc[0][key])
    fig, axs = plt.subplots()
    axs.bar(protocols, bytes, color=COLORS)
    axs.set_title(L4_PROTOCOLS_CHART_TITLE)
    fig.savefig(os.path.join(CHARTS_FOLDER + L4_PROTOCOLS_CHART_NAME), bbox_inches='tight')


def bar_of_pie_protocols_chart(input_data):
    # print(type(input_data))
    # print(input_data)
    protocol_ratio_others = {}
    bytes_sum_total = 0
    bytes_sum_others = 0
    ratio_tcp = 0
    ratio_udp = 0
    legend_others = []
    # sum number of bytes
    # bytes_sum_total = input_data.sum()
    # # print(bytes_sum_total)
    # bytes_sum_others = input_data.iloc[:, 0:9].sum()
    # bytes_sum_others = bytes_sum_others.sum()

    for key, value in input_data.iteritems():
        # print(key)
        # print(value)
        bytes_sum_total = input_data.iloc[0][key]
        if key not in ['TCP', 'UDP']:
            bytes_sum_others = input_data.iloc[0][key]

    print(bytes_sum_total)
    print(bytes_sum_others)
    # for key, value in input_data.items():
    #     bytes_sum_total += value
    #     if key not in ['TCP', 'UDP']:
    #         bytes_sum_others += value
    #     print(bytes_sum_others)
    # calculate ratios
    for key, value in input_data.items():
        if key == 'TCP':
            ratio_tcp = round((value / bytes_sum_others) * 100, 2)
        if key == 'UDP':
            ratio_udp = round((value / bytes_sum_others) * 100, 2)
        if key not in ['TCP', 'UDP']:
            protocol_ratio_others[key] = round((value / bytes_sum_others) * 100, 2)
    ratio_others = round((bytes_sum_others / bytes_sum_total) * 100, 2)
    # make figure and assign axis objects
    fig = plt.figure(figsize=(9, 5))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    fig.subplots_adjust(wspace=0)
    # pie chart parameters
    ratios = [ratio_others, ratio_tcp, ratio_udp]
    labels = ['Other', 'TCP', 'UDP']
    explode = [0.2, 0, 0]
    # rotate so that first wedge is split by the x-axis
    angle = -180 * ratios[0]
    ax1.pie(ratios, autopct='%1.2f%%', startangle=angle,
            labels=labels, explode=explode)
    ax1.set_title(PROTOCOLS_CHART_TITLE)
    # bar chart parameters
    xpos = 0
    bottom = 0
    ratios = []
    width = .2
    print(protocol_ratio_others)
    for key, value in protocol_ratio_others.items():
        if value > 1:
            ratios.append(value)
            legend_others.append(key)

    for j in range(len(ratios)):
        height = ratios[j]
        ax2.bar(xpos, height, width, bottom=bottom, color=COLORS[j])
        ypos = bottom + ax2.patches[j].get_height() / 2
        bottom += height
        ax2.text(xpos, ypos, "%d%%" % (ax2.patches[j].get_height()),
                 ha='center')
    ax2.set_title('Other Protocols')
    ax2.legend(legend_others)
    ax2.axis('off')
    ax2.set_xlim(- 2.5 * width, 2.5 * width)
    # use ConnectionPatch to draw lines between the two plots
    # get the wedge data
    theta1, theta2 = ax1.patches[0].theta1, ax1.patches[0].theta2
    center, r = ax1.patches[0].center, ax1.patches[0].r
    bar_height = sum([item.get_height() for item in ax2.patches])
    # draw top connecting line
    x = r * np.cos(np.pi / 180 * theta2) + center[0]
    y = np.sin(np.pi / 180 * theta2) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData,
                          xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0, 0, 0])
    con.set_linewidth(4)
    ax2.add_artist(con)
    # draw bottom connecting line
    x = r * np.cos(np.pi / 180 * theta1) + center[0]
    y = np.sin(np.pi / 180 * theta1) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData,
                          xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0, 0, 0])
    ax2.add_artist(con)
    con.set_linewidth(4)
    plt.figtext(0.99, 0.01,
                'Note! Protocols with share less than 1% among the other protocols (not TCP or UDP) have been skipped',
                horizontalalignment='right')
    fig.savefig(os.path.join(CHARTS_FOLDER + PROTOCOLS_CHART_NAME), bbox_inches='tight')


def dest_ports_chart(ports):
    plt.rcdefaults()
    fig, ax = plt.subplots()
    services = []
    conn = []
    for key, value in ports.items():
        services.append(PORT_NAME.get(key, -1.0))
        conn.append(ports.iloc[0][key])
    y_pos = np.arange(len(services))
    x_axis = conn
    ax.barh(y_pos, x_axis, align='center', color=COLORS)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(services)
    ax.invert_yaxis()
    ax.set_xlabel(DEST_PORTS_X_LABEL)
    ax.set_title(DEST_PORTS_CHART_TITLE)
    fig.savefig(os.path.join(CHARTS_FOLDER + DEST_PORTS_CHART_NAME), bbox_inches='tight')


def get_summary_chart(data, option='flows'):
    """
    This functions generates charts depends on the option attribute.
    :param data: dataframe object; must contain date column
    :param option: Possible values are:
     - flows - default value
     - bytes
     - packets
     - avg_bps
     - avg_pps
     - avg_bpp
    :return: saved chart into png file
    """
    if isinstance(data, pd.DataFrame):
        try:
            day = data['date'][0]
            day = str(day.day) + '-' + str(day.month) + '-' + str(day.year)
            data.reset_index()
            data = data.set_index(['date'])
            data.sort_values('date', inplace=True, ascending=True)
        except KeyError:
            print('missing column date in input data frame')
    y_axis = data[option].apply(lambda x: int(x))
    fig, ax = plt.subplots()
    print(f'index value: {data.index}')
    ax.plot(data.index, y_axis)
    ax.set_xlabel(SUMMARY_CHART_X_LABEL, fontsize=LABEL_TITLE_FONT_SIZE)
    ax.set_ylabel(option, fontsize=LABEL_TITLE_FONT_SIZE)
    if option == 'avg_bps':
        ax.set_title('average bites per seconds' + ' ' + SUMMARY_CHART_TITLE + day, fontsize=LABEL_TITLE_FONT_SIZE)
    elif option == 'avg_pps':
        ax.set_title('average packets per seconds' + ' ' + SUMMARY_CHART_TITLE + day, fontsize=LABEL_TITLE_FONT_SIZE)
    elif option == 'avg_bpp':
        ax.set_title('average bytes per packet' + ' ' + SUMMARY_CHART_TITLE + day, fontsize=LABEL_TITLE_FONT_SIZE)
    elif not option.startswith('avg'):
        ax.set_title('number of ' + option + ' ' + SUMMARY_CHART_TITLE + day, fontsize=LABEL_TITLE_FONT_SIZE)
    else:
        ax.set_title(option + ' ' + SUMMARY_CHART_TITLE + day, fontsize=LABEL_TITLE_FONT_SIZE)
    ax.grid(True, linestyle='-.')
    ax.tick_params(labelcolor='black', labelsize='medium', width=3)
    plt.xticks(rotation=90)
    fig.savefig(os.path.join(CHARTS_FOLDER + SUMMARY_CHART_NAME + option), bbox_inches='tight', facecolor='#f2ede6',
                edgecolor='b')


def get_summary_chart2(data, option='flows'):
    print(data.columns.values)
    fig, ax = plt.subplots()
    y_axis = data.index
    if option == 'flows':
        data = data['ts'].apply(lambda x: int(x))
        ax.plot(y_axis, data)
        ax.set_title('flows' + ' ' + SUMMARY_CHART_TITLE, fontsize=LABEL_TITLE_FONT_SIZE)
    elif option == 'bytes':
        data = data['te'].apply(lambda x: int(x))
        ax.plot(y_axis, data)
        ax.set_title('bytes' + ' ' + SUMMARY_CHART_TITLE, fontsize=LABEL_TITLE_FONT_SIZE)
    elif option == 'packets':
        data = data['td'].apply(lambda x: int(x))
        ax.plot(y_axis, data)
        ax.set_title('packets' + ' ' + SUMMARY_CHART_TITLE, fontsize=LABEL_TITLE_FONT_SIZE)
    elif option == 'avg_bps':
        data = data['sa'].apply(lambda x: int(x))
        ax.plot(y_axis, data)
        ax.set_title('average bites per seconds' + ' ' + SUMMARY_CHART_TITLE , fontsize=LABEL_TITLE_FONT_SIZE)
    elif option == 'avg_pps':
        data = data['da'].apply(lambda x: int(x))
        ax.plot(y_axis, data)
        ax.set_title('average packets per seconds' + ' ' + SUMMARY_CHART_TITLE , fontsize=LABEL_TITLE_FONT_SIZE)
    elif option == 'avg_bpp':
        data = data['sp'].apply(lambda x: int(x))
        ax.plot(y_axis, data)
        ax.set_title('average bytes per packet' + ' ' + SUMMARY_CHART_TITLE , fontsize=LABEL_TITLE_FONT_SIZE)
    ax.set_xlabel(SUMMARY_CHART_X_LABEL, fontsize=LABEL_TITLE_FONT_SIZE)
    ax.set_ylabel(option, fontsize=LABEL_TITLE_FONT_SIZE)
    ax.grid(True, linestyle='-.')
    ax.tick_params(labelcolor='black', labelsize='medium', width=3)
    plt.xticks(rotation=90)
    fig.savefig(os.path.join(CHARTS_FOLDER + SUMMARY_CHART_NAME + option), bbox_inches='tight', facecolor='#f2ede6',
                edgecolor='b')
