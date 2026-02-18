from fastapi import FastAPI, UploadFile, File, HTTPException
import whisper
import shutil
import os
import subprocess
import uuid

app = FastAPI()

model = whisper.load_model("tiny")

SUPPORTED_FORMATS = (".wav", ".mp3", ".m4a", ".mp4")


@app.get("/")
def home():
    return {"message": "Transcription is running"}


@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(SUPPORTED_FORMATS):
        raise HTTPException(status_code=400, detail="Unsupported file format")

    upload_path = f"uploaded_{file.filename}"

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "message": "File uploaded successfully"
    }


@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(SUPPORTED_FORMATS):
        raise HTTPException(status_code=400, detail="Unsupported file format")

    unique_id = str(uuid.uuid4())
    temp_input = f"temp_{unique_id}"
    normalized_file = f"normalized_{unique_id}.wav"

    with open(temp_input, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Convert to mono 16kHz WAV
        subprocess.run([
            "ffmpeg",
            "-y",
            "-i", temp_input,
            "-ac", "1",
            "-ar", "16000",
            normalized_file
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        result = model.transcribe(normalized_file)

        segments = [
            {
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"].strip()
            }
            for seg in result["segments"]
        ]

        return {
            "full_text": result["text"],
            "segments": segments
        }

    finally:
        for f in [temp_input, normalized_file]:
            if os.path.exists(f):
                os.remove(f)
