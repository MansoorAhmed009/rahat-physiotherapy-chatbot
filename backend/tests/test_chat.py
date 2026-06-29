from chat import detect_intent, trim_history


class TestDetectIntent:
    def test_appointment_intent(self):
        assert detect_intent("I want to book an appointment") == "appointment"
        assert detect_intent("Can I schedule a visit?") == "appointment"
        assert detect_intent("I need to see a physio") == "appointment"
        assert detect_intent("When can I come in?") == "appointment"

    def test_lead_intent(self):
        assert detect_intent("How much is a consultation?") == "lead"
        assert detect_intent("What is the cost of massage?") == "lead"
        assert detect_intent("I'm interested in dry needling") == "lead"

    def test_no_intent(self):
        assert detect_intent("What are your hours?") is None
        assert detect_intent("Where are you located?") is None
        assert detect_intent("Do you treat back pain?") is None

    def test_case_insensitive(self):
        assert detect_intent("BOOK AN APPOINTMENT") == "appointment"
        assert detect_intent("How Much?") == "lead"


class TestTrimHistory:
    def test_under_limit(self):
        history = [{"role": "user", "content": "hi"}] * 5
        assert len(trim_history(history)) == 5

    def test_over_limit(self):
        history = [{"role": "user", "content": f"msg {i}"} for i in range(25)]
        trimmed = trim_history(history)
        assert len(trimmed) == 20
        assert trimmed[0]["content"] == "msg 5"

    def test_empty_history(self):
        assert trim_history([]) == []
