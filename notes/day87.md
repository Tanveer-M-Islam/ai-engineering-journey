# Day 87 — Vision-Language Models

## Core Concepts

Vision-Language Models connect visual information with language.

Main models studied:

- CLIP
- BLIP
- LLaVA-style architectures

---

## CLIP

CLIP = Contrastive Language-Image Pre-training.

CLIP contains:

- Image encoder
- Text encoder
- Shared embedding space

Image:

Image -> Image Encoder -> Image Embedding

Text:

Text -> Text Encoder -> Text Embedding

The embeddings can be compared using similarity.

---

## Contrastive Learning

The model learns to increase similarity between matching image-text pairs and decrease similarity between incorrect pairs.

Positive:

Image <-> Correct Text

Negative:

Image <-> Incorrect Text

---

## Zero-Shot Classification

CLIP can compare an image against candidate text descriptions.

Example:

Image

Candidate labels:

- a dog
- a cat
- a car
- a chair

The text with the highest similarity can be selected.

---

## BLIP

BLIP = Bootstrapping Language-Image Pre-training.

BLIP can support:

- image captioning
- visual question answering
- image-text matching
- vision-language generation

Simplified:

Image
-> Vision Encoder
-> Vision-Language Module
-> Language Generation

---

## LLaVA

LLaVA = Large Language and Vision Assistant.

Simplified architecture:

Image
-> Vision Encoder
-> Projector
-> LLM

Text prompt is also provided to the LLM.

The projector converts visual representations into a representation compatible with the language model.

---

## CLIP vs BLIP vs LLaVA

CLIP:
Image-text alignment and similarity.

BLIP:
Image understanding and language generation.

LLaVA:
Vision + projector + LLM for conversational multimodal reasoning.

---

## Embedding Space

Images and text can be represented as vectors.

Similar semantic concepts should have nearby representations.

This enables:

- semantic image search
- multimodal retrieval
- zero-shot classification
- image-text matching

---

## CLIP + Vector Database

Image:

Image -> CLIP Image Encoder -> Vector

Query:

Text -> CLIP Text Encoder -> Vector

Then perform vector similarity search.

This can create multimodal search systems.

---

## YOLO + VLM

YOLO:
Object detection.

CLIP:
Image-text semantic alignment.

VLM:
Visual understanding and language reasoning.

Possible architecture:

Camera
-> YOLO
-> Object Information
-> VLM/LLM
-> Scene Understanding
-> TTS

---

## Important Limitations

CLIP similarity is not guaranteed truth.

A similarity score should not automatically be interpreted as a real-world probability.

Safety-critical systems require additional validation and deterministic logic.

---

## Day 87 Practical Project

Built:

CLIP Image-Text Matching API

Input:

- image
- candidate text descriptions

Output:

- similarity scores
- best matching description

Technology:

- Python
- PyTorch
- Transformers
- CLIP
- FastAPI
- Pillow