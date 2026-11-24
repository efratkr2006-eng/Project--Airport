
import random
from getpass import getpass
import psycopg

random.seed(42)

password = getpass("Enter PostgreSQL password: ")

with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="EFRAT",
    user="HILA",
    password=password
) as conn:

    with conn.cursor() as cur:

        # Get existing checks
        cur.execute('SELECT checkid FROM public."CHECK"')
        checks = [row[0] for row in cur.fetchall()]

        # Get existing hazards
        cur.execute("SELECT hazardid FROM public.hazard")
        hazards = [row[0] for row in cur.fetchall()]

        # Prevent duplicate insertion
        cur.execute("SELECT COUNT(*) FROM public.identifies")
        existing = cur.fetchone()[0]

        if existing != 0:
            raise RuntimeError("IDENTIFIES is not empty!")

        if len(checks) * len(hazards) < 750:
            raise RuntimeError("Not enough checks or hazards!")

        # Each hazard is linked to at least one check
        pairs = set()

        for hazard_id in hazards:
            check_id = random.choice(checks)
            pairs.add((check_id, hazard_id))

        # Add more unique relationships
        while len(pairs) < 750:
            check_id = random.choice(checks)
            hazard_id = random.choice(hazards)
            pairs.add((check_id, hazard_id))

        # Insert directly into PostgreSQL
        cur.executemany("""
            INSERT INTO public.identifies (checkid, hazardid)
            VALUES (%s, %s)
        """, sorted(pairs))

        cur.execute("SELECT COUNT(*) FROM public.identifies")
        total = cur.fetchone()[0]

print("Successfully inserted IDENTIFIES relationships!")
print(f"Total relationships: {total}")
print("Database transaction committed successfully!")
