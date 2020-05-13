import matplotlib
import matplotlib.pyplot as plt
import numpy as np

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
    print(f'protocols: {protocols}')
    print(f'bytes: {bytes}')

    fig, axs = plt.subplots()
    axs.bar(protocols, bytes)
    # fig.subtitle('Bytes per Protocols of Transport Layer')
    axs.legend()
    fig.savefig('Distribution of Bytes per Transport Layer Protocols', bbox_inches='tight')






