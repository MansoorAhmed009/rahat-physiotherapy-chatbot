"use client";

import { motion } from "framer-motion";

const PROMPTS = [
  "What services do you offer?",
  "How much is a consultation?",
  "What are your clinic hours?",
  "Book an appointment",
];

interface Props {
  onSelect: (prompt: string) => void;
  visible: boolean;
}

export default function SuggestedPrompts({ onSelect, visible }: Props) {
  if (!visible) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, staggerChildren: 0.05 }}
      className="px-4 pb-3"
    >
      <p className="text-xs text-gray-400 mb-2 font-medium">
        Suggested questions
      </p>
      <div className="flex flex-wrap gap-2">
        {PROMPTS.map((prompt, i) => (
          <motion.button
            key={prompt}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.05 }}
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            onClick={() => onSelect(prompt)}
            className="text-xs sm:text-sm bg-white border border-dental-200 text-dental-700 rounded-full px-3.5 py-1.5 hover:bg-dental-50 hover:border-dental-300 transition-colors shadow-sm"
          >
            {prompt}
          </motion.button>
        ))}
      </div>
    </motion.div>
  );
}
