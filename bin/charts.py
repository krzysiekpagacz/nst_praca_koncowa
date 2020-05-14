import matplotlib.pyplot as plt
import numpy as np
import os

from matplotlib.patches import ConnectionPatch

from bin.config import PROTOCOLS_CHART_NAME, L4_PROTOCOLS_CHART_NAME, CHARTS_FOLDER


def bytes_per_L4_protocol_chart(input_data):
    print(f'input data type is: {type(input_data)}')
    try:
        protocols = input_data['pr'].to_numpy()
    except KeyError:
        print('missing column pr')
    try:
        bytes = input_data['ibyt'].to_numpy()
    except KeyError:
        print('missing column ibyt')
    fig, axs = plt.subplots()
    axs.bar(protocols, bytes)
    axs.legend()
    fig.savefig(os.path.join(CHARTS_FOLDER+L4_PROTOCOLS_CHART_NAME), bbox_inches='tight')

def bar_of_pie_protocols_chart(input_data):
    protocol_ratio_others = {}
    bytes_sum_total = 0
    bytes_sum_others = 0
    ratio_tcp = 0
    ratio_udp = 0
    ratio_others = 0
    legend_others = []
    #sum number of bytes
    for key, value in input_data.items():
        bytes_sum_total += value
        if key not in ['TCP', 'UDP']:
            bytes_sum_others += value
    #calculate ratios
    for key, value in input_data.items():
        if key == 'TCP':
            ratio_tcp = round((value/bytes_sum_others)*100, 2)
        if key == 'UDP':
            ratio_udp = round((value/bytes_sum_others) * 100, 2)
        if key not in ['TCP', 'UDP']:
            protocol_ratio_others[key] = round((value/bytes_sum_others)*100, 2)
    ratio_others = round((bytes_sum_others/bytes_sum_total)*100, 2)
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
    ax1.set_title('Distribution of bytes among protocols.')
    # bar chart parameters
    xpos = 0
    bottom = 0
    ratios = []
    width = .2
    colors = ['#1531d1', '#fa1616', '#3cd113', '#f6fa16', '#b515d1', '#15a2d1', '#2b15d1', '#d1158c','#15d183' ]
    print(protocol_ratio_others)
    for key, value in protocol_ratio_others.items():
        if value>1:
            ratios.append(value)
            legend_others.append(key)

    for j in range(len(ratios)):
        height = ratios[j]
        ax2.bar(xpos, height, width, bottom=bottom, color=colors[j])
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
    fig.savefig(os.path.join(CHARTS_FOLDER+PROTOCOLS_CHART_NAME), bbox_inches='tight')




