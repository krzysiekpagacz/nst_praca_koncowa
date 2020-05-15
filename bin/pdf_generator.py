import os

from fpdf import FPDF
from bin.config import TITLE, CHAPTER_1_TITLE, AUTHOR, CHAPTER_1_INPUT, CHARTS_FOLDER, PROTOCOLS_CHART_NAME, \
    CHAPTER_3_TITLE, CHAPTER_3_INPUT, L4_PROTOCOLS_CHART_NAME, DEST_PORTS_CHART_NAME, CHAPTER_4_INPUT, CHAPTER_4_TITLE


class PDF(FPDF):
    def header(self):
        if self.page_no()==1:
            self.set_font('Arial', 'B', 15)
            # Calculate width of title and position
            w = self.get_string_width(TITLE) + 6
            self.set_x((210 - w) / 2)
            self.set_fill_color(255, 255, 255)
            self.set_text_color(128)
            # TITLE
            self.cell(w, 9, TITLE, 1, 1, 'C', 1)
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
        self.cell(0, 6, 'Chapter %d : %s' % (num, label), 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, name, input_files=None):
        # Read text file
        file = os.path.join(name)
        with open(file, 'rb') as f:
            txt = f.read().decode('latin-1')
        self.set_font('Times', '', 12)
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
            self.ln(10)
        self.chapter_title(num, title)
        self.chapter_body(name, input_files)


    def print_image(self, image_name, x=10, y=10, w=150, h=110, title=None, new_page=True):
        if new_page:
            self.add_page()
        else:
            self.ln(10)
        self.image(image_name, x=x, y=y, w=w, h=h)


def generate_pdf_file(input_files=None):
    pdf = PDF()
    pdf.set_title(TITLE)
    pdf.set_author(AUTHOR)
    try:
        pdf.print_chapter(1, CHAPTER_1_TITLE, CHAPTER_1_INPUT, input_files)
        pdf.print_chapter(2, CHAPTER_1_TITLE, CHAPTER_1_INPUT, input_files)
        pdf.print_chapter(3, CHAPTER_3_TITLE, CHAPTER_3_INPUT, new_page=True)
        try:
            pdf.print_image(os.path.join(CHARTS_FOLDER+PROTOCOLS_CHART_NAME+'.png'), y=pdf.get_y()+10, w=210-2*pdf.get_x(), new_page=False)
            pdf.print_image(os.path.join(CHARTS_FOLDER + L4_PROTOCOLS_CHART_NAME + '.png'), x=25,y=30, w=160, h=160)
        except RuntimeError:
            print('check if the screen you are trying to insert is of correct type (should be png, jpg, etc.)')
        pdf.print_chapter(4, CHAPTER_4_TITLE, CHAPTER_4_INPUT, new_page=True)
        pdf.print_image(os.path.join(CHARTS_FOLDER + DEST_PORTS_CHART_NAME + '.png'), y=pdf.get_y()+1,
                        w=210 - 2 * pdf.get_x(), new_page=False)
    except FileNotFoundError:
        print(f'file has not been found in a given location')
    pdf.output(TITLE + '.pdf', 'F')
