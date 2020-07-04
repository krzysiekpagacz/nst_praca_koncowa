# core.py configuration
INPUT_FILES = 'netflow_csv_all'

NUMBER_OF_PORTS = 8

# charts.py configuration
COLORS = ['#1531d1', '#fa1616', '#03fcbe', '#f6fa16', '#b515d1', '#4a7531', '#d8c3db', '#d1158c', '#15d183', '#87857b',
          '#ab1d53']
CHARTS_FOLDER = '../resources/charts/'
## bar_of_pie_protocols_chart
PROTOCOLS_CHART_NAME = 'protocols'
PROTOCOLS_CHART_TITLE = 'Distribution of bytes among protocols'
## bytes_per_L4_protocol_chart
L4_PROTOCOLS_CHART_NAME = 'transport_protocols'
L4_PROTOCOLS_CHART_TITLE = 'Distribution of Bytes per Transport Layer Protocols'
## dest_ports_chart
DEST_PORTS_CHART_NAME = 'ports'
DEST_PORTS_CHART_TITLE = 'TOP '+str(NUMBER_OF_PORTS)+' Services'
DEST_PORTS_X_LABEL = 'Number of connections'
## get_summary_chart
SUMMARY_CHART_NAME = 'summary_'
SUMMARY_CHART_TITLE = 'in 5 minutes time interval'
SUMMARY_CHART_X_LABEL = 'time [hours:minutes]'
LABEL_TITLE_FONT_SIZE = 12
SUMMARY_OPTIONS = ['flows', 'bytes', 'packets', 'avg_bps', 'avg_pps', 'avg_bpp']

# pdf_generator.py configuration
TITLE = 'Flow Traffic Analysis'
AUTHOR = 'Krzysztof Pagacz'
CHAPTER_1_TITLE = 'Introduction'
CHAPTER_1_INPUT = '../resources/text/chapter_1.txt'
CHAPTER_2_TITLE = 'Script architecture'
CHAPTER_2_INPUT = '../resources/text/chapter_2.txt'
CHAPTER_3_TITLE = 'Protocols'
CHAPTER_3_INPUT = '../resources/text/protocols.txt'
CHAPTER_4_TITLE = 'Services'
CHAPTER_4_INPUT = '../resources/text/ports.txt'
CHAPTER_5_TITLE = 'Summary of data traffic for a given day'
CHAPTER_5_INPUT = '../resources/text/summary.txt'

PORT_NAME = {
    53.0: 'DNS',
    443.0: 'HTTPS',
    80.0: 'HTTP',
    6881.0: 'Bit Torrent',
    445.0: 'SMB File Sharing',
    123.0: 'NTP',
    3478.0: 'STUN/TURN',  # a protocol for NAT Traversal
    23.0: 'Telnet',
    5222.0: 'XMPP',
    5938.0: 'Team Viewer',
    993.0: 'IMAP',
    22.0: 'SSH',
    6667.0: 'IRC',
    27000.0: 'Online Games',
    27001.0: 'Online Games',
    27002.0: 'Online Games',
    27003.0: 'Online Games',
    27004.0: 'Online Games',
    27005.0: 'Online Games',
    27006.0: 'Online Games',
    27007.0: 'Online Games',
    27008.0: 'Online Games',
    27009.0: 'Online Games',
    27010.0: 'Online Games',
    27011.0: 'Online Games',
    27012.0: 'Online Games',
    27013.0: 'Online Games',
    27014.0: 'Online Games',
    27015.0: 'Online Games',
    27016.0: 'Online Games',
    27017.0: 'Online Games',
    27018.0: 'Online Games',
    27019.0: 'Online Games',
    27020.0: 'Online Games',
    27021.0: 'Online Games',
    27022.0: 'Online Games',
    27023.0: 'Online Games',
    27024.0: 'Online Games',
    27025.0: 'Online Games',
    27026.0: 'Online Games',
    27027.0: 'Online Games',
    27028.0: 'Online Games',
    27029.0: 'Online Games',
    27030.0: 'Online Games',
    27031.0: 'Online Games',
    27032.0: 'Online Games',
    27033.0: 'Online Games',
    27034.0: 'Online Games',
    27035.0: 'Online Games',
    27036.0: 'Online Games',
    27037.0: 'Online Games',
    27038.0: 'Online Games',
    27039.0: 'Online Games',
    27040.0: 'Online Games',
    27041.0: 'Online Games',
    27042.0: 'Online Games',
    27043.0: 'Online Games',
    27044.0: 'Online Games',
    27045.0: 'Online Games',
    27046.0: 'Online Games',
    27047.0: 'Online Games',
    27048.0: 'Online Games',
    27049.0: 'Online Games',
    27050.0: 'Online Games'
}
