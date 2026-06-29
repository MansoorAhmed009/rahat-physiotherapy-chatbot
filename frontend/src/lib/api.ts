const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: number;
  intent?: string;
}

export interface ChatResponse {
  reply: string;
  intent?: string;
}

export interface AppointmentPayload {
  name: string;
  email: string;
  phone: string;
  date: string;
  time: string;
}

export interface LeadPayload {
  name: string;
  email: string;
  phone: string;
  interest: string;
}

export async function sendChat(
  message: string,
  history: { role: string; content: string }[]
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, conversation_history: history }),
  });
  if (!res.ok) {
    throw new Error("Failed to get chat response");
  }
  return res.json();
}

export async function bookAppointment(
  data: AppointmentPayload
): Promise<{ success: boolean; message: string }> {
  const res = await fetch(`${API_BASE}/appointment`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    throw new Error("Failed to book appointment");
  }
  return res.json();
}

export async function captureLead(
  data: LeadPayload
): Promise<{ success: boolean; message: string }> {
  const res = await fetch(`${API_BASE}/lead`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    throw new Error("Failed to capture lead");
  }
  return res.json();
}
