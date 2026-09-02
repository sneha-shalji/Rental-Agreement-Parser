from app.extraction.extraction_service import (
    extract_agreement
)


sample_text = """
RENTAL AGREEMENT

This agreement is made on 15th March 2026.

Mr. Arun Kumar, hereinafter referred to as
the Landlord, and Ms. Priya Nair,
hereinafter referred to as the Tenant.

The property situated at 14 MG Road,
Ernakulam, Kerala - 682016.

The monthly rent shall be Rs. 25,000/-.

The tenant shall pay a security deposit
of Rs. 1,00,000/-.

An advance payment of Rs. 25,000/- shall
be made by the tenant.

Maintenance charges shall be Rs. 2,000/-
per month.

The agreement shall commence from
01/04/2026 and remain valid for 11 months.

Either party shall provide 2 months
prior written notice.
"""


result = extract_agreement(
    sample_text
)


print("\n================ AGREEMENT ================\n")

print(
    result["agreement"].model_dump_json(
        indent=2
    )
)


print("\n================ CONFIDENCE ================\n")

for field, score in result[
    "field_confidence"
].items():

    print(
        f"{field}: {score}"
    )


print("\n================ OVERALL ================\n")

print(
    result["overall_confidence"]
)


print("\n================ VALIDATION ================\n")

print(
    result["validation"]
)