from builtins import int
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.patches import ConnectionPatch
import matplotlib.dates as mdates
from bin.config import PROTOCOLS_CHART_NAME, L4_PROTOCOLS_CHART_NAME, CHARTS_FOLDER, PROTOCOLS_CHART_TITLE, \
    L4_PROTOCOLS_CHART_TITLE, DEST_PORTS_CHART_TITLE, DEST_PORTS_X_LABEL, DEST_PORTS_CHART_NAME, PORT_NAME, COLORS, \
    SUMMARY_CHART_X_LABEL, SUMMARY_CHART_TITLE, LABEL_TITLE_FONT_SIZE, SUMMARY_CHART_NAME


def bytes_per_L4_protocol_chart(data):
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


def destination_ports_chart(ports):
    plt.rcdefaults()
    fig, ax = plt.subplots()
    services = []
    conn = []
    for key, value in ports.items():
        services.append(PORT_NAME.get(key, 'Unassigned'))
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
    locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
    formatter = mdates.ConciseDateFormatter(locator)
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    x_axis = data.index
    if option == 'flows':
        y_axis = data['ts'].apply(lambda x: int(x))
        ax.plot(x_axis, y_axis)
        ax.set_title('flows' + ' ' + SUMMARY_CHART_TITLE, fontsize=LABEL_TITLE_FONT_SIZE)
    elif option == 'bytes':
        y_axis = data['te'].apply(lambda x: int(x))
        ax.plot(x_axis, y_axis)
        ax.set_title('bytes' + ' ' + SUMMARY_CHART_TITLE, fontsize=LABEL_TITLE_FONT_SIZE)
    elif option == 'packets':
        y_axis = data['td'].apply(lambda x: int(x))
        ax.plot(x_axis, y_axis)
        ax.set_title('packets' + ' ' + SUMMARY_CHART_TITLE, fontsize=LABEL_TITLE_FONT_SIZE)
    elif option == 'avg_bps':
        y_axis = data['sa'].apply(lambda x: int(x))
        ax.plot(x_axis, y_axis)
        ax.set_title('Average bytes per seconds' + ' ' + SUMMARY_CHART_TITLE, fontsize=LABEL_TITLE_FONT_SIZE)
    elif option == 'avg_pps':
        y_axis = data['da'].apply(lambda x: int(x))
        ax.plot(x_axis, y_axis)
        ax.set_title('Average packets per seconds' + ' ' + SUMMARY_CHART_TITLE, fontsize=LABEL_TITLE_FONT_SIZE)
    elif option == 'avg_bpp':
        y_axis = data['sp'].apply(lambda x: int(x))
        ax.plot(x_axis, y_axis)
        ax.set_title('Average bytes per packet' + ' ' + SUMMARY_CHART_TITLE, fontsize=LABEL_TITLE_FONT_SIZE)
    ax.set_xlabel(SUMMARY_CHART_X_LABEL, fontsize=LABEL_TITLE_FONT_SIZE)
    ax.set_ylabel(option, fontsize=LABEL_TITLE_FONT_SIZE)
    ax.grid(True, linestyle='-.')
    ax.tick_params(labelcolor='black', labelsize='medium', width=3)
    plt.xticks(rotation=90)
    fig.savefig(os.path.join(CHARTS_FOLDER + SUMMARY_CHART_NAME + option), bbox_inches='tight', facecolor='#f2ede6',
                edgecolor='b')
