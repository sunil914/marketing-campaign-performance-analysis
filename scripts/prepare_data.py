#!/usr/bin/env python3
"""Prepare the UCI Bank Marketing source file for this project.

The script uses only the Python standard library. It preserves the 21 source
columns, appends the five documented analysis fields, validates the published
KPIs and writes a 500-row browser-preview sample.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import os
import tempfile
from pathlib import Path


EXPECTED_SOURCE_COLUMNS = [
    "age", "job", "marital", "education", "default", "housing", "loan",
    "contact", "month", "day_of_week", "duration", "campaign", "pdays",
    "previous", "poutcome", "emp.var.rate", "cons.price.idx",
    "cons.conf.idx", "euribor3m", "nr.employed", "y",
]
DERIVED_COLUMNS = [
    "conversion_flag", "prior_contacted", "age_band",
    "contact_attempt_band", "month_number",
]
MONTH_NUMBER = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}
EXPECTED_ROWS = 41_188
EXPECTED_CONVERSIONS = 4_640
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


def prepare_row(source: dict[str, str]) -> dict[str, str | int]:
    row = {column: source[column].strip() for column in EXPECTED_SOURCE_COLUMNS}
    if row["y"] not in {"yes", "no"}:
        raise ValueError(f"Unexpected campaign outcome: {row['y']!r}")
    month = row["month"].lower()
    if month not in MONTH_NUMBER:
        raise ValueError(f"Unexpected campaign month: {row['month']!r}")

    attempts = int(row["campaign"])
    row.update(
        conversion_flag=int(row["y"] == "yes"),
        prior_contacted=int(int(row["previous"]) > 0),
        age_band=age_band(int(row["age"])),
        contact_attempt_band=attempt_band(attempts),
        month_number=MONTH_NUMBER[month],
    )
    return row


def open_output(path: Path):
    """Return a deterministic text stream and its underlying binary handle."""
    binary = path.open("wb")
    if path.suffix == ".gz":
        compressed = gzip.GzipFile(fileobj=binary, mode="wb", filename="", mtime=0)
        return io.TextIOWrapper(compressed, encoding="utf-8", newline=""), binary
    return io.TextIOWrapper(binary, encoding="utf-8", newline=""), binary


def sha256_uncompressed(path: Path) -> str:
    opener = gzip.open if path.suffix == ".gz" else open
    digest = hashlib.sha256()
    with opener(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Path to bank-additional-full.csv")
    parser.add_argument(
        "--output", type=Path, default=Path("data/bank_marketing_clean.csv.gz")
    )
    parser.add_argument(
        "--sample", type=Path, default=Path("data/bank_marketing_sample.csv")
    )
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.sample.parent.mkdir(parents=True, exist_ok=True)
    output_tmp = Path(tempfile.mkstemp(prefix="bank-clean-", suffix=args.output.suffix)[1])
    sample_tmp = Path(tempfile.mkstemp(prefix="bank-sample-", suffix=".csv")[1])

    rows = conversions = 0
    campaign_total = duration_total = 0
    fieldnames = EXPECTED_SOURCE_COLUMNS + DERIVED_COLUMNS
    try:
        with args.source.open(encoding="utf-8-sig", newline="") as source_stream:
            reader = csv.DictReader(source_stream, delimiter=";")
            if reader.fieldnames != EXPECTED_SOURCE_COLUMNS:
                raise ValueError(
                    "Source columns do not match bank-additional-full.csv.\n"
                    f"Expected: {EXPECTED_SOURCE_COLUMNS}\nReceived: {reader.fieldnames}"
                )

            output_stream, output_binary = open_output(output_tmp)
            with output_stream, sample_tmp.open("w", encoding="utf-8", newline="") as sample_stream:
                writer = csv.DictWriter(output_stream, fieldnames=fieldnames, lineterminator="\n")
                sample_writer = csv.DictWriter(sample_stream, fieldnames=fieldnames, lineterminator="\n")
                writer.writeheader()
                sample_writer.writeheader()
                for source_row in reader:
                    row = prepare_row(source_row)
                    writer.writerow(row)
                    if rows < 500:
                        sample_writer.writerow(row)
                    rows += 1
                    conversions += int(row["conversion_flag"])
                    campaign_total += int(row["campaign"])
                    duration_total += int(row["duration"])
            output_binary.close()

        checks = {
            "rows": (rows, EXPECTED_ROWS),
            "conversions": (conversions, EXPECTED_CONVERSIONS),
            "average attempts": (round(campaign_total / rows, 2), 2.57),
            "average duration": (round(duration_total / rows, 2), 258.29),
        }
        failures = [f"{name}: {actual} != {expected}" for name, (actual, expected) in checks.items() if actual != expected]
        digest = sha256_uncompressed(output_tmp)
        if digest != EXPECTED_UNCOMPRESSED_SHA256:
            failures.append(f"uncompressed SHA-256: {digest} != {EXPECTED_UNCOMPRESSED_SHA256}")
        if failures:
            raise ValueError("Validation failed:\n- " + "\n- ".join(failures))

        os.replace(output_tmp, args.output)
        os.replace(sample_tmp, args.sample)
        print(f"Prepared {rows:,} contacts with {conversions:,} conversions.")
        print(f"Uncompressed SHA-256: {digest}")
        print(f"Wrote {args.output} and {args.sample}.")
    finally:
        output_tmp.unlink(missing_ok=True)
        sample_tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
