"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { captureLead } from "@/lib/api";

interface Props {
  interest: string;
  onComplete: (message: string) => void;
  onDismiss: () => void;
}

export default function LeadCaptureForm({ interest, onComplete, onDismiss }: Props) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmedName = name.trim();
    const trimmedEmail = email.trim();
    const trimmedPhone = phone.trim();

    if (!trimmedName) {
      setError("Name is required.");
      return;
    }
    if (!trimmedEmail || !/\S+@\S+\.\S+/.test(trimmedEmail)) {
      setError("Valid email is required.");
      return;
    }
    if (!trimmedPhone) {
      setError("Phone number is required.");
      return;
    }

    setError("");
    setLoading(true);
    try {
      const res = await captureLead({
        name: trimmedName,
        email: trimmedEmail,
        phone: trimmedPhone,
        interest,
      });
      onComplete(res.message);
    } catch {
      onComplete("Thanks for your interest! A team member will reach out soon.");
    }
    setLoading(false);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -12 }}
      className="bg-white border border-blue-100 rounded-2xl rounded-bl-sm p-4 mb-3 shadow-sm max-w-[85%] sm:max-w-[75%]"
    >
      <h3 className="text-sm font-semibold text-gray-800 mb-1">
        Want us to reach out?
      </h3>
      <p className="text-xs text-gray-500 mb-3">
        Leave your details and we&apos;ll contact you about your interest.
      </p>

      <form onSubmit={handleSubmit} className="space-y-2">
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Full Name"
          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-dental-400 focus:ring-1 focus:ring-dental-400"
        />
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email Address"
          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-dental-400 focus:ring-1 focus:ring-dental-400"
        />
        <input
          type="tel"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          placeholder="Phone Number"
          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-dental-400 focus:ring-1 focus:ring-dental-400"
        />

        {error && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-red-500 text-xs"
          >
            {error}
          </motion.p>
        )}

        <div className="flex gap-2 pt-1">
          <button
            type="button"
            onClick={onDismiss}
            className="text-xs text-gray-500 hover:text-gray-700 px-3 py-1.5 rounded-lg border border-gray-200"
          >
            Not now
          </button>
          <button
            type="submit"
            disabled={loading}
            className="text-xs bg-dental-500 hover:bg-dental-600 text-white px-4 py-1.5 rounded-lg transition-colors disabled:opacity-50"
          >
            {loading ? "Submitting..." : "Submit"}
          </button>
        </div>
      </form>
    </motion.div>
  );
}
