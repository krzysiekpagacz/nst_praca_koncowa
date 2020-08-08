import os

from fpdf import FPDF
from bin.config import TITLE, CHAPTER_1_TITLE, AUTHOR, CHAPTER_1_INPUT, CHARTS_FOLDER, PROTOCOLS_CHART_NAME, \
    CHAPTER_3_TITLE, CHAPTER_3_INPUT, L4_PROTOCOLS_CHART_NAME, DEST_PORTS_CHART_NAME, CHAPTER_4_INPUT, CHAPTER_4_TITLE, \
    CHAPTER_5_TITLE, SUMMARY_CHART_NAME, SUMMARY_OPTIONS, CHAPTER_5_INPUT, CHAPTER_2_TITLE, CHAPTER_2_INPUT, \
    CHAPTER_6_INPUT, CHAPTER_6_TITLE, CHAPTER_7_TITLE, CHAPTER_7_INPUT, CHAPTER_56_INPUT, CHAPTER_55_INPUT, \
    CHAPTER_54_INPUT, CHAPTER_53_INPUT, CHAPTER_52_INPUT, CHAPTER_51_INPUT, CHAPTER_21_INPUT, CHAPTER_22_INPUT, \
    CHAPTER_25_INPUT, CHAPTER_24_INPUT, CHAPTER_23_INPUT, CHAPTER_221_INPUT, CHAPTER_222_INPUT, CHAPTER_223_INPUT, \
    CHAPTER_224_INPUT, CHAPTER_225_INPUT, CHAPTER_226_INPUT, CHAPTER_231_INPUT, CHAPTER_232_INPUT, CHAPTER_233_INPUT, \
    CHAPTER_241_INPUT


class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            self.set_font('Arial', 'B', 20)
            # Calculate width of title and position
            w = self.get_string_width(TITLE) + 6
            self.set_x((210 - w) / 2)
            self.set_fill_color(255, 255, 255)
            self.set_text_color(128)
            # TITLE
            self.cell(w, 9, TITLE, 0, 1, 'C', 1)
            self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, num, label):
        self.set_font('Arial', '', 12)
        self.set_fill_color(237, 233, 228)
        self.cell(0, 6, '%d. %s' % (num, label), 0, 1, 'L', 1)
        self.ln(4)

    def chapter_sub_title(self, num, label):
        num = float(num)
        self.set_font('Arial', '', 12)
        self.cell(0, 6, '%.1f %s' % (num, label), 0, 1, 'L', 1)
        self.ln(4)

    def chapter_3rd_pos(self, label):
        self.set_font('Arial', '', 11)
        self.cell(0, 6, '%s' % label, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, name, input_files=None):
        # Read text file
        file = os.path.join(name)
        with open(file, 'rb') as f:
            txt = f.read().decode('latin-1')
        self.set_font('Times', '', 10)
        self.multi_cell(0, 5, txt)
        self.ln()
        if input_files:
            for file in input_files:
                self.set_font('Times', '', 10)
                self.cell(0, 5, '- ' + file)
                self.ln()

    def print_chapter(self, num, title, name, input_files=None, new_page=True):
        if new_page:
            self.add_page()
        else:
            self.ln(5)
        self.chapter_title(num, title)
        self.chapter_body(name, input_files)

    def print_image(self, image_name, x=10, y=10, w=150, h=110, title=None, new_page=True):
        if new_page:
            self.add_page()
        else:
            self.ln(10)
        self.image(image_name, x=x, y=y, w=w, h=h)


def generate_pdf_file(data):
    pdf = PDF()
    pdf.set_title(TITLE)
    pdf.set_author(AUTHOR)
    try:
        pdf.print_chapter(1, CHAPTER_1_TITLE, CHAPTER_1_INPUT)
        pdf.chapter_sub_title(1.1, 'Input data analysis')
        pdf.set_font('Times', '', 10)
        pdf.cell(0, 5, 'Input data for the analysis has been delivered in a binary form. ')
        pdf.ln()
        pdf.cell(0, 5, 'After conversion it to CSV form it have been ' + str(data[0]) + ' rows in total to analysed.')
        pdf.ln()
        pdf.cell(0, 5, 'The number of rows with no zero duration time (column td) was: ' + str(data[1]))
        pdf.ln()
        pdf.cell(0, 5, 'The total amount of analysed data: ' + str(data[2]) + ' [Tb]')
        pdf.ln()
        pdf.cell(0, 5, 'Number of packets: ' + str(data[3]))
        pdf.ln()
        pdf.cell(0, 5, 'Based on the router address from column ra it was possible to identify the amount of subntest in the university net.')
        pdf.ln()
        pdf.cell(0, 5, 'Below the router IP address has been presented together with the total amount of flows per each of this')
        pdf.ln()
        for item in data[4]:
            pdf.cell(0, 5, 'Router: '+item[0]+' ===> number of flows: '+str(item[1]))
            pdf.ln()
        pdf.ln()
        pdf.add_page()
        pdf.print_chapter(2, CHAPTER_2_TITLE, CHAPTER_2_INPUT, new_page=False)
        pdf.chapter_sub_title(2.1, 'Collecting network logs')
        pdf.chapter_body(CHAPTER_21_INPUT)
        pdf.chapter_sub_title(2.2, 'Module core.py')
        pdf.chapter_body(CHAPTER_22_INPUT)
        pdf.chapter_3rd_pos('get_data(files_count=3)')
        pdf.chapter_body(CHAPTER_221_INPUT)
        pdf.chapter_3rd_pos('get_destination_ports_df(data)')
        pdf.chapter_body(CHAPTER_222_INPUT)
        pdf.chapter_3rd_pos('get_bytes_per_protocols_df(data)')
        pdf.chapter_body(CHAPTER_223_INPUT)
        pdf.chapter_3rd_pos('get_summary_df(data)')
        pdf.chapter_body(CHAPTER_224_INPUT)
        pdf.chapter_3rd_pos('get_input_file_names(data)')
        pdf.chapter_body(CHAPTER_225_INPUT)
        pdf.chapter_3rd_pos('main')
        pdf.chapter_body(CHAPTER_226_INPUT)
        pdf.chapter_sub_title(2.3, 'Module charts.py')
        pdf.chapter_body(CHAPTER_23_INPUT)
        pdf.chapter_3rd_pos('bytes_per_L4_protocol_chart(data)')
        pdf.chapter_body(CHAPTER_231_INPUT)
        pdf.chapter_3rd_pos('destination_ports_chart(data)')
        pdf.chapter_body(CHAPTER_232_INPUT)
        pdf.chapter_3rd_pos('get_summary_chart(data)')
        pdf.chapter_body(CHAPTER_233_INPUT)
        pdf.chapter_sub_title(2.4, 'Module pdf_generator.py')
        pdf.chapter_body(CHAPTER_24_INPUT)
        pdf.chapter_body(CHAPTER_241_INPUT)
        pdf.chapter_3rd_pos('generate_pdf_file(input_files=None)')
        pdf.chapter_sub_title(2.5, 'Module config.py')
        pdf.chapter_body(CHAPTER_25_INPUT)
        pdf.print_chapter(3, CHAPTER_3_TITLE, CHAPTER_3_INPUT, new_page=True)

        pdf.print_image(os.path.join(CHARTS_FOLDER + L4_PROTOCOLS_CHART_NAME + '.png'), x=25, y=30, w=160, h=160)

        pdf.print_chapter(4, CHAPTER_4_TITLE, CHAPTER_4_INPUT, new_page=True)
        pdf.print_image(os.path.join(CHARTS_FOLDER + DEST_PORTS_CHART_NAME + '.png'), y=pdf.get_y() + 1,
                        w=210 - 2 * pdf.get_x(), new_page=False)
        pdf.add_page()
        pdf.chapter_title(5, CHAPTER_5_TITLE)
        pdf.chapter_sub_title(5.1, 'Flows')
        pdf.chapter_body(CHAPTER_51_INPUT)
        pdf.print_image(os.path.join(CHARTS_FOLDER + SUMMARY_CHART_NAME + SUMMARY_OPTIONS[0] + '.png'),
                        y=pdf.get_y() + 1,
                        w=210 - 2 * pdf.get_x(), new_page=False)
        pdf.add_page()
        pdf.chapter_sub_title(5.2, 'Bytes')
        pdf.chapter_body(CHAPTER_52_INPUT)
        pdf.print_image(os.path.join(CHARTS_FOLDER + SUMMARY_CHART_NAME + SUMMARY_OPTIONS[1] + '.png'),
                        y=pdf.get_y() + 1,
                        w=210 - 2 * pdf.get_x(), new_page=False)
        pdf.add_page()
        pdf.chapter_sub_title(5.3, 'Packets')
        pdf.chapter_body(CHAPTER_53_INPUT)
        pdf.print_image(os.path.join(CHARTS_FOLDER + SUMMARY_CHART_NAME + SUMMARY_OPTIONS[2] + '.png'),
                        y=pdf.get_y() + 10,
                        w=210 - 2 * pdf.get_x(), new_page=False)
        pdf.add_page()
        pdf.chapter_sub_title(5.4, 'Average bytes per packet')
        pdf.chapter_body(CHAPTER_56_INPUT)
        pdf.print_image(os.path.join(CHARTS_FOLDER + SUMMARY_CHART_NAME + SUMMARY_OPTIONS[5] + '.png'),
                        y=pdf.get_y() + 10,
                        w=210 - 2 * pdf.get_x(), new_page=False)
        pdf.print_chapter(6, CHAPTER_6_TITLE, CHAPTER_6_INPUT, new_page=True)
        pdf.print_chapter(7, CHAPTER_7_TITLE, CHAPTER_7_INPUT, new_page=True)
    except FileNotFoundError:
        print(f'file has not been found in a given location')
    pdf.output(TITLE + '.pdf', 'F')
