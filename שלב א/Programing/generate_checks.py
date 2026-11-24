
import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

output = Path(__file__).resolve().parent.parent / "check_data.csv"

check_types = [
    "Pre-Flight",
    "Routine",
    "Technical",
    "Emergency"
]

start_date = date(2025, 1, 1)

with open(output, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "checkid",
        "checkdate",
        "checktype",
        "checkresultjson",
        "nextcheckdate",
        "employeeid",
        "airplaneid"
    ])

    for check_id in range(1, 651):
        check_date = start_date + timedelta(
            days=random.randint(0, 620)
        )

        next_check = check_date + timedelta(days=90)

        employee_id = ((check_id - 1) % 60) + 1
        airplane_id = ((check_id - 1) % 120) + 1

        results = {
            "brakes": random.choice(["OK", "Fault"]),
            "tires": random.choice(["OK", "OK", "Fault"]),
            "lights": random.choice(["OK", "OK", "Fault"]),
            "oil_leak": random.choice([False, False, True])
        }

        writer.writerow([
            check_id,
            check_date.isoformat(),
            random.choice(check_types),
            json.dumps(results),
            next_check.isoformat(),
            employee_id,
            airplane_id
        ])

print("Successfully generated 650 checks!")
