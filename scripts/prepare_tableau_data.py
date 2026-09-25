#!/usr/bin/env python3
"""Validate and decompress the committed contact-level Tableau source."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import os
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_COLUMNS = [
    "age", "job", "marital", "education", "default", "housing", "loan",
    "contact", "month", "day_of_week", "duration", "campaign", "pdays",
    "previous", "poutcome", "emp.var.rate", "cons.price.idx",
    "cons.conf.idx", "euribor3m", "nr.employed", "y", "conversion_flag",
    "prior_contacted", "age_band", "contact_attempt_band", "month_number",
]
MONTH_NUMBER = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}
EXPECTED_ROWS = 41_188
EXPECTED_CONVERSIONS = 4_640
EXPECTED_AVERAGE_ATTEMPTS = 2.57
EXPECTED_AVERAGE_DURATION = 258.29
EXPECTED_COMPRESSED_SHA256 = (
    "25ba75f76b29b0e2f90865bf5fc43378179af5925a0bc60f4ca2670529acfd2c"
)
EXPECTED_UNCOMPRESSED_SHA256 = (
    "a5c3bf2ab19f3dfa656655a827ba22f7b0ab05b884edfe588f2b0746b440c579"
)


def age_band(age: int) -> str:
    if age < 25:
        return "Under 25"
    if age < 35:
        return "25-34"
    if age < 45:
        return "35-44"
    if age < 55:
        return "45-54"
    if age < 65:
        return "55-64"
    return "65+"


def attempt_band(attempts: int) -> str:
    if attempts <= 3:
        return str(attempts)
    if attempts <= 5:
        return "4-5"
    return "6+"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def decompress(source: Path, destination: Path) -> str:
    digest = hashlib.sha256()
    with gzip.open(source, "rb") as compressed, destination.open("wb") as output:
        for block in iter(lambda: compressed.read(1024 * 1024), b""):
            digest.update(block)
            output.write(block)
    return digest.hexdigest()


def validate(path: Path) -> tuple[int, int, float, float]:
    rows = conversions = campaign_total = duration_total = 0
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != EXPECTED_COLUMNS:
            raise ValueError(
                "Tableau source columns do not match the documented schema.\n"
                f"Expected: {EXPECTED_COLUMNS}\nReceived: {reader.fieldnames}"
            )

        for line_number, row in enumerate(reader, start=2):
            try:
                age = int(row["age"])
                attempts = int(row["campaign"])
                duration = int(row["duration"])
                previous = int(row["previous"])
                conversion = int(row["conversion_flag"])
                prior_contacted = int(row["prior_contacted"])
                month_number = int(row["month_number"])
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Invalid numeric value on CSV line {line_number}."
                ) from exc

            expected_conversion = int(row["y"] == "yes")
            if row["y"] not in {"yes", "no"} or conversion != expected_conversion:
                raise ValueError(f"Outcome mismatch on CSV line {line_number}.")
            if prior_contacted != int(previous > 0):
                raise ValueError(
                    f"Prior Contacted mismatch on CSV line {line_number}."
                )
            if row["age_band"] != age_band(age):
                raise ValueError(f"Age Band mismatch on CSV line {line_number}.")
            if row["contact_attempt_band"] != attempt_band(attempts):
                raise ValueError(
                    f"Contact Attempt Band mismatch on CSV line {line_number}."
                )
            if month_number != MONTH_NUMBER.get(row["month"]):
                raise ValueError(f"Month Number mismatch on CSV line {line_number}.")

            rows += 1
            conversions += conversion
            campaign_total += attempts
            duration_total += duration

    if rows == 0:
        raise ValueError("Tableau source contains no contact rows.")
    average_attempts = round(campaign_total / rows, 2)
    average_duration = round(duration_total / rows, 2)
    checks = {
        "contacts": (rows, EXPECTED_ROWS),
        "conversions": (conversions, EXPECTED_CONVERSIONS),
        "average attempts": (average_attempts, EXPECTED_AVERAGE_ATTEMPTS),
        "average duration": (average_duration, EXPECTED_AVERAGE_DURATION),
    }
    failures = [
        f"{name}: expected {expected}, got {actual}"
        for name, (actual, expected) in checks.items()
        if actual != expected
    ]
    if failures:
        raise ValueError("Validation failed:\n- " + "\n- ".join(failures))
    return rows, conversions, average_attempts, average_duration


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate and decompress the contact-level Tableau source."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=ROOT / "data" / "bank_marketing_clean.csv.gz",
        help="committed gzip source (default: data/bank_marketing_clean.csv.gz)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "tableau" / "bank_marketing_tableau.csv",
        help="validated CSV destination (default: tableau/bank_marketing_tableau.csv)",
    )
    args = parser.parse_args()

    source = args.source.resolve()
    output = args.output.resolve()
    if not source.is_file():
        raise FileNotFoundError(f"Tableau source not found: {source}")
    if source == output:
        raise ValueError("Source and output paths must be different.")

    compressed_digest = sha256(source)
    if compressed_digest != EXPECTED_COMPRESSED_SHA256:
        raise ValueError(
            "Compressed SHA-256 mismatch: "
            f"expected {EXPECTED_COMPRESSED_SHA256}, got {compressed_digest}"
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix="bank-tableau-", suffix=".csv", dir=output.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        uncompressed_digest = decompress(source, temporary)
        if uncompressed_digest != EXPECTED_UNCOMPRESSED_SHA256:
            raise ValueError(
                "Uncompressed SHA-256 mismatch: "
                f"expected {EXPECTED_UNCOMPRESSED_SHA256}, got {uncompressed_digest}"
            )
        rows, conversions, average_attempts, average_duration = validate(temporary)
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)

    print(f"Prepared {rows:,} Tableau contact rows in {output}.")
    print(f"Conversions: {conversions:,}")
    print(f"Average attempts: {average_attempts:.2f}")
    print(f"Average duration: {average_duration:.2f} seconds")
    print(f"Compressed SHA-256: {compressed_digest}")
    print(f"Uncompressed SHA-256: {uncompressed_digest}")


if __name__ == "__main__":
    main()
