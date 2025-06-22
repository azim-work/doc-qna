from pypdf import PdfReader


def extract_text_from_pdf(fileObj) -> str:
    """
    Extracts text from a PDF file object.

    Args:
        fileObj: A file-like object containing the PDF data.

    Returns:
        str: The extracted text from the PDF.
    """
    text = ""
    reader = PdfReader(fileObj)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
