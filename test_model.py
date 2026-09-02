from app.models.rental_agreement import (
    RentalAgreement,
    Person,
    PropertyDetails,
    FinancialDetails,
    AgreementPeriod,
    AgreementTerms
)


agreement = RentalAgreement(

    landlord=Person(
        name="Arun Kumar",
        role="landlord"
    ),

    tenant=Person(
        name="Priya Nair",
        role="tenant"
    ),

    property=PropertyDetails(
        address="14 MG Road",
        city="Ernakulam",
        state="Kerala",
        pincode="682016"
    ),

    financial=FinancialDetails(
        monthly_rent=25000,
        security_deposit=100000,
        advance_payment=25000,
        maintenance_fee=2000
    ),

    period=AgreementPeriod(
        agreement_date="2026-03-15",
        commencement_date="2026-04-01",
        end_date="2027-02-28",
        duration="11 months"
    ),

    terms=AgreementTerms(
        notice_period="2 months"
    )
)


print(agreement)