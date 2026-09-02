from app.ocr.pdf_processor import render_pdf_pages


PDF_PATH = "sample_documents/rental_agreement.pdf"


pages = render_pdf_pages(
    PDF_PATH,
    output_dir="output/pdf_pages",
    dpi=300
)

print("Rendered pages:")

for page in pages:
    print(page)