from pypdf import PdfReader

def read_pdf(file_path):

    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:

        text += page.extract_text()

    return text