# Day 88 — Image Understanding with LLMs

## 1. What is Image Understanding?

Image understanding is the ability of an AI model to interpret
visual information and answer questions about an image.

Basic pipeline:

Image + Text
    ↓
Vision Encoder
    ↓
Visual Embeddings
    ↓
Multimodal Projector
    ↓
LLM
    ↓
Text Response

---

## 2. Vision-Language Model

A Vision-Language Model (VLM) can process both visual and
language information.

Input:

- Image
- Text prompt

Output:

- Text response

Examples:

- LLaVA
- BLIP-2
- CLIP-based systems
- GPT-4o-class multimodal models
- Gemini multimodal models

---

## 3. Vision Encoder

The vision encoder converts an image into numerical
representations called visual features or embeddings.

Many modern vision encoders use architectures related to
Vision Transformers.

---

## 4. Multimodal Projector

The projector maps visual representations into a representation
space that can be processed by the language model.

Simplified:

Vision Encoder
    ↓
Visual Embeddings
    ↓
Projector
    ↓
LLM

---

## 5. Image Captioning

Image captioning generates a textual description of an image.

Example:

Image → "A person is sitting at a desk."

---

## 6. Visual Question Answering

VQA combines an image with a question.

Example:

Image + "What is on the table?"
        ↓
" A laptop is on the table."

---

## 7. Image Understanding Tasks

Common tasks:

- Image captioning
- Visual question answering
- Object identification
- Scene understanding
- OCR-style understanding
- Visual reasoning
- Image comparison
- Safety analysis

---

## 8. Multimodal Prompting

The prompt is important.

Weak:

"Describe."

Better:

"Describe the important objects visible in this image."

Controlled:

"Identify clearly visible objects. Do not guess objects
that are not clearly visible."

---

## 9. Ollama Vision API

The Ollama generate endpoint can receive images.

Important fields:

- model
- prompt
- images
- stream

Example:

```python
payload = {
    "model": "llava",
    "prompt": "Describe this image.",
    "images": [image_base64],
    "stream": False
}