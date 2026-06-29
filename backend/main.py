import os
import time
import logging
from collections import defaultdict

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import Appointment, Lead
from schemas import (
    ChatRequest,
    ChatResponse,
    AppointmentRequest,
    AppointmentResponse,
    LeadRequest,
    LeadResponse,
)
from chat import get_chat_response, detect_intent
from notifications import notify_new_appointment, notify_new_lead

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dr. Naseem Alam Clinic AI Assistant API",
    description="Backend API for Dr. Naseem Alam's Physiotherapy & Homeopathic Clinic AI Assistant",
    version="1.0.0",
)

# --- CORS ---
cors_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000",
).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Rate Limiter ---
RATE_LIMIT_REQUESTS = 30
RATE_LIMIT_WINDOW = 60  # seconds
request_log: dict[str, list[float]] = defaultdict(list)


def check_rate_limit(client_ip: str):
    now = time.time()
    cutoff = now - RATE_LIMIT_WINDOW
    request_log[client_ip] = [t for t in request_log[client_ip] if t > cutoff]
    if len(request_log[client_ip]) >= RATE_LIMIT_REQUESTS:
        logger.warning("Rate limit exceeded for IP: %s", client_ip)
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please wait a moment before sending another message.",
        )
    request_log[client_ip].append(now)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Dr. Naseem Alam Clinic AI Assistant"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, req: Request):
    check_rate_limit(req.client.host)

    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    logger.info("Chat request from %s: %.60s", req.client.host, request.message)
    reply = get_chat_response(request.message, request.conversation_history)
    intent = detect_intent(request.message)
    logger.info("Chat response intent=%s", intent)

    return ChatResponse(reply=reply, intent=intent)


@app.post("/appointment", response_model=AppointmentResponse)
def book_appointment(data: AppointmentRequest, db: Session = Depends(get_db)):
    if not all([data.name, data.email, data.phone, data.date, data.time]):
        raise HTTPException(status_code=400, detail="All fields are required.")

    appointment = Appointment(
        name=data.name,
        email=data.email,
        phone=data.phone,
        date=data.date,
        time=data.time,
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    logger.info("Appointment booked: %s on %s at %s", data.name, data.date, data.time)
    notify_new_appointment(data.name, data.email, data.phone, data.date, data.time)

    return AppointmentResponse(
        success=True,
        message=(
            f"Wonderful, {data.name}! Your appointment is all set for "
            f"{data.date} at {data.time}. We have sent a confirmation to {data.email}. "
            f"Dr. Naseem Alam and the team look forward to seeing you. If anything comes up, "
            f"feel free to call us at +92 315 2968384."
        ),
    )


@app.post("/lead", response_model=LeadResponse)
def capture_lead(data: LeadRequest, db: Session = Depends(get_db)):
    if not all([data.name, data.email, data.phone, data.interest]):
        raise HTTPException(status_code=400, detail="All fields are required.")

    lead = Lead(
        name=data.name,
        email=data.email,
        phone=data.phone,
        interest=data.interest,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)

    logger.info("Lead captured: %s interested in %s", data.name, data.interest)
    notify_new_lead(data.name, data.email, data.phone, data.interest)

    return LeadResponse(
        success=True,
        message=(
            f"Thank you so much, {data.name}! 😊 Dr. Naseem Alam's team has received your "
            f"inquiry about {data.interest} and will get back to you very soon. "
            f"In the meantime, if you have any urgent questions, feel free to call us directly "
            f"at +92 315 2968384. We are here to help!"
        ),
    )
