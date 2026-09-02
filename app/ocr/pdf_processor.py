import fitz
from pathlib import Path

def get_pdf_page_count(pdf_path: str) -> int:
    """
    Return the number of pages in a PDF.
    """

    document = fitz.open(pdf_path)

    try:
        return len(document)
    finally:
        document.close()


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract embedded text from a PDF.
    """

    document = fitz.open(pdf_path)

    pages = []

    try:
        for page in document:
            text = page.get_text("text")
            pages.append(text)

    finally:
        document.close()

    return "\n".join(pages)


def pdf_contains_text(pdf_path: str) -> bool:
    """
    Determine whether a PDF contains meaningful
    embedded text.
    """

    document = fitz.open(pdf_path)

    try:
        for page in document:
            text = page.get_text("text").strip()

            if len(text) >= 20:
                return True

        return False

    finally:
        document.close()


def render_pdf_pages(
    pdf_path: str,
    output_dir: str = "output/pdf_pages",
    dpi: int = 300
):
    """
    Render every PDF page as a PNG image.
    """

    output_path = Path(output_dir)
    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    document = fitz.open(pdf_path)

    rendered_pages = []

    try:

        zoom = dpi / 72

        matrix = fitz.Matrix(
            zoom,
            zoom
        )

        for page_number, page in enumerate(
            document,
            start=1
        ):

            pixmap = page.get_pixmap(
                matrix=matrix,
                alpha=False
            )

            image_path = (
                output_path /
                f"page_{page_number}.png"
            )

            pixmap.save(
                str(image_path)
            )

            rendered_pages.append(
                str(image_path)
            )

    finally:
        document.close()

    return rendered_pages       