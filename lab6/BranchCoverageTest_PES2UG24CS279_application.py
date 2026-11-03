"""Lab 6 - Branch coverage tests for spam_scoring.py
Name: Mohammed Adaan Hamad | SRN: PES2UG24CS279

Goal: make every decision in spam_scoring.py evaluate to BOTH True and False.
Run:  coverage run --branch --source=spam_scoring -m pytest BranchCoverageTest_PES2UG24CS279_application.py
"""
from spam_scoring import score_message, classify, filter_inbox, inbox_status


# =====================================================================
# score_message
# =====================================================================

# Decision: for word in text.split() (line 6) -> loop body SKIPPED (empty text)
def test_empty_text_skips_loop():
    assert score_message("", False, 0) == 0


# Decision: word.lower().strip("!.,") in SPAM_WORDS (line 7) -> True
def test_spam_word_true():
    assert score_message("free", False, 0) == 2


# Decision: word in SPAM_WORDS (line 7) -> True (case-insensitive + punctuation stripped)
def test_spam_word_true_with_case_and_punctuation():
    assert score_message("WINNER!", False, 0) == 2


# Decision: word in SPAM_WORDS (line 7) -> False, then
# Decision: word.isupper() and len(word) > 3 (line 9) -> True
def test_shouting_word_true():
    assert score_message("HELLO", False, 0) == 1


# Decision: word.isupper() and len(word) > 3 (line 9) -> False (not upper-case)
def test_lowercase_word_not_shouting():
    assert score_message("hello", False, 0) == 0


# Decision: word.isupper() and len(word) > 3 (line 9) -> False (upper-case but too short)
def test_short_uppercase_word_not_shouting():
    assert score_message("OK", False, 0) == 0


# Decision: link_count > 3 (line 11) -> True
def test_link_count_greater_than_three_true():
    assert score_message("hi", False, 4) == 4


# Decision: link_count > 3 (line 11) -> False, then
# Decision: link_count > 0 (line 13) -> True
def test_link_count_between_one_and_three():
    assert score_message("hi", False, 3) == 1


# Decision: link_count > 0 (line 13) -> False
def test_zero_links():
    assert score_message("hi", False, 0) == 0


# Decision: sender_known (line 15) -> True, and
# Decision: score < 0 (line 17) -> False (score stays positive after -3)
def test_known_sender_score_stays_positive():
    # free(+2) free(+2) free(+2) = 6; 6 - 3 = 3
    assert score_message("free free free", True, 0) == 3


# Decision: sender_known (line 15) -> True, and
# Decision: score < 0 (line 17) -> True (clamped to 0)
def test_known_sender_score_clamped_to_zero():
    assert score_message("hello", True, 0) == 0


# Decision: sender_known (line 15) -> False
def test_unknown_sender_no_deduction():
    assert score_message("free", False, 0) == 2


# =====================================================================
# classify
# =====================================================================

# Decision: score >= 8 (line 23) -> True
def test_classify_spam():
    assert classify(8) == "spam"


# Decision: score >= 8 (line 23) -> False, then
# Decision: score >= 4 (line 25) -> True
def test_classify_suspicious():
    assert classify(4) == "suspicious"


# Decision: score >= 4 (line 25) -> False
def test_classify_clean():
    assert classify(3) == "clean"


# =====================================================================
# filter_inbox
# =====================================================================

# Decision: for text, known, links in messages (line 32) -> loop SKIPPED (empty list)
def test_filter_inbox_empty_list():
    assert filter_inbox([]) == {"spam": 0, "suspicious": 0, "clean": 0}


# Decision: for ... in messages (line 32) -> loop EXECUTED for every label
def test_filter_inbox_mixed_messages():
    messages = [
        ("free prize cash urgent", False, 5),  # 8 + 4 = 12 -> spam
        ("free prize", False, 0),              # 4 -> suspicious
        ("hello there", False, 0),             # 0 -> clean
    ]
    assert filter_inbox(messages) == {"spam": 1, "suspicious": 1, "clean": 1}


# =====================================================================
# inbox_status
# =====================================================================

# Decision: total == 0 (line 40) -> True
def test_status_empty():
    assert inbox_status({"spam": 0, "suspicious": 0, "clean": 0}) == "empty"


# Decision: total == 0 (line 40) -> False, then
# Decision: ratio > 0.5 (line 43) -> True
def test_status_flooded():
    assert inbox_status({"spam": 3, "suspicious": 0, "clean": 1}) == "flooded"


# Decision: ratio > 0.5 (line 43) -> False, then
# Decision: ratio > 0.2 (line 45) -> True
def test_status_noisy():
    assert inbox_status({"spam": 1, "suspicious": 0, "clean": 3}) == "noisy"


# Decision: ratio > 0.2 (line 45) -> False
def test_status_healthy():
    assert inbox_status({"spam": 0, "suspicious": 1, "clean": 9}) == "healthy"


# Boundary: ratio exactly 0.5 is NOT > 0.5 -> falls to "noisy"
def test_status_boundary_half_is_noisy():
    assert inbox_status({"spam": 1, "suspicious": 0, "clean": 1}) == "noisy"
