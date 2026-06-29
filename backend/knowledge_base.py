CLINIC_INFO = {
    "name": "Rahat Homeopathic & Physiotherapy Clinic",
    "address": "R 125, Street 2, 11C 2nd St, Sirsyed Town, Sector 11 C 2, North Karachi, Karachi, 75850, Pakistan",
    "hours": {
        "monday_saturday": "08:30 PM - 11:00 PM",
        "sunday": "11:00 AM - 01:00 PM",
    },
    "phone": "+92 315 2968384",
    "email": "rahatphysio9@gmail.com",
    "fee": "Rs. 500",
    "services": [
        "Abdominal Pain Treatment",
        "Asthma Management",
        "Backache Treatment",
        "Electrotherapy",
        "Hepatitis Management",
    ],
    "conditions_treated": [
        "Abdomen Pain",
        "Anemia",
        "Arthritis",
        "Arthritis Management",
        "Back Ache",
    ],
    "physiotherapists": [
        {
            "name": "Dr. Naseem Alam (Dr. Naseem Ahmed Khan)",
            "specialty": "Homeopath & Physiotherapist",
            "experience": "15+ years (2007 - present)",
        },
    ],
    "about_doctor": (
        "Dr. Naseem Alam (also known as Dr. Naseem Ahmed Khan) is a highly experienced Homeopath and "
        "Physiotherapist with over 15 years of practice. He holds a DHMS (Diploma in Homeopathic Medicine "
        "and Surgery), RHMP certification, and a Physiotherapy Technician Certificate. He believes in "
        "holistic healing and patient-centered care, combining natural homeopathic remedies with modern "
        "physiotherapy techniques. He is a member of the National Council for Homeopathy Pakistan and "
        "practices at Rahat Homeopathic & Physiotherapy Clinic in North Karachi. He treats a wide range "
        "of acute and chronic conditions including abdominal pain, asthma, backache, arthritis, and more. "
        "He has an 83% patient satisfaction score. Dr. Naseem is fluent in English and Urdu."
    ),
    "education": [
        "DHMS (Diploma in Homeopathic Medicine and Surgery), Pakistan",
        "RHMP (Registered Homeopathic Medical Practitioner), Pakistan",
        "Physiotherapy Technician Certificate, Pakistan",
    ],
    "professional_memberships": [
        "National Council for Homeopathy Pakistan",
    ],
    "languages": ["English", "Urdu"],
    "practice_locations": [
        "Rahat Homeopathic & Physiotherapy Clinic, North Karachi",
        "Online Video Consultation (available nationwide)",
        "Satti Muhammad Lohsar Medical Complex, Barnala, Bhimber, AJK",
    ],
    "pricing": {
        "Online Video Consultation": "Rs. 500",
        "In-person Consultation": "Rs. 500",
    },
    "emergency_disclaimer": (
        "If you are experiencing a medical emergency, please call 911 or "
        "visit your nearest emergency room immediately. Do not delay seeking emergency care."
    ),
}

SYSTEM_PROMPT = """You are the friendly AI assistant for Dr. Naseem Alam's Rahat Homeopathic & Physiotherapy Clinic. Be warm, conversational, and helpful — like a real clinic receptionist who genuinely cares.

## Rules
- Be warm, natural, and conversational. Use a friendly tone as if you are speaking to a patient in person. Feel free to use simple emojis occasionally like 😊 👍 to add warmth, but don't overdo it.
- Avoid markdown formatting (no asterisks, bold, or italics) — keep responses clean and readable.
- ONLY answer using the clinic information provided below. Do not make up information.
- NEVER provide medical diagnoses, treatment recommendations, or interpret symptoms. Always recommend a consultation with Dr. Naseem Alam for personalized advice.
- NEVER provide emergency medical advice. If someone describes an emergency, instruct them to call 911 or visit the nearest emergency room immediately.
- If you do not know the answer, say so naturally and suggest they call the clinic at +92 315 2968384 to speak with Dr. Naseem directly.
- When mentioning the doctor, refer to him as Dr. Naseem Alam. Speak about him with respect and warmth — he has over 15 years of experience and truly cares about his patients.

## About the Doctor
{about_doctor}

## Qualifications
{education}

## Professional Memberships
{memberships}

## Languages Spoken
{languages}

## Practice Locations
{locations}

## Clinic Information
Name: {name}
Address: {address}

Hours:
- Monday to Saturday: {hours_ms}
- Sunday: {hours_sun}

Phone: {phone}
Consultation Fee: {fee}

Services Offered:
{services}

Conditions Treated:
{conditions}

Physiotherapists:
{physiotherapists}

Pricing:
- Online Video Consultation: {price_online}
- In-person Consultation: {price_inperson}

{disclaimer}
"""


def build_system_prompt() -> str:
    info = CLINIC_INFO
    services_bullets = "\n".join(f"- {s}" for s in info["services"])
    conditions_bullets = "\n".join(f"- {c}" for c in info["conditions_treated"])
    education_bullets = "\n".join(f"- {e}" for e in info["education"])
    memberships_bullets = "\n".join(f"- {m}" for m in info["professional_memberships"])
    languages_text = ", ".join(info["languages"])
    locations_bullets = "\n".join(f"- {l}" for l in info["practice_locations"])
    physios_text = "\n".join(
        f"- {p['name']} ({p['specialty']}, {p['experience']})" for p in info["physiotherapists"]
    )
    return SYSTEM_PROMPT.format(
        name=info["name"],
        address=info["address"],
        about_doctor=info["about_doctor"],
        hours_ms=info["hours"]["monday_saturday"],
        hours_sun=info["hours"]["sunday"],
        phone=info["phone"],
        fee=info["fee"],
        services=services_bullets,
        conditions=conditions_bullets,
        education=education_bullets,
        memberships=memberships_bullets,
        languages=languages_text,
        locations=locations_bullets,
        physiotherapists=physios_text,
        price_online=info["pricing"]["Online Video Consultation"],
        price_inperson=info["pricing"]["In-person Consultation"],
        disclaimer=info["emergency_disclaimer"],
    )
