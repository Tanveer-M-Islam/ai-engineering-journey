# AI Text Summarizer API

A FastAPI-based AI-style summarization API.

## Features

* FastAPI backend
* Input validation
* Structured JSON response
* Health check endpoint

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Endpoints

### GET /

Health check

### POST /summarize

Input:

```json
{
  "text": "your text"
}
```
