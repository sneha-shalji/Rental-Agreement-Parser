from typing import Any,List


HIGH_CONFIDENCE = 0.99
MEDIUM_CONFIDENCE = 0.90
LOW_CONFIDENCE = 0.75


def confidence_for_value(
    value: Any,
    level: str = "medium"
) -> float:

    if value is None:

        return 0.0

    if level == "high":

        return HIGH_CONFIDENCE

    if level == "low":

        return LOW_CONFIDENCE

    return MEDIUM_CONFIDENCE


def calculate_overall_confidence(
    confidences: List[float]
) -> float:

    valid_scores = [
        score
        for score in confidences
        if score > 0
    ]

    if not valid_scores:

        return 0.0

    return round(
        sum(valid_scores)
        /
        len(valid_scores),
        2
    )