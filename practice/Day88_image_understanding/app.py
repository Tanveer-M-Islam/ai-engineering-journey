import base64
import json
import os
import requests


# ============================================================
# CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llava"

IMAGE_PATH = "images/test.jpg"


# ============================================================
# IMAGE ENCODING
# ============================================================

def encode_image(image_path):
    """
    Read an image and convert it to Base64.
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    encoded_image = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    return encoded_image


# ============================================================
# SEND IMAGE TO OLLAMA
# ============================================================

def analyze_image(image_path, question):
    """
    Send an image and question to the Ollama vision model.
    """

    image_base64 = encode_image(image_path)

    payload = {
        "model": MODEL_NAME,
        "prompt": question,
        "images": [image_base64],
        "stream": False,
        "options": {
            "temperature": 0
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300
    )

    response.raise_for_status()

    result = response.json()

    return result.get("response", "")


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("DAY 88 - IMAGE UNDERSTANDING")
    print("=" * 60)

    question = input(
        "\nEnter your question about the image: "
    ).strip()

    if not question:
        question = (
            "Describe the important objects visible "
            "in this image. Do not guess objects that "
            "are not clearly visible."
        )

    print("\nAnalyzing image...")
    print("-" * 60)

    try:

        answer = analyze_image(
            IMAGE_PATH,
            question
        )

        print("\nModel Answer:")
        print(answer)

        print("\n" + "=" * 60)

    except requests.exceptions.ConnectionError:
        print(
            "\nERROR: Could not connect to Ollama."
        )
        print(
            "Make sure Ollama is running."
        )

    except FileNotFoundError as error:
        print(f"\nERROR: {error}")

    except requests.exceptions.RequestException as error:
        print(
            f"\nOllama API error: {error}"
        )

    except Exception as error:
        print(
            f"\nUnexpected error: {error}"
        )


if __name__ == "__main__":
    main()