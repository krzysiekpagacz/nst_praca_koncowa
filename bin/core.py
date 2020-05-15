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

from bin.config import INPUT_FILES, PORT_NAME
from bin.pdf_generator import generate_pdf_file
from bin.charts import bar_of_pie_protocols_chart, dest_ports_chart
from bin.charts import bytes_per_L4_protocol_chart


def get_data():
	li = []
	input_files = []
	with os.scandir('../../' + INPUT_FILES) as entries:
		for entry in entries:
			try:
				df = pd.read_csv('../../' + INPUT_FILES + '/' + entry.name, index_col=0, sep=',', low_memory=False)
				print(f'File name: {entry.name}, Rows: {df.shape[0]}')
				li.append(df)
				input_files.append(entry.name)
			except FileNotFoundError:
				print('check path to file or file name')
				sys.exit()
	out = pd.concat(li, axis=0, ignore_index=True)
	return out, input_files


def bytes_per_l4_protocol(df):
	if isinstance(df, pd.DataFrame):
		df = df[df.pr.isin(['TCP', 'UDP'])]
		protocols = df.groupby(['pr'], as_index=False)['ibyt'].sum()
		print(protocols)
		print(type(protocols))
	else:
		print('something went wrong with import data, passed object is not a dataframe')
		sys.exit()
	return protocols


def bytes_per_protocols(df):
	if isinstance(df, pd.DataFrame):
		new_df = df.groupby(['pr'], as_index=False)['ibyt'].sum()
	else:
		print('something went wrong with import data, passed object is not a dataframe')
		sys.exit()
	temp_list = new_df.to_dict(orient='records')
	protocols = {}
	for item_dict in temp_list:
		new_key = list(item_dict.values())[0]
		new_value = list(item_dict.values())[1]
		protocols[new_key] = new_value
	return protocols


def dest_ports(df, get_results=10):
	"""
	:param df: input data
	:param get_results: number of analyzed ports (in descending order in terms of connections number)
	:return: dictionary with port number and number of connections
	"""
	ports = {}
	try:
		df = df[~df.dp.isin(['0','21548'])]
		df = df.loc[df.dp<49152]
		new_df = df.groupby(['dp'], as_index=False)['sa'].count().sort_values(by='sa', ascending=False)[:get_results]
		# print(new_df.head(20))
		print(type(new_df))
	except KeyError:
		print(f'missing column dp in input dataframe')
	temp_list = new_df.to_dict(orient='records')
	for item in temp_list:
		new_key = list(item.values())[0]
		new_value = list(item.values())[1]
		ports[new_key] = new_value
	print(ports)
	return ports


# def avg_duration(df):
# 	try:
# 		arr = df['td'].values
# 		print(type(arr))
# 		avg_td = np.average(arr)
# 		print(f'avg_td: {avg_td}')
# 	except KeyError:
# 		print(f'missing column td in input dataframe')


if __name__ == '__main__':
	input_data = get_data()
	df = input_data[0]
	dest_ports_chart(dest_ports(df))
	bpp = bytes_per_l4_protocol(df)
	bytes_per_L4_protocol_chart(bpp)
	bpp_all = bytes_per_protocols(df)
	bar_of_pie_protocols_chart(bpp_all)
	generate_pdf_file(input_data[1])
