# Day 90 — Multimodal AI Application

A practical multimodal AI application combining speech,
vision and text-to-speech.

## Features

- Speech-to-text with Whisper
- Image understanding with LLaVA
- Text-to-speech with pyttsx3
- Local inference through Ollama
- Modular Python architecture

## Architecture

```text
Audio
  ↓
Whisper
  ↓
Text Question
  ↓
Image + Question
  ↓
LLaVA
  ↓
Text Answer
  ↓
pyttsx3
  ↓
Audio Response