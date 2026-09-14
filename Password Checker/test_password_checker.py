"""
Simple automated checks for passwordchecker.py.

Run with:
    python test_password_checker.py

This doesn't require pytest - it just asserts expected behavior and prints
PASS/FAIL, which is enough for this assignment's "test with several example
passwords" step and gives repeatable proof that the rating logic behaves as
expected across weak, medium, and strong cases.
"""

from passwordchecker import PasswordChecker

CASES = [
    # (password, expected_rating)
    ("123456", "Very Weak"),        # exact match on common-password blacklist
    ("password", "Very Weak"),      # exact match on common-password blacklist
    ("hello", "Weak"),              # too short, only lowercase -> score 1
    ("aaaaaaaa", "Weak"),           # length ok + lowercase only -> score 2
    ("Summer2026", "Medium"),       # length, upper, lower, digit ok; no special -> score 4
    ("ADMIN123!", "Medium"),        # length, upper, digit, special ok; no lowercase -> score 4
    ("Password1!", "Strong"),       # all five checks pass, not on blacklist
    ("Qwerty123!", "Strong"),       # all five checks pass, not an exact blacklist match
    ("Tr0ub4dor&3!!", "Strong"),    # long, all char types, not on blacklist
]


def main() -> None:
    checker = PasswordChecker()
    failures = 0

    for password, expected in CASES:
        report = checker.evaluate(password)
        actual = report.rating.value
        status = "PASS" if actual == expected else "FAIL"
        if status == "FAIL":
            failures += 1
        print(f"[{status}] {password!r}: got {actual!r}, expected {expected!r}")
        for item in report.feedback:
            print(f"        - {item}")

    print()
    if failures:
        print(f"{failures} test(s) failed.")
        raise SystemExit(1)
    print("All tests passed.")


if __name__ == "__main__":
    main()