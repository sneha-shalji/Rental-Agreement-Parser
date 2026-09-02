import re
from typing import Optional,List
from dateutil import parser as date_parser
from app.models.rental_agreement import (
    RentalAgreement,
    Person,
    PropertyDetails,
    FinancialDetails,
    AgreementPeriod,
    AgreementTerms
)

def normalize_money(value: str) -> Optional[float]:
    """
    Convert a monetary string into a numeric value.

    Examples:
        '25,000' -> 25000.0
        '1,00,000' -> 100000.0
    """

    if not value:
        return None

    value = value.replace(",", "")
    value = value.strip()

    try:
        return float(value)

    except ValueError:
        return None
    
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
        \d{1,3}
        (?:
            [,\s]\d{2,3}
        )*
        |
        \d+
    )
    """,
    re.IGNORECASE | re.VERBOSE
)


def extract_money_values(text: str) -> List[float]:
    """
    Extract all monetary values from text.
    """

    matches = MONEY_PATTERN.findall(text)

    values = []

    for match in matches:

        value = normalize_money(match)

        if value is not None:
            values.append(value)

    return values    

def find_value_near_keywords(
    text: str,
    keywords: List[str],
    pattern: re.Pattern
):
    """
    Find a value occurring near one of the supplied keywords.
    """

    lower_text = text.lower()

    for keyword in keywords:

        keyword_position = lower_text.find(
            keyword.lower()
        )

        if keyword_position == -1:
            continue

        start = max(
            0,
            keyword_position - 150
        )

        end = min(
            len(text),
            keyword_position + 300
        )

        context = text[start:end]

        match = pattern.search(context)

        if match:

            return match.group(1)

    return None

def extract_monthly_rent(text: str):
    """
    Extract monthly rent using contextual keywords.
    """

    keywords = [
        "monthly rent",
        "monthly rental",
        "rent per month",
        "rent shall be",
        "rent of"
    ]

    value = find_value_near_keywords(
        text,
        keywords,
        MONEY_PATTERN
    )

    return normalize_money(value)

def extract_security_deposit(text: str):
    """
    Extract security deposit.
    """

    keywords = [
        "security deposit",
        "refundable deposit",
        "deposit amount",
        "deposit of"
    ]

    value = find_value_near_keywords(
        text,
        keywords,
        MONEY_PATTERN
    )

    return normalize_money(value)

def extract_advance_payment(text: str):
    """
    Extract advance payment.
    """

    keywords = [
        "advance payment",
        "advance amount",
        "advance of",
        "rental advance"
    ]

    value = find_value_near_keywords(
        text,
        keywords,
        MONEY_PATTERN
    )

    return normalize_money(value)


def extract_maintenance_fee(text: str):
    """
    Extract maintenance fee.
    """

    keywords = [
        "maintenance fee",
        "maintenance charges",
        "maintenance charge",
        "monthly maintenance"
    ]

    value = find_value_near_keywords(
        text,
        keywords,
        MONEY_PATTERN
    )

    return normalize_money(value)


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

def extract_dates(text: str) -> List[str]:
    """
    Extract date-like expressions from text.
    """

    return DATE_PATTERN.findall(text)

def normalize_date(date_text: str) -> Optional[str]:
    """
    Convert a recognized date into YYYY-MM-DD.
    """

    if not date_text:
        return None

    try:

        parsed = date_parser.parse(
            date_text,
            dayfirst=True,
            fuzzy=True
        )

        return parsed.strftime(
            "%Y-%m-%d"
        )

    except (ValueError, OverflowError):

        return None
    
DURATION_PATTERN = re.compile(
    r"""
    \b(
        \d+
        \s+
        (?:months?|years?)
    )\b
    """,
    re.IGNORECASE | re.VERBOSE
)


def extract_duration(text: str):
    """
    Extract agreement duration.
    """

    match = DURATION_PATTERN.search(
        text
    )

    if match:
        return match.group(1)

    return None

NOTICE_PATTERN = re.compile(
    r"""
    \b(
        \d+
        \s+
        (?:days?|months?)
    )\b
    """,
    re.IGNORECASE | re.VERBOSE
)


def extract_notice_period(text: str):
    """
    Extract notice period from termination/notice clauses.
    """

    keywords = [
        "notice period",
        "notice of",
        "prior notice",
        "written notice"
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
            position - 100
        )

        end = min(
            len(text),
            position + 200
        )

        context = text[start:end]

        match = NOTICE_PATTERN.search(
            context
        )

        if match:
            return match.group(1)

    return None

PIN_PATTERN = re.compile(
    r"\b[1-9][0-9]{5}\b"
)


def extract_pincodes(text: str) -> List[str]:
    """
    Extract Indian six-digit PIN codes.
    """

    return PIN_PATTERN.findall(
        text
    )

PARTY_PATTERN = re.compile(
    r"""
    (?P<title>
        Mr\.?|Mrs\.?|Ms\.?|Miss
    )
    \s+
    (?P<name>
        [A-Z][A-Za-z]+
        (?:
            \s+
            [A-Z][A-Za-z]+
        ){1,4}
    )
    """,
    re.VERBOSE
)

def extract_candidate_names(text: str):
    """
    Extract candidate person names based on title patterns.
    """

    matches = PARTY_PATTERN.finditer(
        text
    )

    return [
        match.group("name").strip()
        for match in matches
    ]

def extract_rule_based(text: str) -> dict:
    """
    Extract rental agreement information
    using deterministic rules.
    """

    dates = extract_dates(text)

    return {
        "agreement_date": (
            normalize_date(dates[0])
            if dates
            else None
        ),

        "all_dates": [
            normalize_date(date)
            for date in dates
        ],

        "agreement_duration": (
            extract_duration(text)
        ),

        "monthly_rent": (
            extract_monthly_rent(text)
        ),

        "security_deposit": (
            extract_security_deposit(text)
        ),

        "advance_payment": (
            extract_advance_payment(text)
        ),

        "maintenance_fee": (
            extract_maintenance_fee(text)
        ),

        "notice_period": (
            extract_notice_period(text)
        ),

        "pincodes": (
            extract_pincodes(text)
        ),

        "candidate_names": (
            extract_candidate_names(text)
        )
    }

def build_rule_based_agreement(
    text: str
) -> RentalAgreement:
    """
    Convert rule-based extraction results
    into a validated RentalAgreement model.
    """

    result = extract_rule_based(
        text
    )

    candidate_names = result.get(
        "candidate_names",
        []
    )

    landlord = None
    tenant = None

    if len(candidate_names) >= 1:

        landlord = Person(
            name=candidate_names[0],
            role="landlord"
        )

    if len(candidate_names) >= 2:

        tenant = Person(
            name=candidate_names[1],
            role="tenant"
        )

    all_dates = result.get(
        "all_dates",
        []
    )

    agreement_date = (
        all_dates[0]
        if len(all_dates) > 0
        else None
    )

    commencement_date = (
        all_dates[1]
        if len(all_dates) > 1
        else None
    )

    return RentalAgreement(

        landlord=landlord,

        tenant=tenant,

        property=PropertyDetails(
            pincode=(
                result["pincodes"][0]
                if result["pincodes"]
                else None
            )
        ),

        financial=FinancialDetails(
            monthly_rent=result[
                "monthly_rent"
            ],
            security_deposit=result[
                "security_deposit"
            ],
            advance_payment=result[
                "advance_payment"
            ],
            maintenance_fee=result[
                "maintenance_fee"
            ]
        ),

        period=AgreementPeriod(
            agreement_date=agreement_date,
            commencement_date=commencement_date,
            duration=result[
                "agreement_duration"
            ]
        ),

        terms=AgreementTerms(
            notice_period=result[
                "notice_period"
            ]
        )
    )
