from fastapi import FastAPI
from app.models import TextRequest
from app.services import generate_summary
from app.services import translate_to_uppercase

app = FastAPI(
    title="AI Text Summarizer API"
)


@app.get("/")
def health():

    return {
        "status": "running"
    }


@app.post("/summarize")
def summarize(data: TextRequest):

    result = generate_summary(data.text)

    return result

@app.post("/translate")
def translate(data: TextRequest):
    result = translate_to_uppercase(data.text)
    return result