import re
from typing import Optional,List
from dateutil import parser as date_parser
from app.models.rental_agreement import (RentalAgreement,Person,
    PropertyDetails,FinancialDetails,AgreementPeriod,AgreementTerms
)



# GENERAL PATTERNS

MONEY_PATTERN = re.compile(
    r"""
    (?:
        ₹
        |
        Rs\.?
        |
        INR
    )
    \s*
    (
        \d[\d,]*
    )
    """,
    re.IGNORECASE | re.VERBOSE
)


DATE_PATTERN = re.compile(
    r"""
    (?:
        \b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b
        |
        \b\d{1,2}\.\d{1,2}\.\d{2,4}\b
        |
        \b\d{1,2}(?:st|nd|rd|th)?\s+
        (?:January|February|March|April|May|June|
        July|August|September|October|November|December)
        \s+\d{4}\b
        |
        \b(?:January|February|March|April|May|June|
        July|August|September|October|November|December)
        \s+\d{1,2},?\s+\d{4}\b
    )
    """,
    re.IGNORECASE | re.VERBOSE
)


PIN_PATTERN = re.compile(
    r"\b[1-9][0-9]{5}\b"
)


# ============================================================
# BASIC UTILITIES
# ============================================================

def normalize_money(value: Optional[str]) -> Optional[float]:
    """
    Convert monetary text into a numeric value.

    Example:
        '1,00,000' -> 100000.0
    """

    if not value:
        return None

    value = value.replace(",", "").strip()

    try:
        return float(value)

    except ValueError:
        return None


def normalize_date(value: Optional[str]) -> Optional[str]:
    """
    Convert a recognized date to YYYY-MM-DD.
    """

    if not value:
        return None

    try:
        parsed = date_parser.parse(
            value,
            dayfirst=True,
            fuzzy=True
        )

        return parsed.strftime("%Y-%m-%d")

    except (ValueError, OverflowError):

        return None


def clean_text(text: str) -> str:
    """
    Normalize OCR text without destroying
    useful document information.
    """

    text = text.replace("\r", "\n")

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


# CONTEXT SEARCH

def get_context(
    text: str,
    keyword: str,
    before: int = 150,
    after: int = 300
) -> Optional[str]:
    """
    Return text surrounding a keyword.
    """

    lower_text = text.lower()
    lower_keyword = keyword.lower()

    position = lower_text.find(
        lower_keyword
    )

    if position == -1:
        return None

    start = max(
        0,
        position - before
    )

    end = min(
        len(text),
        position + len(keyword) + after
    )

    return text[start:end]


def find_money_near_keywords(
    text: str,
    keywords: List[str]
) -> Optional[float]:
    """
    Find a monetary value near one of the
    supplied keywords.
    """

    for keyword in keywords:

        context = get_context(
            text,
            keyword
        )

        if not context:
            continue

        match = MONEY_PATTERN.search(
            context
        )

        if match:

            return normalize_money(
                match.group(1)
            )

    return None



# FINANCIAL EXTRACTION


def extract_monthly_rent(
    text: str
) -> Optional[float]:

    keywords = [
        "monthly rent",
        "monthly rental",
        "rent per month",
        "rent shall be",
        "rent of",
        "monthly rental amount"
    ]

    return find_money_near_keywords(
        text,
        keywords
    )


def extract_security_deposit(
    text: str
) -> Optional[float]:

    keywords = [
        "security deposit",
        "refundable deposit",
        "deposit amount",
        "deposit of"
    ]

    return find_money_near_keywords(
        text,
        keywords
    )


def extract_advance_payment(
    text: str
) -> Optional[float]:

    keywords = [
        "advance payment",
        "advance amount",
        "advance of",
        "rental advance"
    ]

    return find_money_near_keywords(
        text,
        keywords
    )


def extract_maintenance_fee(
    text: str
) -> Optional[float]:

    keywords = [
        "maintenance fee",
        "maintenance charges",
        "maintenance charge",
        "monthly maintenance"
    ]

    return find_money_near_keywords(
        text,
        keywords
    )



# PARTY EXTRACTION


NAME_PATTERN = re.compile(
    r"""
    \b
    (?P<title>
        Mr\.?|Mrs\.?|Ms\.?|Miss
    )
    \s+
    (?P<name>
        [A-Z][A-Za-z.'
        -]+
        (?:
            \s+
            [A-Z][A-Za-z.'
            -]+
        ){0,4}
    )
    """,
    re.VERBOSE
)


def extract_person_near_role(
    text: str,
    role_keywords: List[str]
) -> Optional[Person]:
    """
    Find a person's name associated with a
    contractual role.
    """

    lower_text = text.lower()

    for keyword in role_keywords:

        position = lower_text.find(
            keyword.lower()
        )

        if position == -1:
            continue

        start = max(
            0,
            position - 200
        )

        end = min(
            len(text),
            position + len(keyword) + 200
        )

        context = text[start:end]

        matches = list(
            NAME_PATTERN.finditer(
                context
            )
        )

        if not matches:
            continue

        # Prefer the closest name to the role.
        closest = min(
            matches,
            key=lambda match:
            abs(
                match.start()
                -
                context.lower().find(
                    keyword.lower()
                )
            )
        )

        title = closest.group(
            "title"
        ).strip()

        name = closest.group(
            "name"
        ).strip()

        return Person(
            name=f"{title} {name}",
            role=keyword
        )

    return None


def extract_landlord(
    text: str
) -> Optional[Person]:

    keywords = [
        "landlord",
        "lessor",
        "owner"
    ]

    return extract_person_near_role(
        text,
        keywords
    )


def extract_tenant(
    text: str
) -> Optional[Person]:

    keywords = [
        "tenant",
        "lessee",
        "occupant"
    ]

    return extract_person_near_role(
        text,
        keywords
    )



# DATE EXTRACTION


def extract_date_near_keywords(
    text: str,
    keywords: List[str]
) -> Optional[str]:
    """
    Find a date near a contextual keyword.
    """

    for keyword in keywords:

        context = get_context(
            text,
            keyword,
            before=50,
            after=150
        )

        if not context:
            continue

        match = DATE_PATTERN.search(
            context
        )

        if match:

            return normalize_date(
                match.group(0)
            )

    return None


def extract_agreement_date(
    text: str
) -> Optional[str]:

    keywords = [
        "agreement is made on",
        "agreement made on",
        "this agreement is dated",
        "agreement dated",
        "executed on",
        "execution date"
    ]

    return extract_date_near_keywords(
        text,
        keywords
    )


def extract_commencement_date(
    text: str
) -> Optional[str]:

    keywords = [
        "commence from",
        "commences from",
        "commencement date",
        "commencement",
        "commencing from",
        "tenancy shall commence",
        "lease shall commence",
        "rental period shall commence"
    ]

    return extract_date_near_keywords(
        text,
        keywords
    )


def extract_end_date(
    text: str
) -> Optional[str]:

    keywords = [
        "valid until",
        "valid upto",
        "valid up to",
        "agreement ends on",
        "lease ends on",
        "terminates on",
        "expiry date",
        "expiration date"
    ]

    return extract_date_near_keywords(
        text,
        keywords
    )



# DURATION

DURATION_PATTERN = re.compile(
    r"""
    \b
    (
        \d+
        \s+
        (?:months?|years?)
    )
    \b
    """,
    re.IGNORECASE | re.VERBOSE
)


def extract_duration(
    text: str
) -> Optional[str]:

    keywords = [
        "agreement period",
        "rental period",
        "lease period",
        "valid for",
        "period of",
        "term of"
    ]

    for keyword in keywords:

        context = get_context(
            text,
            keyword,
            before=50,
            after=150
        )

        if not context:
            continue

        match = DURATION_PATTERN.search(
            context
        )

        if match:
            return match.group(1)

    return None



# PROPERTY EXTRACTION


def extract_pincode(
    text: str
) -> Optional[str]:

    matches = PIN_PATTERN.findall(text)

    if matches:
        return matches[0]

    return None


def extract_property_context(
    text: str
) -> Optional[str]:

    keywords = [
        "property situated at",
        "property located at",
        "property address",
        "premises situated at",
        "premises located at",
        "rented premises",
        "residential premises"
    ]

    for keyword in keywords:

        context = get_context(
            text,
            keyword,
            before=20,
            after=250
        )

        if context:
            return context

    return None



# CITY / STATE


INDIAN_STATES = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal"
]


def extract_state(
    text: str
) -> Optional[str]:

    for state in INDIAN_STATES:

        if re.search(
            rf"\b{re.escape(state)}\b",
            text,
            re.IGNORECASE
        ):
            return state

    return None


def extract_city(
    text: str,
    state: Optional[str]
) -> Optional[str]:

    if not state:
        return None

    pattern = re.compile(
        rf"""
        ([A-Za-z][A-Za-z\s.-]+)
        \s*,\s*
        {re.escape(state)}
        """,
        re.IGNORECASE | re.VERBOSE
    )

    match = pattern.search(text)

    if match:

        city = match.group(1).strip()

        # Remove common preceding text.
        city = re.sub(
            r"^(.*?)(?:at|in|located|situated)\s+",
            "",
            city,
            flags=re.IGNORECASE
        )

        return city.strip(" ,.-")

    return None


def extract_address(
    text: str
) -> Optional[str]:

    context = extract_property_context(
        text
    )

    if not context:
        return None

    # Remove common introductory phrases.
    address = re.sub(
        r".*?(?:situated at|located at|address|premises situated at|premises located at)",
        "",
        context,
        flags=re.IGNORECASE
    )

    # Stop before common contractual phrases.
    address = re.split(
        r"\b(?:hereinafter|hereafter|the monthly rent|monthly rent|shall be)\b",
        address,
        flags=re.IGNORECASE
    )[0]

    address = address.strip(
        " \n,.-:"
    )

    return address if address else None


def extract_renewal_terms(
    text: str
) -> Optional[str]:

    keywords = [
        "renewal",
        "renew",
        "renewed"
    ]

    lower_text = text.lower()

    for keyword in keywords:

        position = lower_text.find(
            keyword
        )

        if position == -1:
            continue

        start = max(
            0,
            position - 50
        )

        end = min(
            len(text),
            position + 300
        )

        context = text[
            start:end
        ].strip()

        if context:
            return context

    return None


# CONTRACT TERMS


def extract_notice_period(
    text: str
) -> Optional[str]:

    keywords = [
        "notice period",
        "prior written notice",
        "prior notice",
        "written notice"
    ]

    for keyword in keywords:

        context = get_context(
            text,
            keyword,
            before=100,
            after=150
        )

        if not context:
            continue

        match = re.search(
            r"\b(\d+)\s+(days?|months?)\b",
            context,
            re.IGNORECASE
        )

        if match:

            return (
                f"{match.group(1)} "
                f"{match.group(2)}"
            )

    return None

def extract_termination_terms(
    text: str
) -> Optional[str]:

    keywords = [
        "termination",
        "terminate",
        "terminated"
    ]

    lower_text = text.lower()

    for keyword in keywords:

        position = lower_text.find(
            keyword
        )

        if position == -1:
            continue

        start = max(
            0,
            position - 50
        )

        end = min(
            len(text),
            position + 300
        )

        context = text[
            start:end
        ].strip()

        if context:
            return context

    return None

def extract_purpose(
    text: str
) -> Optional[str]:

    keywords = [
        "residential purpose",
        "residential use",
        "commercial purpose",
        "commercial use",
        "purpose of tenancy",
        "purpose of the agreement"
    ]

    lower_text = text.lower()

    for keyword in keywords:

        if keyword in lower_text:

            return keyword

    return None


# FINAL EXTRACTION PIPELINE


def extract_rule_based(
    text: str
) -> RentalAgreement:

    text = clean_text(text)

    landlord = extract_landlord(
        text
    )

    tenant = extract_tenant(
        text
    )

    state = extract_state(
        text
    )

    city = extract_city(
        text,
        state
    )

    return RentalAgreement(

        landlord=landlord,

        tenant=tenant,

        property=PropertyDetails(

            address=extract_address(
                text
            ),

            city=city,

            state=state,

            pincode=extract_pincode(
                text
            )
        ),

        financial=FinancialDetails(

            monthly_rent=extract_monthly_rent(
                text
            ),

            security_deposit=extract_security_deposit(
                text
            ),

            advance_payment=extract_advance_payment(
                text
            ),

            maintenance_fee=extract_maintenance_fee(
                text
            )
        ),

        period=AgreementPeriod(

            agreement_date=extract_agreement_date(
                text
            ),

            commencement_date=extract_commencement_date(
                text
            ),

            end_date=extract_end_date(
                text
            ),

            duration=extract_duration(
                text
            )
        ),

        terms=AgreementTerms(

            notice_period=extract_notice_period(
                text
            ),

            renewal_terms=extract_renewal_terms(
                text
            ),

            termination_terms=extract_termination_terms(
                text
            ),

            purpose=extract_purpose(
                text
            )
        )
    )

