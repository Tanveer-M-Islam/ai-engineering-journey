import os
import shutil
import uuid

from fastapi import FastAPI, File, HTTPException, UploadFile

from speech_pipeline import SpeechPipeline


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="Day 89 - Speech-to-Text and Text-to-Speech",
    version="1.0.0",
    description="Local STT -> AI Response -> TTS pipeline",
)


# ============================================================
# Directories
# ============================================================

AUDIO_DIR = "audio"
OUTPUT_DIR = "outputs"

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# Load Speech Pipeline
# ============================================================

print("Initializing Speech Pipeline...")

try:
    speech_pipeline = SpeechPipeline()

    print("Speech Pipeline initialized successfully.")

except Exception as e:

    print("ERROR: Could not initialize Speech Pipeline.")
    print(str(e))

    speech_pipeline = None


# ============================================================
# Health Check
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "ok",
        "project": "Day 89 - Speech-to-Text and Text-to-Speech",
        "stt_model": "openai/whisper-tiny",
        "device": "cpu",
        "tts": "pyttsx3",
        "pipeline_loaded": speech_pipeline is not None,
    }


# ============================================================
# STT Only
# ============================================================

@app.post("/transcribe")
async def transcribe(
    audio: UploadFile = File(...)
):

    if speech_pipeline is None:

        raise HTTPException(
            status_code=500,
            detail="Speech pipeline was not initialized."
        )

    if not audio.filename:

        raise HTTPException(
            status_code=400,
            detail="No audio filename was provided."
        )

    try:

        extension = os.path.splitext(
            audio.filename
        )[1].lower()

        if not extension:

            extension = ".wav"

        filename = (
            f"{uuid.uuid4()}{extension}"
        )

        input_path = os.path.join(
            AUDIO_DIR,
            filename
        )

        with open(
            input_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                audio.file,
                buffer
            )

        transcript = speech_pipeline.transcribe(
            input_path
        )

        return {
            "status": "success",
            "filename": audio.filename,
            "transcript": transcript,
        }

    except Exception as e:

        print("STT ERROR:")
        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Speech-to-text failed: {str(e)}"
        )


# ============================================================
# Complete Voice Pipeline
# ============================================================

@app.post("/voice")
async def voice(
    audio: UploadFile = File(...)
):

    if speech_pipeline is None:

        raise HTTPException(
            status_code=500,
            detail="Speech pipeline was not initialized."
        )

    if not audio.filename:

        raise HTTPException(
            status_code=400,
            detail="No audio filename was provided."
        )

    try:

        # ----------------------------------------------------
        # Save uploaded audio
        # ----------------------------------------------------

        extension = os.path.splitext(
            audio.filename
        )[1].lower()

        if not extension:

            extension = ".wav"

        input_filename = (
            f"{uuid.uuid4()}{extension}"
        )

        input_path = os.path.join(
            AUDIO_DIR,
            input_filename
        )

        with open(
            input_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                audio.file,
                buffer
            )

        # ----------------------------------------------------
        # Output audio path
        # ----------------------------------------------------

        output_filename = (
            f"{uuid.uuid4()}_response.wav"
        )

        output_path = os.path.join(
            OUTPUT_DIR,
            output_filename
        )

        # ----------------------------------------------------
        # Run complete pipeline
        # ----------------------------------------------------

        result = speech_pipeline.run(
            audio_path=input_path,
            output_path=output_path
        )

        return {
            "status": "success",
            "input_file": input_path,
            "transcript": result["transcript"],
            "response": result["response"],
            "audio_output": result["audio_output"],
        }

    except Exception as e:

        print("VOICE PIPELINE ERROR:")
        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Voice pipeline failed: {str(e)}"
        )