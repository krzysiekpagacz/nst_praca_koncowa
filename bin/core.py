"""
In our research, flow is defined as a unidirectional se-
quence of packets that share the same five-tuple: IP source
address, IP destination address, source port, destination
port, and transport layer protocol type

elephant and mice flows

extract models of flow length and size

flow length (in packets) and flow size (in bytes)


"""

import pandas as pd
import numpy as np
import matplotlib
import os
import sys

from bin.charts import bytes_per_protocol_chart

INPUT_FILES: str = 'netflow_csv'

def get_data():
	li = []
	with os.scandir('../../'+INPUT_FILES) as entries:
		for entry in entries:
			try:
				df = pd.read_csv('../../'+INPUT_FILES+'/' + entry.name, index_col=0, sep=',', low_memory=False)
				print(f'File name: {entry.name}, Rows: {df.shape[0]}')
				li.append(df)
			except FileNotFoundError:
				print('check path to file or file name')
				sys.exit()
	out = pd.concat(li, axis=0, ignore_index=True)
	return out

def bytes_per_protocol(df):
	if isinstance(df, pd.DataFrame):
		protocols = df.groupby(['pr'], as_index=False)['ibyt'].sum()
		print(protocols)
	else:
		print('something went wrong with import data, passed object is not a dataframe')
		sys.exit()
	return protocols.to_dict()


if __name__ == '__main__':
    df = get_data()
    bpp = bytes_per_protocol(df)
    # bytes_per_protocol_chart(bpp)

