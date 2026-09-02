from dataclasses import dataclass
from typing import List


@dataclass
class DocumentPage:
    page_number: int
    text: str
    confidence: float = 0.0


@dataclass
class OCRDocument:
    pages: List[DocumentPage]

    @property
    def full_text(self) -> str:
        """
        Combine all pages while preserving
        page boundaries.
        """

        return "\n\n".join(
            page.text
            for page in self.pages
        )