SYSTEM_PROMPT = """
You are an information extraction system for rental agreements.

Extract facts directly from the provided document.

IMPORTANT RULES:

- Use ONLY information explicitly present in the document.
- Do NOT guess.
- Do NOT invent missing information.
- Identify people by their roles in the agreement.
- Return dates in the same form as they appear in the document.
- Return monetary amounts as numbers.
- If a value is not present, use null.
- Return JSON only.
"""


EXTRACTION_PROMPT = """
Read the rental agreement below and extract the following information.

LANDLORD:
The person identified as Landlord.

TENANT:
The person identified as Tenant.

PROPERTY:
The complete property address, city, state and PIN code.

FINANCIAL:
Monthly rent.
Security deposit.
Advance payment.
Maintenance fee.
Other charges.

PERIOD:
Date on which the agreement was made.
Date on which the tenancy starts/commences.
Date on which the agreement ends.
Duration of the agreement.

TERMS:
Notice period.
Renewal terms.
Termination terms.
Purpose of the tenancy.

Use the exact wording from the document for names and text fields.

For example, if the document says:

"Mr. Arun Kumar, hereinafter referred to as the Landlord"

then landlord.name must be:

"Mr. Arun Kumar"

If the document says:

"monthly rent shall be Rs. 25,000/-"

then monthly_rent must be:

25000

If information is not explicitly available, return null.

Return ONLY this JSON object:

{{
  "landlord": {{
    "name": null
  }},
  "tenant": {{
    "name": null
  }},
  "property": {{
    "address": null,
    "city": null,
    "state": null,
    "pincode": null
  }},
  "financial": {{
    "monthly_rent": null,
    "security_deposit": null,
    "advance_payment": null,
    "maintenance_fee": null,
    "other_charges": null
  }},
  "period": {{
    "agreement_date": null,
    "commencement_date": null,
    "end_date": null,
    "duration": null
  }},
  "terms": {{
    "notice_period": null,
    "renewal_terms": null,
    "termination_terms": null,
    "purpose": null
  }}
}}

RENTAL AGREEMENT:

{document_text}
"""