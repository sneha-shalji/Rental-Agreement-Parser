# Rental Agreement Parser

An OCR-based document information extraction system for extracting structured information from Indian rental agreements.

## Features

- Scanned PDF and image processing
- Image preprocessing using OpenCV
- OCR using Tesseract
- Rule-based and context-aware information extraction
- Extracts landlord and tenant details
- Extracts property address and PIN code
- Extracts rent, deposit, advance and maintenance
- Extracts agreement dates and duration
- Extracts notice and other agreement terms
- Pydantic validation
- Confidence scoring
- FastAPI REST API
- Streamlit web interface
- Field-level evaluation using test documents

## Architecture

```text
PDF / Image
    ↓
OpenCV Preprocessing
    ↓
Tesseract OCR
    ↓
Text Cleaning
    ↓
Rule-Based Extraction
    ↓
Pydantic Validation
    ↓
Confidence Scoring
    ↓
Structured JSON
    ↓
FastAPI + Streamlit
