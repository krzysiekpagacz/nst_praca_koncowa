# core.py configuration
INPUT_FILES = 'netflow_csv'

# charts.py configuration
COLORS = ['#1531d1', '#fa1616', '#03fcbe', '#f6fa16', '#b515d1', '#4a7531', '#d8c3db', '#d1158c', '#15d183', '#87857b','#ab1d53']
CHARTS_FOLDER = '../resources/charts/'
## bar_of_pie_protocols_chart
PROTOCOLS_CHART_NAME = 'protocols'
PROTOCOLS_CHART_TITLE = 'Distribution of bytes among protocols'
## bytes_per_L4_protocol_chart
L4_PROTOCOLS_CHART_NAME = 'transport_protocols'
L4_PROTOCOLS_CHART_TITLE = 'Distribution of Bytes per Transport Layer Protocols'
## dest_ports_chart
DEST_PORTS_CHART_NAME = 'ports'
DEST_PORTS_CHART_TITLE = 'TOP 10 Services'
DEST_PORTS_X_LABEL = 'Number of connection'
## get_summary_chart
SUMMARY_CHART_NAME = 'summary_'
SUMMARY_CHART_TITLE = 'in 5 minutes time interval for the day: '
SUMMARY_CHART_X_LABEL = 'time [hours:minutes]'
LABEL_TITLE_FONT_SIZE = 16
SUMMARY_OPTIONS = ['flows', 'bytes', 'packets', 'avg_bps', 'avg_pps', 'avg_bpp']

# pdf_generator.py configuration
TITLE = 'Flow Traffic Analysis'
AUTHOR = 'Krzysztof Pagacz'
CHAPTER_1_TITLE = 'Introduction'
CHAPTER_1_INPUT = '../resources/text/chapter_1.txt'
CHAPTER_3_TITLE = 'Protocols'
CHAPTER_3_INPUT = '../resources/text/protocols.txt'
CHAPTER_4_TITLE = 'Services'
CHAPTER_4_INPUT = '../resources/text/ports.txt'
CHAPTER_5_TITLE = 'Summary of data traffic for a given day'
CHAPTER_5_INPUT = '../resources/text/summary.txt'

# known ports (up to 49152)
PORT_NAME = {
	53.0 : 'DNS',
	443.0 : 'HTTPS',
	80.0: 'HTTP',
	6881.0: 'Bit Torrent',
	445.0: 'SMB File Sharing',
	123.0: 'NTP',
	3478.0: 'STUN/TURN',  # a protocol for NAT Traversal
	23.0: 'Telnet',
	5222.0: 'XMPP',
	5938.0: 'Team Viewer'
}
