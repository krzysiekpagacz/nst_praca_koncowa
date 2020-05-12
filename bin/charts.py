import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def bytes_per_protocol_chart(input_data):
    global fig, ax, rects1, rects2
    labels = ['G1', 'G2', 'G3', 'G4', 'G5']
    protocols, bytes = zip(*input_data)
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, protocols, width, label='protocols')
    rects2 = ax.bar(x + width / 2, bytes, width, label='bytes')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()

    plt.show()




