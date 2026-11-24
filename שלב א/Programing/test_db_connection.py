
import psycopg
from getpass import getpass

password = getpass("Enter PostgreSQL password: ")

try:
    with psycopg.connect(
        host="localhost",
        port=5432,
        dbname="EFRAT",
        user="HILA",
        password=password
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM public.employee")
            employees = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM public.hazard")
            hazards = cur.fetchone()[0]

            print("Connected successfully!")
            print(f"Employees: {employees}")
            print(f"Hazards: {hazards}")

except psycopg.Error as e:
    print(f"Connection failed: {e}")
