from app.utils.text_cleaner import clean_text


raw_text = """
RENTAL   AGREEMENT


This   Agreement   is   made   on   15th March, 2026.

Mr. Arun Kumar
    hereinafter referred to as the "Landlord".


The monthly rent shall be Rs. 25,000/-.


The tenant shall pay a security deposit
of Rs. 1,00,000/-.
"""


print("=" * 70)
print("RAW TEXT")
print("=" * 70)

print(raw_text)


cleaned = clean_text(
    raw_text
)


print("\n")
print("=" * 70)
print("CLEANED TEXT")
print("=" * 70)

print(cleaned)