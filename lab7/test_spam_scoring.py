"""Lab 7 - Fuzz testing spam_scoring.py with Hypothesis
Name: Mohammed Adaan Hamad | SRN: PES2UG24CS279

Each function is fuzzed with random / malformed input (any unicode text or None).
Property 1 (robustness): the function must never raise an exception.
Property 2 (correctness): the value it returns must always make sense.

Run:  pytest test_spam_scoring.py      (or: python -m pytest test_spam_scoring.py)
"""
from hypothesis import given, example, settings, strategies as st
from spam_scoring import sender_domain, first_link, shout_ratio

FUZZ = settings(max_examples=500, deadline=None)


# ---------------------------------------------------------------------
# sender_domain(email) -> domain in lower case, or None if not an email
# ---------------------------------------------------------------------
@FUZZ
@given(st.text() | st.none())
@example("")                 # empty string
@example("no-at-sign")       # missing '@'  -> IndexError in buggy code
@example("a@b@c.com")        # more than one '@'
@example("user@")            # empty domain
@example(None)               # None -> AttributeError in buggy code
def test_sender_domain_no_crash(s):
    try:
        result = sender_domain(s)
    except Exception as e:
        assert False, f"sender_domain crashed with: {e!r} on input {s!r}"
    # the result must be either None (invalid email) or a clean lower-case domain
    assert result is None or isinstance(result, str)
    if result is not None:
        assert result != ""
        assert "@" not in result
        assert result == result.lower()


@FUZZ
@given(st.emails())
def test_sender_domain_valid_email(email):
    # for a well-formed address the domain part is returned in lower case
    assert sender_domain(email) == email.rsplit("@", 1)[1].lower()


# ---------------------------------------------------------------------
# first_link(text) -> first 'http...' token in the text, or None
# ---------------------------------------------------------------------
@FUZZ
@given(st.text() | st.none())
@example("")                         # empty string
@example("no link in here")          # missing 'http' -> ValueError in buggy code
@example("visit http://a.com now")
@example("go\thttp://a.com\tnow")    # link ended by a tab, not a space
@example(None)                       # None -> AttributeError in buggy code
def test_first_link_no_crash(s):
    try:
        result = first_link(s)
    except Exception as e:
        assert False, f"first_link crashed with: {e!r} on input {s!r}"
    # the result must be None or a link that really appears in the text
    assert result is None or isinstance(result, str)
    if result is not None:
        assert result.startswith("http")
        assert result in s
        assert not any(ch.isspace() for ch in result)


@FUZZ
@given(st.text(alphabet=st.characters(blacklist_categories=("Zs", "Cc"))),
       st.text(alphabet=st.characters(blacklist_categories=("Zs", "Cc"))))
def test_first_link_finds_embedded_link(prefix_word, url_tail):
    # build "<word> http<tail> end" and make sure exactly that link comes back
    prefix_word = prefix_word.replace("h", "")   # so the prefix can never contain 'http'
    url_tail = "".join(ch for ch in url_tail if not ch.isspace())
    text = f"{prefix_word} http{url_tail} end"
    assert first_link(text) == f"http{url_tail}"


# ---------------------------------------------------------------------
# shout_ratio(text) -> fraction of letters that are upper case, in [0, 1]
# ---------------------------------------------------------------------
@FUZZ
@given(st.text() | st.none())
@example("")            # no letters -> ZeroDivisionError in buggy code
@example("12345 !!!")   # digits / punctuation only
@example("FREE prize NOW")
@example(None)          # None -> TypeError in buggy code
def test_shout_ratio_no_crash(s):
    try:
        result = shout_ratio(s)
    except Exception as e:
        assert False, f"shout_ratio crashed with: {e!r} on input {s!r}"
    # the ratio is always a number between 0 and 1
    assert isinstance(result, float)
    assert 0.0 <= result <= 1.0


@FUZZ
@given(st.text(alphabet=st.characters(min_codepoint=ord("A"), max_codepoint=ord("Z")), min_size=1))
def test_shout_ratio_all_caps_is_one(s):
    assert shout_ratio(s) == 1.0


@FUZZ
@given(st.text(alphabet=st.characters(min_codepoint=ord("a"), max_codepoint=ord("z")), min_size=1))
def test_shout_ratio_all_lower_is_zero(s):
    assert shout_ratio(s) == 0.0
