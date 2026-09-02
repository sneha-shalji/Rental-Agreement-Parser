from app.extraction.rule_extractor import (
    extract_rule_based
)

from app.extraction.validator import (
    validate_agreement
)

from app.extraction.confidence import (
    confidence_for_value,
    calculate_overall_confidence
)


def extract_agreement(
    text: str
):

    # STEP 1: RULE-BASED EXTRACTION
    

    agreement = extract_rule_based(
        text
    )

    
    # STEP 2: VALIDATION
    

    validation = validate_agreement(
        agreement
    )

    
    # STEP 3: FIELD CONFIDENCE
   

    confidence_scores = []

    fields = {

        "landlord":
            agreement.landlord,

        "tenant":
            agreement.tenant,

        "property_address":
            agreement.property.address,

        "city":
            agreement.property.city,

        "state":
            agreement.property.state,

        "pincode":
            agreement.property.pincode,

        "agreement_date":
            agreement.period.agreement_date,

        "commencement_date":
            agreement.period.commencement_date,

        "end_date":
            agreement.period.end_date,

        "duration":
            agreement.period.duration,

        "monthly_rent":
            agreement.financial.monthly_rent,

        "security_deposit":
            agreement.financial.security_deposit,

        "advance_payment":
            agreement.financial.advance_payment,

        "maintenance_fee":
            agreement.financial.maintenance_fee,

        "notice_period":
            agreement.terms.notice_period
    }

    field_confidence = {}

    for field, value in fields.items():

        if value is None:

            score = 0.0

        else:

            score = confidence_for_value(
                value,
                "high"
            )

        field_confidence[field] = score

        if score > 0:

            confidence_scores.append(
                score
            )

    
    # STEP 4: OVERALL CONFIDENCE
   
    overall_confidence = (
        calculate_overall_confidence(
            confidence_scores
        )
    )

    
    # STEP 5: FINAL RESULT
    

    return {
        "agreement":
            agreement,

        "field_confidence":
            field_confidence,

        "overall_confidence":
            overall_confidence,

        "validation":
            validation
    }