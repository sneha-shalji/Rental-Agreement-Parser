from app.ocr.pdf_ocr import extract_text_from_scanned_pdf


PDF_PATH = "sample_documents/rental_agreement.pdf"


pages = extract_text_from_scanned_pdf(
    PDF_PATH
)


for page in pages:

    print("\n")
    print("=" * 70)
    print(f"PAGE {page['page']}")
    print("=" * 70)

    print(page["text"])