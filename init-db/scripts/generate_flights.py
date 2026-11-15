
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

# Folder for the generated data
output = Path("init-db/flight_data.csv")

routes = [
    ("TLV", "LHR", 330),
    ("TLV", "CDG", 300),
    ("TLV", "FCO", 225),
    ("TLV", "ATH", 125),
    ("TLV", "DXB", 195),
    ("TLV", "BER", 245),
    ("TLV", "AMS", 300),
]

start_date = date(2025, 1, 1)

with open(output, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "flightid",
        "flightdate",
        "departure",
        "destination",
        "duration",
        "airplaneid"
    ])

    for flight_id in range(1, 701):
        departure, destination, duration = random.choice(routes)

        flight_date = start_date + timedelta(
            days=random.randint(0, 670)
        )

        airplane_id = ((flight_id - 1) % 120) + 1

        writer.writerow([
            flight_id,
            flight_date.isoformat(),
            departure,
            destination,
            duration,
            airplane_id
        ])

print("Successfully generated 700 flights!")
