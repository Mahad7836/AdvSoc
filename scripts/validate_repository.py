from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

required_files = [
    "README.md",
    "LICENSE",
    ".env.example",
    "workflows/advsoc-core-v1.0.json",
    "results/EVALUATION_SUMMARY.md",
    "results/advsoc-postfix-metrics.json",
    "results/advsoc-security-hardening-results.json",
    "screenshots/workflow-overview.png",
]

errors = []

for relative_path in required_files:
    path = ROOT / relative_path
    if not path.exists():
        errors.append(f"Missing required file: {relative_path}")

json_directories = [
    ROOT / "workflows",
    ROOT / "results",
    ROOT / "test-data",
]

validated_json = 0

for directory in json_directories:
    if not directory.exists():
        continue

    for path in directory.rglob("*.json"):
        try:
            with path.open("r", encoding="utf-8-sig") as handle:
                json.load(handle)

            validated_json += 1

        except Exception as exc:
            errors.append(
                f"Invalid JSON: {path.relative_to(ROOT)} -> {exc}"
            )

if errors:
    print("\nAdvSOC repository validation FAILED\n")

    for error in errors:
        print(f"- {error}")

    sys.exit(1)

print("AdvSOC repository validation PASSED.")
print(f"Validated {validated_json} JSON files.")
print("Required release artifacts are present.")
