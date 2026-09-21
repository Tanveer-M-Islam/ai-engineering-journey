from typing import List

import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor


class CLIPEngine:

    def __init__(
        self,
        model_name: str = "openai/clip-vit-base-patch32",
    ):
        self.device = "cpu"

        print("Loading CLIP model...")
        print(f"Model: {model_name}")
        print(f"Device: {self.device}")

        self.processor = CLIPProcessor.from_pretrained(model_name)

        self.model = CLIPModel.from_pretrained(model_name)

        self.model.to(self.device)
        self.model.eval()

        print("CLIP model loaded successfully.")

    def compare_image_with_text(
        self,
        image_path: str,
        texts: List[str],
    ) -> dict:

        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(
            text=texts,
            images=image,
            return_tensors="pt",
            padding=True,
        )

        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        with torch.no_grad():

            outputs = self.model(**inputs)

            logits_per_image = outputs.logits_per_image

            probabilities = logits_per_image.softmax(dim=1)

        scores = probabilities[0].tolist()

        results = []

        for text, score in zip(texts, scores):
            results.append(
                {
                    "text": text,
                    "score": round(float(score), 4),
                }
            )

        results.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return {
            "image": image_path,
            "results": results,
            "best_match": results[0],
        }