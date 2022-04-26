'''
pip install PyPDF2
'''

from PyPDF2 import PdfFileWriter, PdfFileReader


def pick_up(pdf_file, pages, output_file="output.pdf"):
    output = PdfFileWriter()
    pdf_file = PdfFileReader(open("xxx.pdf", "rb"))

    for i in pages:
        output.addPage(pdf_file.getPage(i))

    output_stream = open(output_file, "wb")
    output.write(output_stream)


if __name__ == '__main__':
    pick_up("xxx.pdf", [0, 7, 8])
