from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class TextRequest(BaseModel):
    text: str


@app.post("/summarize")
def summarize(data: TextRequest):

    summary = data.text[:50]

    return {
        "summary": summary
    }

@app.post("/summarizes")
def summarize(data: TextRequest):

    words = data.text.split()

    summary = " ".join(words[:10])

    return {
        "summary": summary
    }

@app.post("/summarizing")
def summarize(data: TextRequest):

    words = data.text.split()

    summary = " ".join(words[:10])

    return {
        "summary": summary,
        "original_word_count": len(words),
        "summary_word_count": len(summary.split())
    }

@app.post("/translate")
def translate(data: TextRequest):

    translation = data.text.upper()

    return {
        "translation": translation
    }