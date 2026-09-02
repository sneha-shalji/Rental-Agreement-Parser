import ollama


MODEL_NAME = "llama3.2:1b"


def generate_response(
    prompt: str,
    system_prompt: str = None
) -> str:
    """
    Send a prompt to the local Ollama model.
    """

    messages = []

    if system_prompt:
        messages.append(
            {
                "role": "system",
                "content": system_prompt
            }
        )

    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    response = ollama.chat(
        model=MODEL_NAME,
        messages=messages
    )

    return response.message.content