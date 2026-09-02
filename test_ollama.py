from app.llm.extractor import (
    extract_with_llm
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


result = extract_with_llm(
    sample_text
)


print("\n========== FINAL RESULT ==========\n")

print(
     result.model_dump_json(
        indent=2
    )
)