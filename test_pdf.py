from app.ocr.pdf_processor import get_pdf_page_count, extract_text_from_pdf,pdf_contains_text



PDF_PATH = "sample_documents/rental_agreement.pdf"


print(
    f"Pages: {get_pdf_page_count(PDF_PATH)}"
)

if pdf_contains_text(PDF_PATH):

    print("PDF TYPE: Text-based PDF")

    text = extract_text_from_pdf(PDF_PATH)

    print("=" * 70)
    print("EXTRACTED TEXT")
    print("=" * 70)

    print(text)

else:

    print("PDF TYPE: Scanned/Image PDF")
    print("OCR is required.")