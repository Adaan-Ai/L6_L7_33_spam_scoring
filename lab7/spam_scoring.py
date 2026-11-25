"""Lab 7 - Fuzz Testing: hardened version of spam_scoring.py
Name: Mohammed Adaan Hamad | SRN: PES2UG24CS279

Bugs found by fuzzing (Hypothesis) and how they were fixed:
  sender_domain : None -> AttributeError, no '@' -> IndexError,
                  'a@b@c' -> wrong domain, 'user@' -> empty domain
                  => validate type and format, return None for invalid input
  first_link    : None -> AttributeError, no 'http' -> ValueError (str.index),
                  link ended by tab/newline was not cut off
                  => use str.find, stop at any whitespace, return None if no link
  shout_ratio   : None -> TypeError, no letters ('' / '123') -> ZeroDivisionError
                  => validate type, return 0.0 when there are no letters
"""


def sender_domain(email):
    """Return the lower-cased domain of an email address, or None if invalid."""
    if not isinstance(email, str):
        return None
    email = email.strip()
    if email.count('@') != 1:
        return None
    local, domain = email.split('@')
    if not local or not domain:
        return None
    return domain.lower()


def first_link(text):
    """Return the first token starting with 'http' in text, or None if none."""
    if not isinstance(text, str):
        return None
    start = text.find('http')
    if start == -1:
        return None
    end = start
    while end < len(text) and not text[end].isspace():
        end += 1
    return text[start:end]


def shout_ratio(text):
    """Return the fraction (0.0 - 1.0) of letters in text that are upper case."""
    if not isinstance(text, str):
        return 0.0
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    upper = [c for c in letters if c.isupper()]
    return len(upper) / len(letters)


def main():
    print("==== Running sender_domain ====")
    user_input = input("Enter a sender email (e.g. offers@Deals.com): ")
    result = sender_domain(user_input)
    print("Sender Domain:", result if result is not None else "Invalid email address")

    print("\n==== Running first_link ====")
    user_input = input("Enter a message containing a link: ")
    result = first_link(user_input)
    print("First Link:", result if result is not None else "No link found")

    print("\n==== Running shout_ratio ====")
    user_input = input("Enter a message (e.g. FREE prize NOW): ")
    result = shout_ratio(user_input)
    print("Uppercase Ratio:", result)


if __name__ == "__main__":
    main()
