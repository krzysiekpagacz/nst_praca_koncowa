import requests
import re
import os
from bs4 import BeautifulSoup

MAIN_URL = 'http://pbz.kt.agh.edu.pl/~matiolanski/netflow/'
THIS_DIRECTORY = os.path.dirname(__file__)

def get_folders_with_netflows():
	response = requests.get(MAIN_URL)
	soup = BeautifulSoup(response.text, 'html.parser')
	folders = []
	for link in soup.find_all('a', {'href': re.compile('\d{4}-\d{2}-\d{2}/')}):
		url = MAIN_URL + link.text
		folders.append(url)
	return folders


def get_all_files_from_folder(folder):
	files = []
	response = requests.get(folder)
	soup = BeautifulSoup(response.text, 'html.parser')
	for link in soup.find_all('a', {'href': re.compile('nfcapd')}):
		url = folder + link.text
		files.append(url)
	return files


def main():
	file_counter = 0
	folders = get_folders_with_netflows()
	print('Found {} folders'.format(len(folders)))
	for folder in folders:
		print('current folder is {}'.format(folder))
		files = get_all_files_from_folder(folder)
		for file_url in files:
			file_counter += 1
			file_name = str(file_url).split('/')[-1]
			print('current FILE is {}'.format(file_name))
			file_response = requests.get(file_url)
			open(os.path.join(THIS_DIRECTORY, '../resources/netflow_raw/'+file_name), 'wb').write(file_response.content)
	print('DONE. Downloaded files: {}'.format(file_counter))


if __name__ == '__main__':
    main()