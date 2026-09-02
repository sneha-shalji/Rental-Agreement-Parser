from typing import Any, Optional,List
from pydantic import BaseModel

class FieldConfidence(BaseModel):

    value: Any

    confidence: float

    source: Optional[str] = None


class ExtractionMetadata(BaseModel):

    overall_confidence: float

    validation_passed: bool

    errors: List[str] = []

    warnings: List[str] = []