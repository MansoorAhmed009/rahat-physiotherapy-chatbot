from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[list[dict]] = []


class ChatResponse(BaseModel):
    reply: str
    intent: Optional[str] = None


class AppointmentRequest(BaseModel):
    name: str
    email: str
    phone: str
    date: str
    time: str


class AppointmentResponse(BaseModel):
    success: bool
    message: str


class LeadRequest(BaseModel):
    name: str
    email: str
    phone: str
    interest: str


class LeadResponse(BaseModel):
    success: bool
    message: str
