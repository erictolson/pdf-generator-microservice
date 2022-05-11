
"""
Reads a key from a txt file. Searches a json file with the key.
Exports the key values in a pdf form. Writes the PDF file name
to the txt file.  
"""

import json
from fpdf import FPDF
from time import sleep


TXTFILE = 'recipe.txt'          # update to txt file name for read
JSONFILE = 'recipes.json'       # update to json file name for read
CATEGORY = 'recipe'             # update category to preceed number in PDF file name

def create_pdf() -> object:
    """
    Create pdf object from FPDF class

    :return: PDF object
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    return pdf


def read_txt(file_name) -> object:
    """
    Open/reads txt file argument

    :param file_name(str)
    :return: file content
    """
    with open(file_name, 'r') as txt_file:
        content = txt_file.read()
        return content


def load_json(file_name) -> object:
    """
    Opens/loads json file argument

    :param file_name(str)
    :return: file contentquit
    """
    with open(file_name, 'r') as json_file:
        content = json.load(json_file)
        return content


def add_pdf_content(txt_content, json_content, pdf) -> None:
    """
    Searches json content with key from txt_content. Adds relevant data to pdf object.

    :param txt_content: txt file content for json search
    :param json_content: json file content to search
    :param pdf: pdf object to update
    :return: none
    """
    for key, value in json_content.items():
        if key == txt_content:
            for key, value in value.items():
                if isinstance(value, dict):
                    pdf.cell(200, 10, txt=key.title() + ":", ln=1, align='C')
                    for key, value in value.items():
                        pdf.cell(200, 10, txt=key + ": " + str(value), ln=1, align='C')
                else:
                    pdf.cell(200, 10, txt=key.title() + ": " + str(value), ln=1, align='C')


def generate_pdf(category_name, txt_content, pdf) -> str:
    """
    Generate pdf file from pdf object with relevant naming 'category + key from txt file'

    :param category_name: category for pdf title
    :param txt_content: txt identifier for pdf title
    :param pdf: pdf object to generate pdf file
    :return: pdf file name
    """
    pdf.output(f"{category_name}{txt_content}.pdf")
    return f"{category_name}{txt_content}.pdf"


def write_txt(file_name, pdf_file) -> None:
    """
    Write generated pdf file name to txt file

    :param file_name: txt file(str) to write to
    :param pdf_file: pdf file name to write(str)
    :return: none
    """
    with open(file_name, 'w') as txt_file:
        txt_file.write(pdf_file)


def main():

    initial_content = read_txt(TXTFILE)                                     # initialize variables for while loop comparison

    while True:
        updated_content = read_txt(TXTFILE)
                                                                            # watch for txt change
        if updated_content != initial_content:
            if updated_content == 'QUIT':                                   # exit program upon cue
                break

            pdf = create_pdf()                                              # create pdf object for file generation

            json_content = load_json(JSONFILE)                              # load json content for data search

            add_pdf_content(updated_content, json_content, pdf)             # update pdf object with data

            pdf_file_name = generate_pdf(CATEGORY, updated_content, pdf)    # generate pdf file with appropriate name

            write_txt(TXTFILE, pdf_file_name)                               # write pdf file name to txt file

            initial_content = read_txt(TXTFILE)                             # update comparison variable
        
        sleep(.25)

if __name__ == "__main__":
    main()
