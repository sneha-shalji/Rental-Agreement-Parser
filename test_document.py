from app.ocr.pdf_ocr import (
    extract_document_from_scanned_pdf
)


PDF_PATH = (
    "sample_documents/"
    "rental_agreement.pdf"
)


document = extract_document_from_scanned_pdf(
    PDF_PATH
)


print("=" * 70)
print("DOCUMENT")
print("=" * 70)

print(
    f"Number of pages: "
    f"{len(document.pages)}"
)


for page in document.pages:

    print("\n")
    print("=" * 70)

    print(
        f"PAGE {page.page_number}"
    )

    print(
        f"OCR Confidence: "
        f"{page.confidence}%"
    )

    print("=" * 70)

    print(page.text)


print("\n")
print("=" * 70)
print("FULL DOCUMENT TEXT")
print("=" * 70)

print(document.full_text)