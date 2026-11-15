# Airport Safety Management System

## 1. Project Overview

This project focuses on designing and implementing a database for the Safety Department of an airport.

The system manages aircraft safety inspections, identified hazards, corrective actions, employee assignments, and flight information.

The database was developed using PostgreSQL and contains six main entities and one additional relationship table.

## 2. Database Structure

The database consists of seven tables:

| Table | Description |
|---|---|
| Employee | Stores information about safety department employees. |
| Airplane | Stores aircraft details, including model, manufacturer, capacity, and manufacturing year. |
| Check | Records aircraft safety inspections and their results. |
| Hazard | Stores information about identified safety hazards. |
| CorrectiveAction | Tracks corrective actions assigned to employees. |
| Flight | Stores flight information associated with aircraft. |
| Identifies | Connects safety inspections with identified hazards. |

Primary keys and foreign keys are used to maintain relationships and referential integrity.

JSONB fields are used to store additional inspection results and hazard details.

## 3. Database Design and Normalization

The database design process included:

- Creating an Entity-Relationship Diagram (ERD).
- Identifying functional dependencies.
- Analyzing normalization according to 3NF and BCNF.
- Creating the relational schema using SQL.
- Generating a Database Schema Diagram (DSD).

## 4. Data Generation and Population

The database was populated with synthetic data using three different methods:

1. **Mockaroo:** Employee records were generated using Mockaroo and imported into PostgreSQL through CSV.
2. **Excel / CSV:** Aircraft records were generated using Excel formulas and imported into PostgreSQL.
3. **Python:** Python scripts were used to generate flight, inspection, and hazard data. The `psycopg` library was also used to insert corrective actions and inspection-hazard relationships directly into PostgreSQL.

### Record Counts

| Table | Number of Records |
|---|---:|
| Employee | 60 |
| Airplane | 120 |
| Flight | 700 |
| Check | 650 |
| Hazard | 550 |
| CorrectiveAction | 600 |
| Identifies | 750 |
| **Total** | **3,430** |

## 5. Data Integrity Verification

SQL queries were executed to verify record counts and referential integrity.

The verification included relationships between:

- Flights and airplanes.
- Safety inspections, employees, and airplanes.
- Corrective actions, employees, and hazards.
- Safety inspections and identified hazards.

All four referential integrity checks returned zero invalid references.

## 6. Database Backup and Restoration

A full database backup was created using pgAdmin in PostgreSQL Custom format.

**Backup file:** `EFRAT_backup.backup`

To verify the backup, it was restored into a separate database named `EFRAT_restore_test`.

The restoration completed successfully, and SQL queries confirmed that all seven tables and 3,430 records were restored.

## 7. Technologies Used

- PostgreSQL
- pgAdmin
- Docker
- Python
- SQL
- Microsoft Excel
- Mockaroo
- Git and GitHub

## 8. Project Files

- `init-db/01-schema.sql` – SQL script for creating the database tables.
- `init-db/scripts/` – Python scripts for generating and inserting data.
- `init-db/*.csv` – Generated CSV datasets.
- `backups/EFRAT_backup.backup` – Database backup file.

Database credentials are stored locally in a `.env` file and must not be committed to GitHub.