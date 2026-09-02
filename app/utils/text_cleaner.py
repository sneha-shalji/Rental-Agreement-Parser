import re
from typing import List


def normalize_line_endings(text: str) -> str:
    """
    Normalize different newline formats.
    """

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    return text


def normalize_whitespace(text: str) -> str:
    """
    Normalize excessive spaces and tabs
    while preserving line breaks.
    """

    lines = text.split("\n")

    cleaned_lines = []

    for line in lines:

        line = re.sub(
            r"[ \t]+",
            " ",
            line
        )

        line = line.strip()

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def remove_empty_lines(text: str) -> str:
    """
    Remove excessive blank lines.
    """

    lines = text.split("\n")

    cleaned_lines = []

    previous_empty = False

    for line in lines:

        if not line.strip():

            if previous_empty:
                continue

            previous_empty = True

        else:

            previous_empty = False

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def normalize_punctuation(text: str) -> str:
    """
    Normalize a few common OCR punctuation artifacts.

    This function is intentionally conservative.
    """

    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("“", '"')
    text = text.replace("”", '"')
    text = text.replace("‘", "'")
    text = text.replace("’", "'")

    return text


def clean_text(text: str) -> str:
    """
    Complete OCR text cleaning pipeline.
    """

    if not text:
        return ""

    text = normalize_line_endings(
        text
    )

    text = normalize_punctuation(
        text
    )

    text = normalize_whitespace(
        text
    )

    text = remove_empty_lines(
        text
    )

    return text.strip()

def clean_pages(pages: List[dict]) -> List[dict]:
    """
    Clean OCR text while preserving page information.
    """

    cleaned_pages = []

    for page in pages:

        cleaned_pages.append(
            {
                "page": page["page"],
                "text": clean_text(
                    page["text"]
                )
            }
        )

    return cleaned_pages