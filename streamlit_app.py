import json

import requests
import streamlit as st



# CONFIGURATION


API_URL = "http://127.0.0.1:8000"

# CHECK 

def format_amount(value):
    if value is None:
        return "Not available"

    try:
        return f"₹{float(value):,.2f}"
    except (ValueError, TypeError):
        return str(value)



# PAGE CONFIGURATION

st.set_page_config(
    page_title="Rental Agreement Parser",
    page_icon="📄",
    layout="wide"
)


# HEADER


st.title("📄 Rental Agreement Parser")

st.write(
    """
    Upload an Indian rental agreement and extract
    structured information using OCR and
    rule-based document extraction.
    """
)


st.divider()


# FILE UPLOAD

uploaded_file = st.file_uploader(
    "Upload Rental Agreement",
    type=[
        "pdf",
        "png",
        "jpg",
        "jpeg"
    ]
)


# PARSE BUTTON


if uploaded_file is not None:

    st.write(
        f"Selected file: **{uploaded_file.name}**"
    )

    if st.button(
        "🔍 Parse Agreement",
        type="primary"
    ):

        with st.spinner(
            "Processing document..."
        ):

            try:

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                response = requests.post(
                    f"{API_URL}/parse",
                    files=files,
                    timeout=120
                )

                
                # API error
                

                if response.status_code != 200:

                    st.error(
                        f"API Error: {response.text}"
                    )

                    st.stop()

                result = response.json()

            except requests.exceptions.ConnectionError:

                st.error(
                    """
                    Could not connect to the FastAPI server.

                    Make sure FastAPI is running:

                    `uvicorn app.main:app --reload`
                    """
                )

                st.stop()

            except requests.exceptions.Timeout:

                st.error(
                    "The document took too long to process."
                )

                st.stop()

            except Exception as error:

                st.error(
                    f"Unexpected error: {error}"
                )

                st.stop()

        
        # RESULTS
       

        extraction = result[
            "extraction"
        ]

        agreement = extraction[
            "agreement"
        ]

        confidence = extraction[
            "overall_confidence"
        ]

        validation = extraction[
            "validation"
        ]

        
        # OVERALL STATUS
        

        st.subheader(
            "Extraction Summary"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Overall Confidence",
                f"{confidence:.2f}"
            )

        with col2:

            if validation["valid"]:

                st.success(
                    "Validation Passed"
                )

            else:

                st.error(
                    "Validation Failed"
                )

        with col3:

            st.metric(
                "OCR Confidence",
                f"{result['ocr']['confidence']:.2f}"
            )

        st.divider()

        
        # PARTIES
        

        st.subheader(
            "👥 Parties"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                "**Landlord**"
            )

            landlord = agreement.get(
                "landlord"
            )

            if landlord:

                st.write(
                    landlord["name"]
                )

            else:

                st.warning(
                    "Landlord not identified"
                )

        with col2:

            st.markdown(
                "**Tenant**"
            )

            tenant = agreement.get(
                "tenant"
            )

            if tenant:

                st.write(
                    tenant["name"]
                )

            else:

                st.warning(
                    "Tenant not identified"
                )

        
        # PROPERTY
        

        st.divider()

        st.subheader(
            "🏠 Property"
        )

        property_data = agreement[
            "property"
        ]

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                "**Address**"
            )

            st.write(
                property_data.get(
                    "address"
                ) or "Not found"
            )

            st.markdown(
                "**City**"
            )

            st.write(
                property_data.get(
                    "city"
                ) or "Not found"
            )

        with col2:

            st.markdown(
                "**State**"
            )

            st.write(
                property_data.get(
                    "state"
                ) or "Not found"
            )

            st.markdown(
                "**PIN Code**"
            )

            st.write(
                property_data.get(
                    "pincode"
                ) or "Not found"
            )

        
        # FINANCIAL DETAILS
        

        st.divider()

        st.subheader(
            "💰 Financial Details"
        )

        financial = agreement[
            "financial"
        ]

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Monthly Rent",
                format_amount(
                    financial.get(
                        "monthly_rent"
                    )
                )
            )

        with col2:

            st.metric(
                "Security Deposit",
                format_amount(
                    financial.get(
                        "security_deposit"
                    )
                )
            )

        with col3:

            st.metric(
                "Advance Payment",
                format_amount(
                    financial.get(
                        "advance_payment"
                    )
                )
            )

        with col4:

            st.metric(
                "Maintenance",
                format_amount(
                    financial.get(
                        "maintenance_fee"
                    )
                )
            )

        
        # AGREEMENT PERIOD
        

        st.divider()

        st.subheader(
            "📅 Agreement Period"
        )

        period = agreement[
            "period"
        ]

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.markdown(
                "**Agreement Date**"
            )

            st.write(
                period.get(
                    "agreement_date"
                ) or "Not found"
            )

        with col2:

            st.markdown(
                "**Commencement Date**"
            )

            st.write(
                period.get(
                    "commencement_date"
                ) or "Not found"
            )

        with col3:

            st.markdown(
                "**End Date**"
            )

            st.write(
                period.get(
                    "end_date"
                ) or "Not explicitly stated"
            )

        with col4:

            st.markdown(
                "**Duration**"
            )

            st.write(
                period.get(
                    "duration"
                ) or "Not found"
            )

        
        # TERMS
        

        st.divider()

        st.subheader(
            "📋 Agreement Terms"
        )

        terms = agreement[
            "terms"
        ]

        st.markdown(
            "**Notice Period**"
        )

        st.write(
            terms.get(
                "notice_period"
            ) or "Not found"
        )

        if terms.get(
            "renewal_terms"
        ):

            st.markdown(
                "**Renewal Terms**"
            )

            st.write(
                terms[
                    "renewal_terms"
                ]
            )

        if terms.get(
            "termination_terms"
        ):

            st.markdown(
                "**Termination Terms**"
            )

            st.write(
                terms[
                    "termination_terms"
                ]
            )

        
        # CONFIDENCE DETAILS
        

        st.divider()

        with st.expander(
            "🔎 Field Confidence"
        ):

            field_confidence = (
                extraction[
                    "field_confidence"
                ]
            )

            for field, score in (
                field_confidence.items()
            ):

                st.write(
                    f"**{field}**: {score:.2f}"
                )

                st.progress(
                    score
                )

        
        # VALIDATION DETAILS
        

        with st.expander(
            "✅ Validation Details"
        ):

            if validation[
                "errors"
            ]:

                st.error(
                    "Errors"
                )

                for error in validation[
                    "errors"
                ]:

                    st.write(
                        f"- {error}"
                    )

            else:

                st.success(
                    "No validation errors."
                )

            if validation[
                "warnings"
            ]:

                st.warning(
                    "Warnings"
                )

                for warning in validation[
                    "warnings"
                ]:

                    st.write(
                        f"- {warning}"
                    )

        
        # OCR TEXT
        

        with st.expander(
            "📜 OCR Text"
        ):

            st.text(
                result[
                    "ocr"
                ][
                    "text"
                ]
            )

        
        # JSON DOWNLOAD
        

        st.divider()

        st.subheader(
            "📥 Export"
        )

        json_data = json.dumps(
            result,
            indent=4
        )

        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name="rental_agreement_result.json",
            mime="application/json"
        )



# HELPER FUNCTIONS


def format_amount(
    amount
):

    if amount is None:

        return "Not found"

    return f"₹{amount:,.2f}"