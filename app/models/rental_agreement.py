from typing import Optional,List
from pydantic import (BaseModel,Field,field_validator)


class Person(BaseModel):
    """
    Represents a person involved in the agreement.
    """

    name: str
    role: Optional[str] = None


class PropertyDetails(BaseModel):
    """
    Details about the rental property.
    """

    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, value):

        if value is None:
            return value

        import re

        if not re.match(
            r"^[1-9][0-9]{5}$",
            value
        ):
            raise ValueError(
                "Invalid Indian PIN code"
            )

        return value


class FinancialDetails(BaseModel):
    """
    Financial terms of the rental agreement.
    """

    monthly_rent: Optional[float] = None
    security_deposit: Optional[float] = None
    advance_payment: Optional[float] = None
    maintenance_fee: Optional[float] = None
    other_charges: Optional[float] = None

    @field_validator(
        "monthly_rent",
        "security_deposit",
        "advance_payment",
        "maintenance_fee",
        "other_charges"
    )
    @classmethod
    def validate_amount(cls, value):

        if value is None:
            return value

        if value < 0:
            raise ValueError(
                "Financial amounts cannot be negative"
            )

        return value


class AgreementPeriod(BaseModel):
    """
    Agreement validity information.
    """

    agreement_date: Optional[str] = None
    commencement_date: Optional[str] = None
    end_date: Optional[str] = None
    duration: Optional[str] = None

    @field_validator(
        "agreement_date",
        "commencement_date",
        "end_date"
    )
    @classmethod
    def validate_date_format(cls, value):

        if value is None:
            return value

        import re

        if not re.match(
            r"^\d{4}-\d{2}-\d{2}$",
            value
        ):
            raise ValueError(
                "Date must use YYYY-MM-DD format"
            )

        return value
    duration: Optional[str] = None


class AgreementTerms(BaseModel):
    """
    Important contractual terms.
    """

    notice_period: Optional[str] = None
    renewal_terms: Optional[str] = None
    termination_terms: Optional[str] = None
    purpose: Optional[str] = None


class RentalAgreement(BaseModel):
    """
    Complete structured representation
    of a rental agreement.
    """

    landlord: Optional[Person] = None

    tenant: Optional[Person] = None

    other_parties: List[Person] = Field(
        default_factory=list
    )

    property: PropertyDetails = Field(
        default_factory=PropertyDetails
    )

    financial: FinancialDetails = Field(
        default_factory=FinancialDetails
    )

    period: AgreementPeriod = Field(
        default_factory=AgreementPeriod
    )

    terms: AgreementTerms = Field(
        default_factory=AgreementTerms
    )