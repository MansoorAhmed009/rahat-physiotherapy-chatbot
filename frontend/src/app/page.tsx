import dynamic from "next/dynamic";

const Chatbot = dynamic(() => import("@/components/Chatbot"), { ssr: false });

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 via-white to-blue-50 px-4 py-8">
      <div className="text-center mb-6">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-dental-100 rounded-full mb-4">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="w-8 h-8 text-dental-600"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M4.5 12.75l6 6 9-13.5"
            />
          </svg>
        </div>
        <h2 className="text-lg font-semibold text-gray-700">
          Rahat Homeopathic &amp; Physiotherapy Clinic
        </h2>
        <p className="text-sm text-gray-400">
          Dr. Naseem Alam — talk to our AI assistant below
        </p>
      </div>

      <Chatbot />

      <footer className="mt-6 text-xs text-gray-400 text-center max-w-md">
        <p>
          This AI assistant provides general clinic information only. It does
          not provide medical diagnoses, treatment recommendations, or emergency advice.
        </p>
      </footer>
    </main>
  );
}
