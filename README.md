Audio Transcription Service

Built with FastAPI + OpenAI Whisper

1. Overview

This project implements a RESTful API for audio transcription using FastAPI and OpenAI Whisper.

The service allows users to upload audio files and receive:

Full transcription text

Timestamped transcription segments

The focus of the design was simplicity, correctness, and clean separation of responsibilities, while keeping scalability in mind.

2. High-Level Architecture

Client → FastAPI API → Audio Normalization (FFmpeg) → Whisper Model → JSON Response

The system processes uploaded audio files, normalizes them to a standard format, transcribes them using Whisper, and returns structured results.

3. Key Design Decisions
3.1 Model Loading Strategy

The Whisper model is loaded once at application startup:

model = whisper.load_model("tiny")


Reasoning:

Avoids loading the model per request

Reduces latency

Improves performance

For production:

Larger model variants could be used

GPU acceleration could be enabled

Model could run in a dedicated inference service

3.2 Audio Normalization

Before transcription, audio is converted to:

Mono channel (-ac 1)

16kHz sample rate (-ar 16000)

WAV format

This ensures:

Consistent input to the Whisper model

Improved transcription stability

Compatibility across multiple input formats

FFmpeg is used for reliability and format flexibility.

3.3 Temporary File Handling

Uploaded files are stored temporarily and cleaned up in a finally block:

Prevents disk space leaks

Ensures cleanup even if errors occur

Improves system reliability

Unique filenames are generated using UUID to avoid collisions in concurrent requests.

3.4 Supported Formats

The system currently supports:

.wav

.mp3

.m4a

.mp4

This is validated before processing to prevent unsupported inputs.

3.5 API Design

Endpoints:

GET / – Health check

POST /upload – Upload audio file

POST /transcribe – Upload and transcribe audio

The /transcribe endpoint returns:

Full transcript text

Structured timestamp segments

The API is RESTful and leverages FastAPI’s automatic OpenAPI documentation.

4. Error Handling

The system includes:

File format validation

HTTP 400 responses for invalid inputs

Guaranteed file cleanup

Structured JSON responses

For production systems, logging and monitoring would be added.

5. Scalability Considerations (Future Improvements)

Although the current implementation processes requests synchronously, the system can be scaled by:

5.1 Background Processing

Move transcription to a task queue such as:

Celery + Redis

RabbitMQ

AWS SQS

The API would:

Accept upload

Return a job ID

Process transcription asynchronously

This prevents request blocking and improves responsiveness.

5.2 Horizontal Scaling

Run multiple FastAPI workers (Gunicorn/Uvicorn)

Deploy behind a load balancer

Use containerization (Docker + Kubernetes)

5.3 Storage Strategy

In production:

Store audio files in object storage (e.g., AWS S3)

Store metadata and transcripts in PostgreSQL

Use database indexing for efficient retrieval

5.4 Security Improvements

Planned production enhancements:

JWT or API key authentication

Rate limiting

Request size limits

Logging and monitoring

Input sanitization

6. Trade-offs

Used Whisper “tiny” model for speed over accuracy.

Processing is synchronous for simplicity.

Local storage is used instead of cloud storage for development simplicity.

These decisions prioritize clarity and simplicity for demonstration purposes.

7. Conclusion

This implementation demonstrates:

Clean API design

Proper resource handling

Audio preprocessing best practices

Structured transcription output

Consideration for production scalability

The system can be easily extended into a production-ready architecture with background processing, cloud storage, and distributed deployment.
