import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Dr. Naseem Alam - Clinic AI Assistant",
  description:
    "AI assistant for Rahat Homeopathic & Physiotherapy Clinic, Dr. Naseem Alam. Book appointments, get pricing, and learn about services.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
