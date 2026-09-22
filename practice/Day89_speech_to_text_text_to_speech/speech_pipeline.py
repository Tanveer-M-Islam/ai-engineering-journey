import os

import numpy as np
import pyttsx3
import soundfile as sf
import torch

from transformers import (
    AutoModelForSpeechSeq2Seq,
    AutoProcessor,
    pipeline,
)


class SpeechPipeline:

    def __init__(self, model_name="openai/whisper-tiny"):

        self.device = "cpu"
        self.torch_dtype = torch.float32

        print("Loading Whisper model...")
        print(f"Model: {model_name}")
        print(f"Device: {self.device}")

        # ------------------------------------------------
        # Load Whisper processor
        # ------------------------------------------------

        self.processor = AutoProcessor.from_pretrained(
            model_name
        )

        # ------------------------------------------------
        # Load Whisper model
        # ------------------------------------------------

        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_name,
            torch_dtype=self.torch_dtype,
        )

        self.model.to(self.device)
        self.model.eval()

        # ------------------------------------------------
        # Create ASR pipeline
        # ------------------------------------------------

        self.asr = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            torch_dtype=self.torch_dtype,
            device=-1,
        )

        # ------------------------------------------------
        # Initialize TTS
        # ------------------------------------------------

        self.tts_engine = pyttsx3.init()

        print("Whisper loaded successfully.")
        print("TTS engine initialized.")
        print("Speech pipeline ready.")

    # ====================================================
    # SPEECH TO TEXT
    # ====================================================

    def transcribe(self, audio_path: str) -> str:

        if not os.path.exists(audio_path):
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        print(f"Loading audio: {audio_path}")

        # ------------------------------------------------
        # Load WAV directly using soundfile
        # This avoids FFmpeg
        # ------------------------------------------------

        audio, sampling_rate = sf.read(audio_path)

        print(f"Original sampling rate: {sampling_rate}")
        print(f"Audio shape: {audio.shape}")

        # ------------------------------------------------
        # Convert stereo -> mono
        # ------------------------------------------------

        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)

        # ------------------------------------------------
        # Convert to float32
        # ------------------------------------------------

        audio = audio.astype(np.float32)

        # ------------------------------------------------
        # Whisper normally works with 16 kHz audio
        # ------------------------------------------------

        if sampling_rate != 16000:

            print(
                "Warning: audio is not 16 kHz. "
                "Please use a 16 kHz WAV file for best results."
            )

        # ------------------------------------------------
        # Give raw audio array to Whisper
        # Instead of giving filename
        # ------------------------------------------------

        result = self.asr(
            {
                "raw": audio,
                "sampling_rate": sampling_rate,
            }
        )

        transcript = result["text"].strip()

        print(f"Transcript: {transcript}")

        return transcript

    # ====================================================
    # AI RESPONSE
    # ====================================================

    def generate_response(self, text: str) -> str:

        text_lower = text.lower()

        if "hello" in text_lower or "hi" in text_lower:

            return "Hello! How can I help you?"

        if "time" in text_lower:

            return (
                "I received a request about the time. "
                "A production assistant would call a time "
                "tool here."
            )

        if "what is ai" in text_lower:

            return (
                "Artificial intelligence is the field of "
                "building systems that can perform tasks "
                "that normally require human intelligence."
            )

        return (
            f"I heard you say: {text}. "
            "This response layer can later be replaced "
            "with an LLM or AI agent."
        )

    # ====================================================
    # TEXT TO SPEECH
    # ====================================================

    def text_to_speech(
        self,
        text: str,
        output_path: str,
    ):

        print(f"Generating speech: {text}")

        self.tts_engine.save_to_file(
            text,
            output_path,
        )

        self.tts_engine.runAndWait()

        print(f"TTS output saved: {output_path}")

        return output_path

    # ====================================================
    # COMPLETE VOICE PIPELINE
    # ====================================================

    def run(
        self,
        audio_path: str,
        output_path: str,
    ):

        # ------------------------------------------------
        # Step 1: Speech -> Text
        # ------------------------------------------------

        transcript = self.transcribe(
            audio_path
        )

        # ------------------------------------------------
        # Step 2: Generate response
        # ------------------------------------------------

        response = self.generate_response(
            transcript
        )

        # ------------------------------------------------
        # Step 3: Text -> Speech
        # ------------------------------------------------

        audio_output = self.text_to_speech(
            response,
            output_path,
        )

        return {
            "transcript": transcript,
            "response": response,
            "audio_output": audio_output,
        }