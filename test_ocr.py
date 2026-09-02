from app.ocr.tesseract_engine import (
    extract_text_from_image,
    extract_text_with_confidence
)


IMAGE_PATH = (
    "sample_documents/"
    "rental_agreement.png"
)


print("=" * 70)
print("RAW OCR")
print("=" * 70)

raw_text = extract_text_from_image(
    IMAGE_PATH,
    preprocess=False
)

print(raw_text)


print("\n")
print("=" * 70)
print("PRECISION OCR")
print("=" * 70)

processed_text = extract_text_from_image(
    IMAGE_PATH,
    preprocess=True
)

print(processed_text)


print("\n")
print("=" * 70)
print("OCR CONFIDENCE")
print("=" * 70)

result = extract_text_with_confidence(
    IMAGE_PATH,
    preprocess=True
)

print(
    f"Confidence: "
    f"{result['confidence']}%"
)

print(
    f"Words: "
    f"{result['word_count']}"
)