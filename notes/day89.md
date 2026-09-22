# Day 89 — Speech-to-Text & Text-to-Speech

## Core Architecture

Audio
-> Speech-to-Text
-> Text
-> LLM / Agent
-> Response Text
-> Text-to-Speech
-> Audio

---

## Speech-to-Text

Speech-to-Text converts spoken audio into text.

Another common term is ASR:

Automatic Speech Recognition.

---

## Text-to-Speech

Text-to-Speech converts text into spoken audio.

TTS is used in:

- AI assistants
- accessibility
- navigation
- customer service
- voice agents

---

## Audio

Audio is represented digitally as numerical samples.

Important concepts:

- sampling rate
- channels
- waveform
- frequency
- spectrogram

---

## Sampling Rate

Sampling rate is the number of samples captured per second.

Example:

16 kHz = 16,000 samples per second.

---

## Spectrogram

A spectrogram represents frequency information over time.

Speech recognition models can use spectrogram-based representations to process speech.

---

## Whisper

Whisper is an automatic speech recognition model.

Simplified architecture:

Audio
-> Log-Mel Spectrogram
-> Encoder
-> Decoder
-> Text

Model sizes include:

- tiny
- base
- small
- medium
- large

Smaller models require less computation.

---

## TTS

Simplified neural TTS pipeline:

Text
-> Acoustic Model
-> Mel Spectrogram
-> Vocoder
-> Audio Waveform

Different modern TTS architectures may use different implementations.

---

## VAD

VAD = Voice Activity Detection.

It identifies speech segments and silence.

Pipeline:

Audio
-> VAD
-> Speech segments
-> STT

---

## Voice AI Latency

Voice AI contains multiple latency sources:

STT latency
+
LLM latency
+
TTS latency

Streaming can reduce perceived latency.

---

## Streaming

Non-streaming:

Audio
-> Complete STT
-> Complete LLM response
-> Complete TTS
-> Audio

Streaming:

Audio
-> Partial STT
-> Streaming LLM
-> TTS chunks
-> Audio

---

## Today's Project

Built a local:

Audio
-> Whisper STT
-> Response Layer
-> pyttsx3 TTS
-> WAV

pipeline.

---

## Production Architecture

Microphone
-> Audio Processing
-> VAD
-> STT
-> LLM / Agent
-> Tools / RAG / Memory
-> TTS
-> Speaker

---

## Assistive AI Application

Camera
-> YOLO
-> Scene Information
-> VLM
-> Agent

User Voice
-> STT
-> Agent

Agent
-> Safety Rules
-> TTS

This creates a multimodal voice-enabled assistive system.

---

## Important Engineering Principle

STT, LLM, and TTS are separate components.

Whisper handles speech recognition.

An LLM handles language reasoning/generation.

A TTS engine converts text into audio.

Do not treat a speech model as a complete voice agent.

---

## Safety

For safety-critical applications:

- use deterministic detection where possible
- validate important decisions
- do not rely only on LLM reasoning
- keep confidence thresholds
- log model decisions
- provide safe fallback behavior