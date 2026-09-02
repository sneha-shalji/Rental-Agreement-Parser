import cv2
import pytesseract
from app.ocr.preprocess import preprocess_image


def extract_text_from_image(
    image_path: str,
    preprocess: bool = True,
    config: str = "--psm 3"
) -> str:

    if preprocess:

        image = preprocess_image(
            image_path
        )

    else:

        image = cv2.imread(
            image_path
        )

        if image is None:
            raise ValueError(
                f"Unable to read image: {image_path}"
            )

    text = pytesseract.image_to_string(
        image,
        lang="eng",
        config=config
    )

    return text


def extract_text_with_confidence(
    image_path: str,
    preprocess: bool = True,
    config: str = "--psm 3"
):
    """
    Extract OCR text together with word-level confidence.
    """

    if preprocess:

        image = preprocess_image(
            image_path
        )

    else:

        image = cv2.imread(
            image_path
        )

        if image is None:
            raise ValueError(
                f"Unable to read image: {image_path}"
            )

    data = pytesseract.image_to_data(
        image,
        lang="eng",
        config=config,
        output_type=pytesseract.Output.DICT
    )

    words = []
    confidences = []

    for text, confidence in zip(
        data["text"],
        data["conf"]
    ):

        text = text.strip()

        if not text:
            continue

        try:
            confidence = float(confidence)

        except ValueError:
            continue

        if confidence < 0:
            continue

        words.append(text)
        confidences.append(confidence)

    full_text = " ".join(words)

    average_confidence = (
        sum(confidences) / len(confidences)
        if confidences
        else 0.0
    )

    return {
        "text": full_text,
        "confidence": round(
            average_confidence,
            2
        ),
        "word_count": len(words)
    }