import json

from app.llm.ollama_client import (
    generate_response
)

from app.llm.prompts import (
    SYSTEM_PROMPT,
    EXTRACTION_PROMPT
)


# def extract_with_llm(
#     document_text: str
# ) -> dict:
#     """
#     Extract rental agreement information
#     using Llama 3.2 1B.
#     """

#     prompt = EXTRACTION_PROMPT.format(
#         document_text=document_text
#     )

#     response = generate_response(
#         prompt,
#         SYSTEM_PROMPT
#     )

#     try:

#         return json.loads(
#             response
#         )

#     except json.JSONDecodeError as e:

#         raise ValueError(
#             "LLM did not return valid JSON."
#         ) from e


import json

from app.llm.ollama_client import generate_response
from app.llm.prompts import SYSTEM_PROMPT, EXTRACTION_PROMPT


def extract_with_llm(document_text: str):

    prompt = EXTRACTION_PROMPT.format(
        document_text=document_text
    )

    response = generate_response(
        prompt,
        SYSTEM_PROMPT
    )

    print("\n========== RAW LLM RESPONSE ==========")
    print(response)
    print("======================================\n")

    try:
        return json.loads(response)

    except json.JSONDecodeError as exc:
        raise ValueError(
            "LLM did not return valid JSON."
        ) from exc