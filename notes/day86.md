# Day 86 — Multimodal LLM Fundamentals

## What is Multimodal AI?

Multimodal AI processes more than one type of information.

Common modalities:

- Text
- Image
- Audio
- Video
- Sensor data

## Unimodal

Example:

Text → LLM → Text

## Multimodal

Example:

Text + Image → Multimodal Model → Text

## Vision-Language Model

A Vision-Language Model combines visual understanding with language
understanding.

Example:

Image + Question → Answer

## Basic VLM Architecture

Image
↓
Vision Encoder
↓
Visual Features
↓
Adapter / Projection
↓
Language Model
↑
Text Prompt

## Image Encoder

An image encoder converts image information into learned numerical
representations.

Image
↓
Vision Encoder
↓
Visual Embeddings

## Embeddings

Embeddings are numerical representations of information.

Different modalities can be represented in learned vector spaces.

## Cross-Modal Alignment

The model learns relationships between different modalities.

Example:

Image of a dog
+
Text "dog"

The representations should be semantically related.

## Architecture Patterns

### Early Fusion

Different modalities are combined early.

### Late Fusion

Different modalities are processed separately and combined later.

### Cross-Attention / Adapter Fusion

Visual representations interact with a language model through
attention or intermediate projection mechanisms.

## YOLO vs VLM

YOLO:

- Object detection
- Bounding boxes
- Confidence scores
- Real-time detection

VLM:

- Image understanding
- Visual question answering
- Image description
- Visual reasoning

They can be combined.

## Multimodal Pipeline

Camera
↓
Vision Model
↓
Structured Scene
↓
Multimodal Model
↓
Decision
↓
TTS

## Multimodal RAG

Traditional RAG:

Question
↓
Text Retriever
↓
Documents
↓
LLM

Multimodal RAG:

Question + Image
↓
Multimodal Retrieval
↓
Text + Image Information
↓
Multimodal Model
↓
Answer

## Audio Pipeline

Microphone
↓
Speech Recognition
↓
LLM
↓
Text-to-Speech
↓
Speaker

## Important Engineering Consideration

Multimodal systems may increase:

- Latency
- Memory usage
- Compute requirements
- Complexity
- Cost

Therefore, use multimodality only when it adds meaningful value.

## Day 86 Key Lesson

A multimodal LLM is not simply a text LLM with an image attached.

The system needs mechanisms to convert different modalities into
representations that can interact with the model.