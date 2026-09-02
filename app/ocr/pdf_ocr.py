from app.models.document import (
    DocumentPage,
    OCRDocument
)

from app.ocr.pdf_processor import (
    render_pdf_pages
)

from app.ocr.tesseract_engine import (
    extract_text_with_confidence
)

from app.utils.text_cleaner import (
    clean_text
)


def extract_document_from_scanned_pdf(pdf_path: str) -> OCRDocument:
    """
    Convert a scanned PDF into an OCRDocument.
    """

    page_images = render_pdf_pages(
        pdf_path,
        output_dir="output/pdf_pages",
        dpi=300
    )

    pages = []

    for page_number, image_path in enumerate(
        page_images,
        start=1
    ):

        result = extract_text_with_confidence(
            image_path,
            preprocess=True
        )

        cleaned_text = clean_text(
            result["text"]
        )

        page = DocumentPage(
            page_number=page_number,
            text=cleaned_text,
            confidence=result["confidence"]
        )

        pages.append(page)

    return OCRDocument(
        pages=pages
    )