#!/usr/bin/env python3
"""
password_checker.py

Password Strength Checker
Vortex Tech Cyber Security Internship - Week 2 Task

Evaluates password strength based on:
    - Length
    - Character variety (uppercase, lowercase, digits, special characters)
    - Membership in a common/breached password blacklist

Usage:
    python password_checker.py                  # interactive mode
    python password_checker.py -p "MyP@ssw0rd"  # check a single password
    python password_checker.py --demo           # run built-in demo/test cases
"""

from __future__ import annotations

import argparse
import string
from dataclasses import dataclass, field
from enum import Enum


class Strength(str, Enum):
    VERY_WEAK = "Very Weak"
    WEAK = "Weak"
    MEDIUM = "Medium"
    STRONG = "Strong"


# A representative sample of the most frequently observed passwords in public
# breach datasets (e.g. RockYou, Have I Been Pwned password lists). This is
# not exhaustive -- in a production tool this list would be loaded from a
# proper wordlist file (see README for notes on scaling this).
COMMON_PASSWORDS: frozenset[str] = frozenset({
    "123456", "123456789", "12345678", "12345", "1234567",
    "1234567890", "qwerty", "password", "password1", "abc123",
    "111111", "123123", "1234", "iloveyou", "adobe123",
    "photoshop", "1q2w3e4r", "letmein", "monkey", "dragon",
    "welcome", "login", "admin", "master", "sunshine",
    "football", "shadow", "654321", "666666", "michael",
    "superman", "1qaz2wsx", "trustno1", "batman", "starwars",
    "qazwsx", "121212", "flower", "hottie", "loveme",
    "zaq1zaq1", "princess", "solo", "passw0rd", "root",
})

SPECIAL_CHARS: str = string.punctuation  # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~


@dataclass
class PasswordReport:
    """Structured result of a single password strength evaluation."""
    password_length: int
    has_upper: bool
    has_lower: bool
    has_digit: bool
    has_special: bool
    is_common: bool
    rating: Strength
    feedback: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "length": self.password_length,
            "has_upper": self.has_upper,
            "has_lower": self.has_lower,
            "has_digit": self.has_digit,
            "has_special": self.has_special,
            "is_common": self.is_common,
            "rating": self.rating.value,
            "feedback": self.feedback,
        }


class PasswordChecker:
    """Evaluates password strength using length, composition, and a
    common-password blacklist check."""

    MIN_LENGTH: int = 8

    def __init__(self, common_passwords: frozenset[str] = COMMON_PASSWORDS) -> None:
        self._common_passwords = common_passwords

    def evaluate(self, password: str) -> PasswordReport:
        """Run all checks against a password and return a PasswordReport."""
        length_ok = len(password) >= self.MIN_LENGTH
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in SPECIAL_CHARS for c in password)
        is_common = password.lower() in self._common_passwords

        feedback = self._build_feedback(
            length_ok, has_upper, has_lower, has_digit, has_special, is_common, len(password)
        )
        rating = self._rate(length_ok, has_upper, has_lower, has_digit, has_special, is_common)

        return PasswordReport(
            password_length=len(password),
            has_upper=has_upper,
            has_lower=has_lower,
            has_digit=has_digit,
            has_special=has_special,
            is_common=is_common,
            rating=rating,
            feedback=feedback,
        )

    def _rate(
        self,
        length_ok: bool,
        has_upper: bool,
        has_lower: bool,
        has_digit: bool,
        has_special: bool,
        is_common: bool,
    ) -> Strength:
        # A common password is flagged as very weak regardless of composition,
        # since attackers try these first in credential-stuffing attacks.
        if is_common:
            return Strength.VERY_WEAK

        score = sum([length_ok, has_upper, has_lower, has_digit, has_special])
        if score <= 2:
            return Strength.WEAK
        if score in (3, 4):
            return Strength.MEDIUM
        return Strength.STRONG

    def _build_feedback(
        self,
        length_ok: bool,
        has_upper: bool,
        has_lower: bool,
        has_digit: bool,
        has_special: bool,
        is_common: bool,
        length: int,
    ) -> list[str]:
        if is_common:
            return [
                "This password appears on public breach/common-password lists. "
                "It should never be used, regardless of length or complexity."
            ]

        feedback = []
        if not length_ok:
            feedback.append(f"Use at least {self.MIN_LENGTH} characters (currently {length}).")
        if not has_upper:
            feedback.append("Add at least one uppercase letter (A-Z).")
        if not has_lower:
            feedback.append("Add at least one lowercase letter (a-z).")
        if not has_digit:
            feedback.append("Add at least one digit (0-9).")
        if not has_special:
            feedback.append(f"Add at least one special character (e.g. {SPECIAL_CHARS[:8]} ...).")
        if not feedback:
            feedback.append("No weaknesses detected against current checks.")
        return feedback


def print_report(password: str, report: PasswordReport) -> None:
    masked = "*" * report.password_length
    print(f"\nPassword : {masked}  (length: {report.password_length})")
    print(f"Rating   : {report.rating.value}")
    print("Checks:")
    print(f"  - Length >= 8       : {'PASS' if report.password_length >= PasswordChecker.MIN_LENGTH else 'FAIL'}")
    print(f"  - Uppercase letter  : {'PASS' if report.has_upper else 'FAIL'}")
    print(f"  - Lowercase letter  : {'PASS' if report.has_lower else 'FAIL'}")
    print(f"  - Digit             : {'PASS' if report.has_digit else 'FAIL'}")
    print(f"  - Special character : {'PASS' if report.has_special else 'FAIL'}")
    print(f"  - Common password   : {'FLAGGED' if report.is_common else 'OK'}")
    print("Feedback:")
    for tip in report.feedback:
        print(f"  - {tip}")


def run_demo(checker: PasswordChecker) -> None:
    """Runs the checker against a fixed set of generic sample passwords
    covering each strength tier."""
    demo_passwords = [
        "123456",          # common password -> Very Weak
        "qwerty",          # common password -> Very Weak
        "sample",          # too short, no variety -> Weak
        "Sample123",       # missing special char -> Medium
        "Sample@123",      # meets all checks -> Strong
        "Tr!ckyP@ss2026",  # long + full variety -> Strong
    ]

    print("=" * 60)
    print("PASSWORD STRENGTH CHECKER -- DEMO RUN")
    print("=" * 60)
    for pwd in demo_passwords:
        print_report(pwd, checker.evaluate(pwd))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate password strength (length, composition, common-password check)."
    )
    parser.add_argument(
        "-p", "--password",
        help="Password to evaluate. If omitted, runs in interactive mode.",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run against a fixed set of generic demo passwords and exit.",
    )
    args = parser.parse_args()

    checker = PasswordChecker()

    if args.demo:
        run_demo(checker)
        return

    if args.password:
        print_report(args.password, checker.evaluate(args.password))
        return

    print("Password Strength Checker (interactive mode). Press Ctrl+C to exit.")
    try:
        while True:
            pwd = input("\nEnter a password to check: ")
            if not pwd:
                continue
            print_report(pwd, checker.evaluate(pwd))
    except KeyboardInterrupt:
        print("\nExiting.")


if __name__ == "__main__":
    main()