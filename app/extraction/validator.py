from __future__ import annotations
import re
from datetime import datetime
from typing import Any



# BASIC VALIDATION

def validate_pincode(
    pincode: str | None
) -> bool:

    if not pincode:
        return False

    return bool(
        re.fullmatch(
            r"[1-9][0-9]{5}",
            pincode
        )
    )


def validate_amount(
    amount: Any
) -> bool:

    if amount is None:
        return False

    try:
        return float(amount) >= 0

    except (TypeError, ValueError):
        return False


def validate_date(
    date_value: str | None
) -> bool:

    if not date_value:
        return False

    try:

        datetime.strptime(
            date_value,
            "%Y-%m-%d"
        )

        return True

    except ValueError:

        return False



# AGREEMENT VALIDATION


def validate_agreement(
    agreement
) -> dict:

    errors = []

    warnings = []

    
    # PINCODE
    

    pincode = agreement.property.pincode

    if pincode:

        if not validate_pincode(pincode):

            errors.append(
                "Invalid Indian PIN code"
            )

    
    # FINANCIAL VALUES
    

    financial = agreement.financial

    financial_values = {
        "monthly_rent":
            financial.monthly_rent,

        "security_deposit":
            financial.security_deposit,

        "advance_payment":
            financial.advance_payment,

        "maintenance_fee":
            financial.maintenance_fee,

        "other_charges":
            financial.other_charges
    }

    for field, value in financial_values.items():

        if value is not None:

            if not validate_amount(value):

                errors.append(
                    f"Invalid value for {field}"
                )

    
    # DATES
   

    period = agreement.period

    dates = {
        "agreement_date":
            period.agreement_date,

        "commencement_date":
            period.commencement_date,

        "end_date":
            period.end_date
    }

    for field, value in dates.items():

        if value:

            if not validate_date(value):

                errors.append(
                    f"Invalid date for {field}"
                )

   
    # DATE ORDER
    

    if (
        period.commencement_date
        and
        period.end_date
    ):

        commencement = datetime.strptime(
            period.commencement_date,
            "%Y-%m-%d"
        )

        end = datetime.strptime(
            period.end_date,
            "%Y-%m-%d"
        )

        if commencement > end:

            errors.append(
                "Commencement date occurs after end date"
            )

    
    # MISSING IMPORTANT FIELDS
   

    if agreement.landlord is None:

        warnings.append(
            "Landlord could not be identified"
        )

    if agreement.tenant is None:

        warnings.append(
            "Tenant could not be identified"
        )

    if not period.agreement_date:

        warnings.append(
            "Agreement date could not be identified"
        )

    if not financial.monthly_rent:

        warnings.append(
            "Monthly rent could not be identified"
        )

  
    # RESULT


    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }