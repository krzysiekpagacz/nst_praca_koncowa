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

# pdf_generator.py configuration
TITLE = 'Flow Traffic Analysis'
AUTHOR = 'Krzysztof Pagacz'
CHAPTER_1_TITLE = 'Introduction'
CHAPTER_1_INPUT = '../resources/text/chapter_1.txt'
CHAPTER_3_TITLE = 'Protocols'
CHAPTER_3_INPUT = '../resources/text/protocols.txt'
CHAPTER_4_TITLE = 'Services'
CHAPTER_4_INPUT = '../resources/text/ports.txt'

# well known ports (up to 49152)
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
