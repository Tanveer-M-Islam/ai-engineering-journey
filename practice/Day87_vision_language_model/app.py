import os
import shutil
import uuid
from typing import List

from fastapi import FastAPI, File, Form, UploadFile

from clip_engine import CLIPEngine


app = FastAPI(
    title="Day 87 - Vision-Language Models",
    version="1.0.0",
)


clip_engine = CLIPEngine()


UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "project": "Day 87 - Vision-Language Models",
        "model": "openai/clip-vit-base-patch32",
        "device": "cpu",
    }


@app.post("/compare")
async def compare_image_text(
    image: UploadFile = File(...),
    texts: List[str] = Form(...),
):

    extension = os.path.splitext(image.filename)[1]

    filename = f"{uuid.uuid4()}{extension}"

    image_path = os.path.join(
        UPLOAD_DIR,
        filename,
    )

    with open(image_path, "wb") as buffer:

        shutil.copyfileobj(
            image.file,
            buffer,
        )

    result = clip_engine.compare_image_with_text(
        image_path=image_path,
        texts=texts,
    )

    return result