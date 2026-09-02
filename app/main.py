from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, UploadFile, HTTPException

from app.ocr.pdf_ocr import (
    extract_document_from_scanned_pdf
)

from app.extraction.extraction_service import (
    extract_agreement
)



# FASTAPI APPLICATION


app = FastAPI(
    title="Rental Agreement Parser API",
    description=(
        "OCR and rule-based information extraction "
        "for Indian rental agreements"
    ),
    version="1.0.0"
)



# ROOT


@app.get("/")
def root():

    return {
        "message": "Rental Agreement Parser API is running"
    }



# HEALTH CHECK


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }



# PARSE RENTAL AGREEMENT


@app.post("/parse")
async def parse_rental_agreement(
    file: UploadFile = File(...)
):


    # Validate file type


    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file provided"
        )

    extension = Path(
        file.filename
    ).suffix.lower()

    allowed_extensions = {
        ".pdf",
        ".png",
        ".jpg",
        ".jpeg"
    }

    if extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Use PDF, PNG, JPG or JPEG."
            )
        )


    # Save uploaded file temporarily


    temp_path = None

    try:

        with NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:

            content = await file.read()

            temp_file.write(
                content
            )

            temp_path = temp_file.name

        # PDF processing
      

        if extension == ".pdf":

            ocr_document = (
                extract_document_from_scanned_pdf(
                    temp_path
                )
            )

            # Combine OCR text from all pages.

            ocr_text = "\n".join(
                page.text
                for page in ocr_document.pages
            )

            # Average OCR confidence.

            page_confidences = [
                page.confidence
                for page in ocr_document.pages
            ]

            ocr_confidence = (
                sum(page_confidences)
                /
                len(page_confidences)
                if page_confidences
                else 0.0
            )

        # Image processing
        

        else:

            from app.ocr.tesseract_engine import (
                extract_text_with_confidence
            )

            result = (
                extract_text_with_confidence(
                    temp_path,
                    preprocess=True
                )
            )

            ocr_text = result["text"]

            ocr_confidence = (
                result["confidence"]
            )

   
        # Rule-based extraction
       

        extraction = extract_agreement(
            ocr_text
        )

        # Build API response
        

        return {

            "filename":
                file.filename,

            "ocr": {

                "confidence":
                    round(
                        ocr_confidence,
                        2
                    ),

                "text":
                    ocr_text
            },

            "extraction": {

                "agreement":
                    extraction[
                        "agreement"
                    ].model_dump(),

                "field_confidence":
                    extraction[
                        "field_confidence"
                    ],

                "overall_confidence":
                    extraction[
                        "overall_confidence"
                    ],

                "validation":
                    extraction[
                        "validation"
                    ]
            }
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:

        
        # Delete temporary uploaded file
       

        if temp_path:

            path = Path(
                temp_path
            )

            if path.exists():

                path.unlink()