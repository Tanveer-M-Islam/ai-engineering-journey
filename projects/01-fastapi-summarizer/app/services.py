def generate_summary(text: str):

    if not text.strip():

        raise ValueError(
            "Text cannot be empty"
        )

    words = text.split()

    summary = " ".join(
        words[:10]
    )

    return {
        "summary": summary,
        "original_word_count": len(words),
        "summary_word_count": len(summary.split())
    }

def translate_to_uppercase(text: str):

    if not text.strip():

        raise ValueError(
            "Text cannot be empty"
        )

    return text.upper()