from typing import Optional


def process_multimodal_input(
    text: Optional[str] = None,
    image_description: Optional[str] = None,
    audio_transcript: Optional[str] = None,
) -> dict:

    modalities = []

    if text:
        modalities.append("text")

    if image_description:
        modalities.append("image")

    if audio_transcript:
        modalities.append("audio")

    if not modalities:
        return {
            "error": "At least one modality is required."
        }

    context_parts = []

    if text:
        context_parts.append(
            f"Text input: {text}"
        )

    if image_description:
        context_parts.append(
            f"Visual information: {image_description}"
        )

    if audio_transcript:
        context_parts.append(
            f"Audio transcript: {audio_transcript}"
        )

    combined_context = "\n".join(context_parts)

    response = (
        "Multimodal pipeline received the following information:\n\n"
        f"{combined_context}\n\n"
        f"Detected modalities: {', '.join(modalities)}"
    )

    return {
        "modalities": modalities,
        "combined_context": combined_context,
        "response": response,
    }