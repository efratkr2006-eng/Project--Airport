# Airport Safety Management System

## Contents

1. [Project Overview](#1-project-overview)
2. [Database Structure](#2-database-structure)
3. [Database Design and Normalization](#3-database-design-and-normalization)
4. [Data Generation and Population](#4-data-generation-and-population)
5. [Data Integrity Verification](#5-data-integrity-verification)
6. [Database Backup and Restoration](#6-database-backup-and-restoration)
7. [Technologies Used](#7-technologies-used)
8. [Project Files](#8-project-files)
9. [System UI Prototype](#9-system-ui-prototype)
10. [Entity Relationship Diagram](#10-entity-relationship-diagram)
11. [Database Structure Diagram (DSD)](#11-database-structure-diagram-dsd)
12. [Stage 1 Documentation](#12-stage-1-documentation)
13. [Functional Dependencies and Normalization](#13-functional-dependencies-and-normalization)

## 1. Project Overview

This project designs and implements a PostgreSQL database for the Safety Department of an airport. The system manages aircraft safety inspections, identified hazards, corrective actions, employee assignments, and flight information.

The design comprises **six main entity tables**, **one relationship table** (`Identifies`), and **one supporting lookup table** (`AirplaneModel`): eight tables in total. The additional lookup table was introduced during normalization.

## 2. Database Structure

| Table | Description |
|---|---|
| Employee | Safety department employees. |
| AirplaneModel | Aircraft models and their manufacturers. |
| Airplane | Individual aircraft, their capacity, manufacturing year, model, and unique registration number. |
| Check | Aircraft safety inspections and structured inspection results. |
| Hazard | Identified safety hazards and optional JSON details. |
| CorrectiveAction | Corrective actions associated with hazards and employees. |
| Flight | Flight information associated with aircraft. |
| Identifies | Relationship between safety inspections and identified hazards. |

Primary keys, foreign keys, and a unique aircraft registration constraint support data integrity. `CheckResultJSON` and `HazardDetailsJSON` use PostgreSQL `JSONB`.

## 3. Database Design and Normalization

The design process included an ERD, conversion to a relational schema, a DSD, identification of functional dependencies, and normalization analysis through 3NF and BCNF. To eliminate the dependency `Model → Manufacturer` from `Airplane`, model/manufacturer information was placed in `AirplaneModel`, with `Airplane.Model` referencing it as a foreign key.

Full functional dependency and normalization explanations are provided in [Section 13](#13-functional-dependencies-and-normalization).

## 4. Data Generation and Population

Synthetic data was produced using three different methods:

1. **Mockaroo:** employee records exported to CSV and imported into PostgreSQL.
2. **Excel / CSV:** aircraft records generated with Excel formulas and imported into PostgreSQL. The finalized aircraft file includes unique synthetic registration numbers; model/manufacturer combinations are stored separately in `airplanemodel_data.csv`.
3. **Python:** scripts generated flight, inspection, and hazard CSV files. The `psycopg` library was also used to insert corrective actions and inspection-hazard relationships directly into PostgreSQL.

### Record Counts — Normalized Database

| Table | Number of records |
|---|---:|
| Employee | 60 |
| AirplaneModel | 5 |
| Airplane | 120 |
| Flight | 700 |
| Check | 650 |
| Hazard | 550 |
| CorrectiveAction | 600 |
| Identifies | 750 |
| **Total** | **3,435** |

The original database contained 3,430 records across seven tables. Normalization introduced five model records without removing the existing 3,430 records.

**Data-loading order:** import the five records in `init-db/airplanemodel_data.csv` into `AirplaneModel` **before** importing `init-db/airplane_data.csv` into `Airplane`, because the latter has a foreign key to the former. Other tables must likewise be populated in foreign-key order. The SQL schema file creates the tables; CSV import and Python population are separate steps.

## 5. Data Integrity Verification

SQL queries were used to verify row counts and referential integrity for flights/aircraft, inspections/employees/aircraft, corrective actions/employees/hazards, and inspection-hazard relationships. The four original referential-integrity checks returned zero invalid references.

After normalization, a further check verified that all 120 aircraft models matched the new lookup table with zero missing model matches or manufacturer mismatches. Row counts in the normalized database were verified as shown above.

## 6. Database Backup and Restoration

- **Original backup:** `backups/EFRAT_backup.backup` — created from the original seven-table database (3,430 records). It was successfully restored into a separate database named `EFRAT_restore_test`, and the restored record counts were checked.
- **Updated backup:** `backups/EFRAT_stage1_normalized.backup` — created successfully after the restored test database was normalized to eight tables (3,435 records). The normalized database's row counts were verified before backup.

The original `EFRAT` database remains unchanged; the normalized working copy is `EFRAT_restore_test`. The updated backup has been created, but a **separate restore test of this updated backup has not yet been documented**.

## 7. Technologies Used

PostgreSQL, pgAdmin, Docker, Python (`psycopg`), SQL, Microsoft Excel, Mockaroo, Git, GitHub, and Google AI Studio (UI prototype).

## 8. Project Files

- `init-db/01-schema.sql` — creates the eight normalized tables.
- `init-db/airplanemodel_data.csv` — five model/manufacturer records.
- `init-db/airplane_data.csv` — 120 aircraft records in the normalized layout.
- `init-db/scripts/` — Python generation and population scripts.
- `init-db/*.csv` — additional generated CSV datasets.
- `backups/EFRAT_backup.backup` — original backup.
- `backups/EFRAT_stage1_normalized.backup` — backup of the normalized database.
- `docs/` — ERD, DSD, UI screenshots, and Stage 1 documentation.

Database credentials are stored locally in `.env` and **must not** be committed to GitHub.

## 9. System UI Prototype

An interactive mock interface was created using Google AI Studio. It illustrates planned dashboards, safety inspections, hazard management, and corrective action tracking. **This prototype uses sample data and is not connected to PostgreSQL.** Some displayed functions are prospective features rather than implemented database fields.

### Dashboard

![Dashboard Overview](docs/Dashboard_Overview.png)

![Dashboard Details](docs/Dashboard_Details.png)

### Safety Inspections

![Inspections](docs/Inspections.png)

### Hazard Management

![Hazards](docs/Hazards.png)

### Corrective Actions

![Corrective Actions](docs/CorrectiveActions.png)

## 10. Entity Relationship Diagram

The original ERD was created using ERDPlus to show the six main entities and their relationships. The supporting `AirplaneModel` table was introduced later in relational normalization, so the original ERD and the normalized DSD are not identical.

![ERD](docs/ERD.jpeg)

## 11. Database Structure Diagram (DSD)

This DSD depicts the **updated eight-table physical schema**, including primary and foreign keys, the `AirplaneModel` relationship, and the aircraft registration field.

![Database Structure Diagram](docs/DSD.png)


## 12. Stage 1 Documentation

The following PDF provides screenshots and explanations of the data generation/import methods, integrity verification, original backup, and restoration process. It was prepared before the additional normalization step described in this README.

[View Stage 1 Documentation](docs/Stage1_Documentation.pdf)

## 13. Functional Dependencies and Normalization

### 13.1 Employee

**Relation:**

Employee(EmployeeID, FirstName, LastName, Role, HireDate)

**Primary Key:** EmployeeID

**Functional Dependency:**

EmployeeID → FirstName, LastName, Role, HireDate

**Normalization Analysis:**

- **1NF:** Each employee is uniquely identified by EmployeeID, and the attributes contain single values.

- **2NF:** The primary key consists of a single attribute, so there are no partial dependencies.

- **3NF:** Assuming no additional business-rule dependencies, all non-key attributes depend directly on EmployeeID.

- **BCNF:** Under the same assumption, EmployeeID is the determinant of every non-trivial functional dependency and is a superkey.

**Conclusion:** The Employee relation satisfies BCNF under the stated functional dependency assumptions.

### 13.2 AirplaneModel

**Relation:**

AirplaneModel(Model, Manufacturer)

**Primary Key:** Model

**Functional Dependency:**

Model → Manufacturer

**Normalization Analysis:**

- 1NF: All attributes contain atomic values.

- 2NF: The primary key consists of one attribute.

- 3NF: There are no transitive dependencies.

- BCNF: Model is a superkey and determines Manufacturer.

**Conclusion:** AirplaneModel satisfies BCNF.

### 13.3 Airplane

**Relation:**

Airplane(AirplaneID, Capacity, ManufacturingYear,

Model, RegistrationNumber)

**Primary Key:** AirplaneID

**Alternative Candidate Key:** RegistrationNumber

**Foreign Key:** Model references AirplaneModel(Model).

**Functional Dependencies:**

AirplaneID → Capacity, ManufacturingYear,

Model, RegistrationNumber

RegistrationNumber → AirplaneID, Capacity,

ManufacturingYear, Model

**Normalization Analysis:**

- 1NF: All attributes contain atomic values.

- 2NF: There are no partial dependencies.

- 3NF: There are no transitive dependencies under

  the stated business assumptions.

- BCNF: Every non-trivial functional dependency

  has a superkey as its determinant.

**Business Assumption:**

Capacity describes the seating configuration of

an individual airplane and is not necessarily

determined by its model.

**Conclusion:**

Under these business assumptions, Airplane

satisfies BCNF.

Manufacturer was moved to AirplaneModel to

eliminate the transitive dependency:

AirplaneID → Model → Manufacturer

### 13.4 Flight

**Relation:**

Flight(FlightID, FlightDate, Departure,

Destination, Duration, AirplaneID)

**Primary Key:** FlightID

**Foreign Key:** AirplaneID references Airplane(AirplaneID).

**Functional Dependency:**

FlightID → FlightDate, Departure, Destination,

Duration, AirplaneID

**Normalization Analysis:**

- 1NF: All attributes contain atomic values.

- 2NF: The primary key consists of a single attribute,

  so there are no partial dependencies.

- 3NF: There are no transitive dependencies under

  the stated business assumptions.

- BCNF: Every non-trivial functional dependency

  has a superkey as its determinant.

**Business Assumption:**

Duration represents the duration of an individual

flight and may vary between flights on the same route.

**Conclusion:**

Under these assumptions, Flight satisfies BCNF.

### 13.5 Check

**Relation:**

Check(CheckID, CheckDate, CheckType,

CheckResultJSON, NextCheckDate,

EmployeeID, AirplaneID)

**Primary Key:** CheckID

**Foreign Keys:**

- EmployeeID references Employee(EmployeeID).

- AirplaneID references Airplane(AirplaneID).

**Functional Dependency:**

CheckID → CheckDate, CheckType, CheckResultJSON,

NextCheckDate, EmployeeID, AirplaneID

**Normalization Analysis:**

- 1NF: Each row represents one safety inspection.

  The JSONB result is stored as a single attribute.

- 2NF: The primary key consists of one attribute,

  so there are no partial dependencies.

- 3NF: Under the stated business assumptions,

  there are no transitive dependencies.

- BCNF: Every non-trivial functional dependency

  has a superkey as its determinant.

**Business Assumptions:**

Each inspection has its own scheduled dates,

assigned employee, airplane, type, and results.

NextCheckDate is determined for each individual

inspection and is not necessarily determined

by CheckType alone.

**Conclusion:**

Under these assumptions, Check satisfies BCNF.

### 13.6 Hazard

**Relation:**

Hazard(HazardID, HazardType, RiskLevel,

Location, HazardDetailsJSON)

**Primary Key:** HazardID

**Functional Dependency:**

HazardID → HazardType, RiskLevel,

Location, HazardDetailsJSON

**Normalization Analysis:**

- 1NF: Each row represents one hazard.

  The JSONB field is treated as a single

  structured attribute in PostgreSQL.

- 2NF: The primary key consists of one

  attribute, so there are no partial dependencies.

- 3NF: There are no transitive dependencies

  under the stated business assumptions.

- BCNF: Every non-trivial functional dependency

  has a superkey as its determinant.

**Business Assumptions:**

RiskLevel is assigned to each individual hazard

and is not necessarily determined by HazardType.

Location represents the location of the specific

hazard and does not determine its other attributes.

HazardDetailsJSON contains additional information

about the hazard and is not used to duplicate

relational keys or create hidden dependencies.

**Conclusion:**

Under these assumptions, Hazard satisfies BCNF.

### 13.7 CorrectiveAction

**Relation:**

CorrectiveAction(ActionID, ActionDescription,

RecoveryTime, State, Duration, HazardID, EmployeeID)

**Primary Key:** ActionID

**Foreign Keys:**

- HazardID references Hazard(HazardID).

- EmployeeID references Employee(EmployeeID).

**Functional Dependency:**

ActionID → ActionDescription, RecoveryTime,

State, Duration, HazardID, EmployeeID

**Normalization Analysis:**

- 1NF: Each row represents one corrective action,

  and its attributes contain atomic values.

- 2NF: The primary key consists of one attribute,

  so there are no partial dependencies.

- 3NF: There are no transitive dependencies

  under the stated business assumptions.

- BCNF: Every non-trivial functional dependency

  has a superkey as its determinant.

**Business Assumptions:**

Each corrective action has its own description,

duration, recovery time, and current state.

Different corrective actions may be assigned to

the same employee or address the same hazard.

Neither EmployeeID nor HazardID alone determines

the other attributes of a corrective action.

**Conclusion:**

Under these assumptions, CorrectiveAction

satisfies BCNF.

### 13.8 Identifies

**Relation:**

Identifies(CheckID, HazardID)

**Composite Primary Key:** (CheckID, HazardID)

**Foreign Keys:**

- CheckID references Check(CheckID).

- HazardID references Hazard(HazardID).

**Functional Dependency:**

(CheckID, HazardID) → All attributes of Identifies

The composite key uniquely identifies each

inspection-hazard relationship.

**Normalization Analysis:**

- 1NF: Each row contains one CheckID and one

  HazardID, both holding atomic values.

- 2NF: There are no non-key attributes that

  could depend on only part of the composite key.

- 3NF: There are no transitive dependencies.

- BCNF: The composite key is a superkey, and

  there are no non-trivial functional dependencies

  with a non-superkey determinant.

**Business Assumptions:**

One inspection may identify several hazards,

and one hazard may be identified by several

inspections.

The combination of CheckID and HazardID is

unique, preventing duplicate relationships.

**Conclusion:**

Identifies satisfies BCNF.

### 13.9 Overall Normalization Summary

All eight relations were analyzed for functional

dependencies and normalization.

Under the documented business assumptions,

all relations satisfy BCNF and therefore also 3NF.

The Airplane relation was decomposed into

Airplane and AirplaneModel to eliminate the

transitive dependency:

AirplaneID → Model → Manufacturer

This decomposition reduces data redundancy

and helps prevent update anomalies.
