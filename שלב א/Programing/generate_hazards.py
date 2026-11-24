
import csv
import json
import random
from pathlib import Path

random.seed(42)

output = Path(__file__).resolve().parent.parent / "hazard_data.csv"

hazard_types = [
    "Oil Leak",
    "Brake Failure",
    "Tire Damage",
    "Electrical Fault",
    "Fuel Leak",
    "Hydraulic Problem",
    "Engine Overheating",
    "Damaged Wing"
]

risk_levels = ["Low", "Medium", "High", "Critical"]

locations = [
    "Left Engine",
    "Right Engine",
    "Landing Gear",
    "Left Wing",
    "Right Wing",
    "Cockpit",
    "Cabin",
    "Fuel System"
]

with open(output, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "hazardid",
        "hazardtype",
        "risklevel",
        "location",
        "hazarddetailsjson"
    ])

    for hazard_id in range(1, 551):
        hazard_type = random.choice(hazard_types)
        risk_level = random.choice(risk_levels)
        location = random.choice(locations)

        details = {
            "detected_during": "Safety Inspection",
            "requires_immediate_action": risk_level in ["High", "Critical"],
            "notes": f"{hazard_type} detected at {location}"
        }

        # Some optional JSON fields contain NULL
        json_value = (
            None if random.random() < 0.15
            else json.dumps(details)
        )

        writer.writerow([
            hazard_id,
            hazard_type,
            risk_level,
            location,
            json_value
        ])

print("Successfully generated 550 hazards!")
