from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import os

app = FastAPI(title="Multilingual Summarizer")

API_KEY = os.getenv("API_KEY")  # Coolify secrets üzerinden ekle

# MT5 small pipeline
model_name = "google/mt5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

class NoteRequest(BaseModel):
    text: str

@app.post("/summarize")
def summarize(note: NoteRequest, x_api_key: str = Header(...)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    # MT5 multi-lingual özetleme
    summary = summarizer(note.text, max_length=150, min_length=30, do_sample=False)
    return {"summary": summary[0]['summary_text']}