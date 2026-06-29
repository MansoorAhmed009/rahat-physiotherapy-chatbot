# Rahat Homeopathic & Physiotherapy Clinic — AI Chatbot

An AI-powered virtual assistant for **Dr. Naseem Alam's** Rahat Homeopathic & Physiotherapy Clinic. Built with **Next.js**, **FastAPI**, **Google Gemini**, and **SQLite**.

---

## Features

| Feature | Description |
|---------|-------------|
| FAQ Support | Answers clinic hours, services, pricing, location |
| Appointment Booking | Multi-step form to collect patient details |
| Lead Capture | Detects buying intent and stores inquiries |
| Conversation Memory | Maintains context during the session |
| Notifications | Sends email (and optional WhatsApp) alerts on new booking or inquiry |
| Modern UI | Smooth animations, responsive design, typing indicators |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js, TypeScript, Tailwind CSS, Framer Motion |
| Backend | FastAPI (Python) |
| AI Model | Google Gemini 2.5 Flash |
| Database | SQLite (via SQLAlchemy) |
| Notifications | SMTP (email) + Twilio (WhatsApp, optional) |

## Project Structure

```
rahat-physiotherapy-chatbot/
├── backend/
│   ├── main.py              # FastAPI app with endpoints
│   ├── database.py          # SQLAlchemy setup
│   ├── models.py            # Appointment & Lead models
│   ├── schemas.py           # Pydantic schemas
│   ├── chat.py              # Gemini integration + intent detection
│   ├── knowledge_base.py    # Clinic info, Dr. Naseem Alam details, system prompt
│   ├── notifications.py     # Email + WhatsApp notification sender
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js pages & layout
│   │   ├── components/      # Chat UI components
│   │   └── lib/             # API client
│   ├── package.json
│   └── ...
└── README.md
```

## Quick Start

### 1. Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and add your **Gemini API key** (get one free at [Google AI Studio](https://aistudio.google.com/app/apikey)):

```
GEMINI_API_KEY=your-key-here
```

Start the backend:

```bash
uvicorn main:app --reload
```

API runs at `http://127.0.0.1:8000`

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

App runs at `http://localhost:3000`

### 3. Email Notifications (optional)

To receive email alerts when patients book or inquire:

1. Enable **2-Factor Authentication** on your Gmail at [Google Security](https://myaccount.google.com/security)
2. Generate an **App Password** at [App Passwords](https://myaccount.google.com/apppasswords)
3. Add to `.env`:

```
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-letter-app-password
DR_EMAIL_TO=rahatphysio9@gmail.com
```

### 4. WhatsApp Notifications (optional)

Sign up at [Twilio](https://console.twilio.com), get a WhatsApp-enabled number, and add to `.env`:

```
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_WHATSAPP_FROM=+14155238886
DR_WHATSAPP_TO=+923152968384
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/chat` | Send a message and get AI reply |
| POST | `/appointment` | Book an appointment |
| POST | `/lead` | Capture a lead / inquiry |

## Deployment

### Deploy Frontend to Vercel

1. Go to [https://vercel.com](https://vercel.com) and sign in with GitHub
2. Click **Add New** → **Project**
3. Import the `rahat-physiotherapy-chatbot` repository
4. Set **Root Directory** to `frontend`
5. Vercel auto-detects Next.js — no changes needed
6. Add environment variable:
   - `NEXT_PUBLIC_API_URL` → your Render backend URL (e.g., `https://rahat-physiotherapy-backend.onrender.com`)
7. Click **Deploy**

Your frontend will be live at `https://rahat-physiotherapy.vercel.app`

### Deploy Backend to Render

1. Go to [https://render.com](https://render.com) and sign in with GitHub
2. Click **New +** → **Web Service**
3. Connect your `rahat-physiotherapy-chatbot` repository
4. Set:
   - **Root Directory**: `backend`
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   - `GEMINI_API_KEY` → your Gemini API key
   - `CORS_ORIGINS` → `https://rahat-physiotherapy.vercel.app`
   - `SMTP_USER`, `SMTP_PASSWORD` → (optional, for email notifications)
   - `DR_EMAIL_TO` → `rahatphysio9@gmail.com`
6. Click **Create Web Service**

### After Both Are Deployed

Update the Vercel environment variable:
- `NEXT_PUBLIC_API_URL` → `https://your-render-backend-url.onrender.com`

Then redeploy the frontend on Vercel (it auto-deploys when you push to GitHub).

## Embedding on Client Website

Once deployed, add this iframe to any HTML page on Dr. Naseem's website:

```html
<iframe
  src="https://rahat-physiotherapy.vercel.app"
  style="position:fixed; bottom:20px; right:20px; width:380px; height:600px; border:none; border-radius:16px; box-shadow:0 4px 24px rgba(0,0,0,0.15); z-index:9999;"
  title="Dr. Naseem Alam - AI Assistant"
></iframe>
```

Or use a floating chat button that opens the chatbot in a modal.

## License

MIT
