import os

from fpdf import FPDF
from bin.config import TITLE, CHAPTER_1_TITLE, AUTHOR, CHAPTER_1_INPUT, CHARTS_FOLDER, PROTOCOLS_CHART_NAME


class PDF(FPDF):
    def header(self):
        if self.page_no()==1:
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Calculate width of title and position
            w = self.get_string_width(TITLE) + 6
            self.set_x((210 - w) / 2)
            # Colors of frame, background and text
            # self.set_draw_color(0, 80, 180)
            self.set_fill_color(255, 255, 255)
            self.set_text_color(128)
            # Thickness of frame (1 mm)
            # self.set_line_width(1)
            # TITLE
            self.cell(w, 9, TITLE, 1, 1, 'C', 1)
            # Line break
            self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, num, label):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Background color
        self.set_fill_color(237, 233, 228)
        # Title
        self.cell(0, 6, 'Chapter %d : %s' % (num, label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, name, input_files=None):
        # Read text file
        file = os.path.join(name)
        with open(file, 'rb') as fh:
            txt = fh.read().decode('latin-1')
        # Times 12
        self.set_font('Times', '', 12)
        # Output justified text
        self.multi_cell(0, 5, txt)
        # Line break
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


    def print_image(self, image_name, w=180, h=110,title=None, new_page=True):
        if new_page:
            self.add_page()
        else:
            self.ln(10)
        self.image(image_name, x=10, y=20, w=w, h=h)


def generate_pdf_file(input_files=None):
    pdf = PDF()
    pdf.set_title(TITLE)
    pdf.set_author(AUTHOR)
    try:
        pdf.print_chapter(1, CHAPTER_1_TITLE, CHAPTER_1_INPUT, input_files)
        pdf.print_chapter(2, CHAPTER_1_TITLE, CHAPTER_1_INPUT, input_files)
        pdf.print_chapter(3, CHAPTER_1_TITLE, CHAPTER_1_INPUT, new_page=False)
        try:
            pdf.print_image(os.path.join(CHARTS_FOLDER+PROTOCOLS_CHART_NAME+'.png'))
        except RuntimeError:
            print('check if the screen you are trying to insert is of correct type (should be png, jpg, etc.)')
    except FileNotFoundError:
        print(f'file {CHAPTER_1_TITLE} has not been found in a given location')
    pdf.output(TITLE + '.pdf', 'F')

if __name__ == '__main__':
    generate_pdf_file()