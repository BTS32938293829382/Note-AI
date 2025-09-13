from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# CPU-only özetleme pipeline
summarizer = pipeline("summarization", model="google/flan-t5-small")

class NoteRequest(BaseModel):
    text: str

@app.post("/summarize")
def summarize(note: NoteRequest):
    summary = summarizer(note.text, max_length=150, min_length=30, do_sample=False)
    return {"summary": summary[0]['summary_text']}