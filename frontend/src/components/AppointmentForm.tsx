"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { bookAppointment } from "@/lib/api";

interface Props {
  onComplete: (message: string) => void;
  onCancel: () => void;
}

function getTodayStr(): string {
  return new Date().toISOString().split("T")[0];
}

export default function AppointmentForm({ onComplete, onCancel }: Props) {
  const [step, setStep] = useState(0);
  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    date: "",
    time: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const fields = [
    { key: "name", label: "Full Name", type: "text", placeholder: "John Doe" },
    {
      key: "email",
      label: "Email Address",
      type: "email",
      placeholder: "john@example.com",
    },
    {
      key: "phone",
      label: "Phone Number",
      type: "tel",
      placeholder: "(555) 123-4567",
    },
    { key: "date", label: "Preferred Date", type: "date", placeholder: "", min: getTodayStr() },
    { key: "time", label: "Preferred Time", type: "time", placeholder: "" },
  ];

  const current = fields[step];

  const validateField = (key: string, val: string): string | null => {
    if (!val.trim()) return `${current.label} is required.`;
    if (key === "email" && !/\S+@\S+\.\S+/.test(val)) return "Please enter a valid email.";
    if (key === "date" && val < getTodayStr()) return "Date must be today or in the future.";
    if (key === "time") {
      const hours = parseInt(val.split(":")[0], 10);
      const mins = parseInt(val.split(":")[1], 10);
      if (isNaN(hours) || isNaN(mins)) return "Please enter a valid time.";
      const totalMinutes = hours * 60 + mins;
      const weekday = new Date(form.date + "T12:00:00").getDay();
      const isWeekend = weekday === 0 || weekday === 6;
      if (isWeekend) {
        if (totalMinutes < 660 || totalMinutes > 780) return "Sunday hours: 11:00 AM - 1:00 PM.";
      } else {
        if (totalMinutes < 1230 || totalMinutes > 1380) return "Weekday hours: 8:30 PM - 11:00 PM.";
      }
    }
    return null;
  };

  const handleNext = () => {
    const val = form[current.key as keyof typeof form];
    const validationError = validateField(current.key, val);
    if (validationError) {
      setError(validationError);
      return;
    }
    setError("");
    if (step < fields.length - 1) {
      setStep((s) => s + 1);
    } else {
      submitForm();
    }
  };

  const submitForm = async () => {
    setLoading(true);
    try {
      const res = await bookAppointment(form);
      onComplete(res.message);
    } catch {
      onComplete(
        "Sorry, we couldn't book your appointment right now. Please call us at +92 315 2968384."
      );
    }
    setLoading(false);
  };

  const handleBack = () => {
    if (step > 0) setStep((s) => s - 1);
    else onCancel();
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -12 }}
      className="bg-white border border-gray-100 rounded-2xl rounded-bl-sm p-4 mb-3 shadow-sm max-w-[85%] sm:max-w-[75%]"
    >
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-gray-800">
          Book an Appointment
        </h3>
        <span className="text-xs text-gray-400">
          {step + 1} of {fields.length}
        </span>
      </div>

      <div className="w-full bg-gray-100 rounded-full h-1.5 mb-4">
        <motion.div
          className="bg-dental-500 h-1.5 rounded-full"
          initial={false}
          animate={{ width: `${((step + 1) / fields.length) * 100}%` }}
          transition={{ duration: 0.3 }}
        />
      </div>

      <label className="text-xs font-medium text-gray-500 mb-1 block">
        {current.label}
      </label>
      <input
        type={current.type}
        value={form[current.key as keyof typeof form]}
        onChange={(e) =>
          setForm({ ...form, [current.key]: e.target.value })
        }
        onKeyDown={(e) => e.key === "Enter" && handleNext()}
        placeholder={current.placeholder}
        min={"min" in current ? (current as any).min : undefined}
        autoFocus
        className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-dental-400 focus:ring-1 focus:ring-dental-400 mb-3"
      />

      {error && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-red-500 text-xs mb-3"
        >
          {error}
        </motion.p>
      )}

      <div className="flex gap-2">
        <button
          onClick={handleBack}
          className="text-xs text-gray-500 hover:text-gray-700 px-3 py-1.5 rounded-lg border border-gray-200"
        >
          {step === 0 ? "Cancel" : "Back"}
        </button>
        <button
          onClick={handleNext}
          disabled={loading}
          className="text-xs bg-dental-500 hover:bg-dental-600 text-white px-4 py-1.5 rounded-lg transition-colors disabled:opacity-50"
        >
          {loading
            ? "Booking..."
            : step < fields.length - 1
            ? "Next"
            : "Confirm"}
        </button>
      </div>
    </motion.div>
  );
}
