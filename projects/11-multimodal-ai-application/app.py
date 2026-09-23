import base64
import os
import requests
import whisper
import pyttsx3


# ============================================================
# CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
VISION_MODEL = "llava"

IMAGE_PATH = "images/test.jpg"
AUDIO_INPUT_PATH = "input.wav"
AUDIO_OUTPUT_PATH = "outputs/response.wav"


# ============================================================
# SPEECH-TO-TEXT
# ============================================================

def speech_to_text(audio_path):
    """
    Convert speech audio into text using Whisper.
    """

    if not os.path.exists(audio_path):
        raise FileNotFoundError(
            f"Audio file not found: {audio_path}"
        )

    print("\nLoading Whisper model...")

    model = whisper.load_model("base")

    print("Transcribing audio...")

    result = model.transcribe(audio_path)

    text = result.get("text", "").strip()

    return text


# ============================================================
# IMAGE ENCODING
# ============================================================

def encode_image(image_path):
    """
    Convert image bytes to Base64.
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"Image file not found: {image_path}"
        )

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    return base64.b64encode(
        image_bytes
    ).decode("utf-8")


# ============================================================
# VISION LLM
# ============================================================

def analyze_image(image_path, question):
    """
    Send image + question to the Ollama vision model.
    """

    image_base64 = encode_image(image_path)

    payload = {
        "model": VISION_MODEL,
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

    data = response.json()

    return data.get("response", "").strip()


# ============================================================
# TEXT-TO-SPEECH
# ============================================================

def text_to_speech(text, output_path):
    """
    Convert generated text into speech.
    """

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    print("\nGenerating audio response...")

    engine = pyttsx3.init()

    engine.setProperty(
        "rate",
        160
    )

    engine.save_to_file(
        text,
        output_path
    )

    engine.runAndWait()

    engine.stop()

    return output_path


# ============================================================
# MULTIMODAL PIPELINE
# ============================================================

def process_multimodal_request(
    image_path,
    audio_path
):
    """
    Complete multimodal pipeline:

    Audio
       ↓
    Whisper
       ↓
    Question
       ↓
    Image + Question
       ↓
    LLaVA
       ↓
    Answer
       ↓
    TTS
       ↓
    Audio
    """

    # --------------------------------------------------------
    # STEP 1: Speech-to-Text
    # --------------------------------------------------------

    question = speech_to_text(
        audio_path
    )

    if not question:

        question = (
            "Describe the important objects "
            "visible in this image. "
            "Do not guess objects that are "
            "not clearly visible."
        )

    print("\nUser Question:")
    print(question)

    # --------------------------------------------------------
    # STEP 2: Vision LLM
    # --------------------------------------------------------

    print("\nAnalyzing image with LLaVA...")

    answer = analyze_image(
        image_path,
        question
    )

    print("\nAI Answer:")
    print(answer)

    # --------------------------------------------------------
    # STEP 3: Text-to-Speech
    # --------------------------------------------------------

    output_audio = text_to_speech(
        answer,
        AUDIO_OUTPUT_PATH
    )

    print(
        f"\nAudio saved to: {output_audio}"
    )

    return {
        "question": question,
        "answer": answer,
        "audio_output": output_audio
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 65)
    print("DAY 90 - MULTIMODAL AI APPLICATION")
    print("=" * 65)

    try:

        result = process_multimodal_request(
            IMAGE_PATH,
            AUDIO_INPUT_PATH
        )

        print("\n" + "=" * 65)
        print("MULTIMODAL PIPELINE COMPLETED")
        print("=" * 65)

        print("\nQuestion:")
        print(result["question"])

        print("\nAnswer:")
        print(result["answer"])

        print("\nAudio:")
        print(result["audio_output"])

    except FileNotFoundError as error:

        print(
            f"\nFILE ERROR:\n{error}"
        )

    except requests.exceptions.ConnectionError:

        print(
            "\nERROR: Could not connect to Ollama."
        )

        print(
            "Make sure Ollama is running."
        )

    except requests.exceptions.RequestException as error:

        print(
            f"\nOLLAMA API ERROR:\n{error}"
        )

    except Exception as error:

        print(
            f"\nUNEXPECTED ERROR:\n{error}"
        )


if __name__ == "__main__":
    main()