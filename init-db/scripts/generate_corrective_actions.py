
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

        # Read existing employees
        cur.execute(
            "SELECT employeeid FROM employee ORDER BY employeeid"
        )
        employees = [row[0] for row in cur.fetchall()]

        # Read existing hazards
        cur.execute("""
            SELECT hazardid, hazardtype, location
            FROM hazard
            ORDER BY hazardid
        """)
        hazards = cur.fetchall()

        # Prevent duplicate insertion
        cur.execute("SELECT COUNT(*) FROM correctiveaction")
        existing = cur.fetchone()[0]

        if existing != 0:
            raise RuntimeError(
                "CorrectiveAction is not empty. No data inserted."
            )

        if not employees or not hazards:
            raise RuntimeError("Missing employees or hazards")

        states = ["Open", "In Progress", "Completed"]

        actions = []

        for action_id in range(1, 601):

            hazard_id, hazard_type, location = hazards[
                (action_id - 1) % len(hazards)
            ]

            employee_id = random.choice(employees)

            description = (
                f"Inspect and repair {hazard_type} "
                f"at {location}"
            )

            duration = random.randint(60, 480)
            recovery_time = random.randint(15, duration)
            state = random.choice(states)

            actions.append((
                action_id,
                description,
                recovery_time,
                state,
                duration,
                hazard_id,
                employee_id
            ))

        cur.executemany("""
            INSERT INTO correctiveaction (
                actionid,
                actiondescription,
                recoverytime,
                state,
                duration,
                hazardid,
                employeeid
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, actions)

        cur.execute("SELECT COUNT(*) FROM correctiveaction")
        total = cur.fetchone()[0]

        print("Successfully inserted corrective actions!")
        print(f"Total actions: {total}")

print("Database transaction committed successfully!")
