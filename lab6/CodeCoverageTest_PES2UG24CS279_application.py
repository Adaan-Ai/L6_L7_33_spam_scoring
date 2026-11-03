"""Lab 6 - Code (line) coverage tests for spam_scoring.py
Name: Mohammed Adaan Hamad | SRN: PES2UG24CS279

Goal: execute every line of spam_scoring.py at least once.
Run:  coverage run --source=spam_scoring -m pytest CodeCoverageTest_PES2UG24CS279_application.py
"""
from spam_scoring import score_message, classify, filter_inbox, inbox_status


# ---------- Starter examples ----------
def test_plain_message_scores_zero():
    assert score_message("hello there", False, 0) == 0


def test_low_score_is_clean():
    assert classify(1) == "clean"


# ---------- score_message ----------
def test_spam_word_shouting_word_and_many_links():
    # "free" -> +2 (spam word), "HELLO" -> +1 (upper, len > 3), 5 links -> +4
    assert score_message("free HELLO", False, 5) == 7


def test_few_links_adds_one():
    assert score_message("hi", False, 2) == 1


def test_known_sender_score_clamped_to_zero():
    # 0 - 3 = -3 -> clamped to 0
    assert score_message("hello", True, 0) == 0


# ---------- classify ----------
def test_classify_spam():
    assert classify(8) == "spam"


def test_classify_suspicious():
    assert classify(5) == "suspicious"


# ---------- filter_inbox ----------
def test_filter_inbox_counts_labels():
    messages = [
        ("free prize cash urgent", False, 5),  # 8 + 4 = 12 -> spam
        ("free prize", False, 0),              # 4 -> suspicious
        ("hello there", False, 0),             # 0 -> clean
    ]
    assert filter_inbox(messages) == {"spam": 1, "suspicious": 1, "clean": 1}


# ---------- inbox_status ----------
def test_status_empty():
    assert inbox_status({"spam": 0, "suspicious": 0, "clean": 0}) == "empty"


def test_status_flooded():
    assert inbox_status({"spam": 3, "suspicious": 0, "clean": 1}) == "flooded"


def test_status_noisy():
    assert inbox_status({"spam": 1, "suspicious": 0, "clean": 3}) == "noisy"


def test_status_healthy():
    assert inbox_status({"spam": 0, "suspicious": 1, "clean": 9}) == "healthy"
