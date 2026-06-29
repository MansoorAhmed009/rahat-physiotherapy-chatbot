"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import ChatHeader from "./ChatHeader";
import ChatMessage from "./ChatMessage";
import TypingIndicator from "./TypingIndicator";
import ChatInput from "./ChatInput";
import SuggestedPrompts from "./SuggestedPrompts";
import AppointmentForm from "./AppointmentForm";
import LeadCaptureForm from "./LeadCaptureForm";
import { sendChat } from "@/lib/api";
import type { Message } from "@/lib/api";

const WELCOME_MESSAGE: Message = {
  role: "assistant",
  content:
    "Assalam-o-Alaikum! 😊 Welcome to Rahat Homeopathic & Physiotherapy Clinic. I'm here to help you connect with Dr. Naseem Alam. Whether you want to know about our services, check consultation fees, see clinic timings, or book an appointment — just let me know! How can I assist you today?",
  timestamp: Date.now(),
};

const STORAGE_KEY = "prime_physio_chat_messages";

function loadMessages(): Message[] {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      const parsed = JSON.parse(saved);
      if (Array.isArray(parsed) && parsed.length > 0) return parsed;
    }
  } catch {}
  return [WELCOME_MESSAGE];
}

export default function Chatbot() {
  const [messages, setMessages] = useState<Message[]>(loadMessages);
  const [isLoading, setIsLoading] = useState(false);
  const [showPrompts, setShowPrompts] = useState(
    () => localStorage.getItem(STORAGE_KEY) === null
  );
  const [showAppointmentForm, setShowAppointmentForm] = useState(false);
  const [showLeadForm, setShowLeadForm] = useState(false);
  const [leadInterest, setLeadInterest] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading, showAppointmentForm, showLeadForm]);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
  }, [messages]);

  const addMessage = (msg: Message) => {
    setMessages((prev) => [...prev, msg]);
  };

  const clearChat = () => {
    localStorage.removeItem(STORAGE_KEY);
    setMessages([WELCOME_MESSAGE]);
    setShowPrompts(true);
    setShowAppointmentForm(false);
    setShowLeadForm(false);
  };

  const handleSend = async (text: string) => {
    setShowPrompts(false);
    setShowAppointmentForm(false);
    setShowLeadForm(false);

    const userMsg: Message = {
      role: "user",
      content: text,
      timestamp: Date.now(),
    };
    addMessage(userMsg);
    setIsLoading(true);

    try {
      const history = messages.map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const res = await sendChat(text, history);

      const botMsg: Message = {
        role: "assistant",
        content: res.reply,
        timestamp: Date.now(),
      };
      addMessage(botMsg);

      if (res.intent === "appointment") {
        setShowAppointmentForm(true);
      } else if (res.intent === "lead") {
        setLeadInterest(text);
        setShowLeadForm(true);
      }
    } catch {
      addMessage({
        role: "assistant",
        content:
          "Oh no, it looks like I am having a bit of a technical hiccup! 😅 Please try again in a moment, or feel free to call Dr. Naseem Alam directly at +92 315 2968384. We would be happy to help you over the phone!",
        timestamp: Date.now(),
      });
    }

    setIsLoading(false);
  };

  const handleLeadComplete = (msg: string) => {
    setShowLeadForm(false);
    addMessage({
      role: "assistant",
      content: msg,
      timestamp: Date.now(),
    });
  };

  const handleAppointmentComplete = (msg: string) => {
    setShowAppointmentForm(false);
    addMessage({
      role: "assistant",
      content: msg,
      timestamp: Date.now(),
    });
  };

  const handleAppointmentCancel = () => {
    setShowAppointmentForm(false);
    addMessage({
      role: "assistant",
      content:
        "No worries at all! 😊 Take your time. Whenever you feel ready to book, just let me know. You can also call Dr. Naseem Alam directly at +92 315 2968384. We are always happy to help!",
      timestamp: Date.now(),
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4 }}
      className="w-full max-w-md mx-auto bg-gray-50 rounded-2xl shadow-xl border border-gray-200 overflow-hidden flex flex-col h-[600px] sm:h-[650px]"
    >
      <ChatHeader onClear={clearChat} />

      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-1">
        {messages.map((msg, i) => (
          <ChatMessage key={`${msg.timestamp}-${i}`} message={msg} />
        ))}

        <AnimatePresence>
          {isLoading && <TypingIndicator />}
        </AnimatePresence>

        <AnimatePresence>
          {showAppointmentForm && (
            <AppointmentForm
              onComplete={handleAppointmentComplete}
              onCancel={handleAppointmentCancel}
            />
          )}
        </AnimatePresence>

        <AnimatePresence>
          {showLeadForm && (
            <LeadCaptureForm
              interest={leadInterest}
              onComplete={handleLeadComplete}
              onDismiss={() => setShowLeadForm(false)}
            />
          )}
        </AnimatePresence>

        <div ref={bottomRef} />
      </div>

      <SuggestedPrompts
        visible={showPrompts && messages.length === 1}
        onSelect={handleSend}
      />

      <ChatInput onSend={handleSend} disabled={isLoading} />
    </motion.div>
  );
}
