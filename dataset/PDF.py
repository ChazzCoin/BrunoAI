from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from dataset import CLEANER, DataCleaner
from FNLP.Language import Sentences
import os, json
import fitz

PDF_MODEL = lambda x: {}

PostProcessor = DataCleaner.TextCleaner()

def list_of_strings_to_string(content: [str]) -> str:
    temp = ""
    for item in content:
        temp += " " + str(item)
    return str(temp).strip()

class FPDF:
    file_paths = []
    file_texts = [{}]

    def __init__(self, file_path):
        if OS.is_directory(file_path):
            temp = OS.get_files_in_directory(file_path)
            for t in temp:
                self.file_paths.append(f"{file_path}/{t}")
            print(self.file_paths)
        else:
            self.file_paths = [file_path]

    def run(self):
        for file_path in self.file_paths:
            try:
                text = self.extract_text_from_pdf_v2(file_path)
                # textOld = self.extract_text_from_pdf(file_path)
                sents = self.post_process_text(text)
                cleaned = []
                for s in sents:
                    cleaned_s = CLEANER.clean_text(s)
                    cleaned.append(cleaned_s)
                full_text = list_of_strings_to_string(cleaned)
                for_ai = Sentences.filter_sentences_for_ai_training(cleaned)
                j = {
                    "text": full_text,
                    "training": for_ai,
                    "file": file_path
                }
                self.file_texts.append(j)
            except Exception as e:
                print(f"Error: {e}")
        OS.save_dict_to_file("pdf_training_data", self.file_texts, file_path=OS.get_cwd())
        return self.file_texts

    def post_process_text(self, text_in:str) -> str:
        text_out = Sentences.to_sentences(text_in)
        return text_out

    def extract_text_from_pdf(self, path):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()
        return text

    def extract_text_from_pdf_v2(self, pdf_path: str) -> str:
        """
        Extract text from a PDF file.

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            str: The extracted text.
        """
        try:
            # Open the PDF file
            pdf_document = fitz.open(pdf_path)

            # Initialize an empty string to store the text
            extracted_text = ""

            # Iterate over each page
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                extracted_text += page.get_text()

            return extracted_text

        except Exception as e:
            print(f"An error occurred while extracting text from the PDF: {e}")
            return ""

if __name__ == '__main__':
    from F import OS
    cwd = OS.get_cwd()
    file = "/Users/chazzromeo/Desktop/projectrpg/Extract"
    # file = f"{cwd}/../Utils/mlpython.pdf"
    ps = FPDF(file).run()