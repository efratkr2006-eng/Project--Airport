# Airport Safety Management System — Stage A System Specification and Data Dictionary

**System:** Airport Safety Management System (AeroSafe Operations prototype)
**Department:** Airport Safety Department
**Students:** [ADD STUDENT 1 NAME AND ID] / [ADD STUDENT 2 NAME AND ID]
**Stage:** A — Design, implementation, data population and backup
**Updated:** 2026-11-24

## 1. Purpose and scope

The proposed system supports safety staff in recording aircraft inspections, identifying hazards, assigning corrective actions, and viewing aircraft and flight information. The current deliverable is a PostgreSQL database plus an interactive Google AI Studio **UI prototype with sample data**; the prototype is not connected to PostgreSQL.

## 2. Top-down screen specification

| Screen | Information displayed | Main operations envisioned | Related tables |
|---|---|---|---|
| Dashboard | Recent inspections, active hazards, corrective actions, aircraft overview | Navigate to detailed records; review a summary | CHECK, Hazard, CorrectiveAction, Airplane |
| Inspections | Check ID, dates, inspection type, result, assigned employee and airplane | Search/filter and view inspection details | CHECK, Employee, Airplane |
| Hazards | Hazard ID, type, risk level, location, further information and related checks | Search/filter and view identified hazards | Hazard, Identifies, CHECK |
| Corrective Actions | Action ID, description, state, duration, recovery time, assigned employee and hazard | Track action information and status | CorrectiveAction, Employee, Hazard |

**Prototype link:** [ADD GOOGLE AI STUDIO SHARE LINK — not provided yet].

*The prototype contains planned features and sample values. Do not treat every UI widget as an implemented database column.*

## 3. Design: entities and tables

Six core entities were modeled: Employee, Airplane, Flight, CHECK, Hazard, CorrectiveAction. `Identifies` is a relationship table between inspections and hazards; `AirplaneModel` is a lookup/support table introduced during normalization. The physical schema therefore has **eight tables**.

**ERD and DSD:** The original ERD diagram and normalized DSD are in the Screenshots folder. Because `AirplaneModel` was added after the original conceptual ERD, verify that the submitted **ERD source** is updated to match the final schema, as required by the lecturer. A screenshot alone is not the editable ERDPlus source.

## 4. Detailed data dictionary

The following types, NULL rules and keys reflect the supplied `createTables.sql` schema.

### Employee — employees in the safety department

| Column | SQL type | Constraints | Meaning |
|---|---|---|---|
| EmployeeID | INT | PK, NOT NULL | Unique employee identifier |
| FirstName | VARCHAR(50) | NOT NULL | First name |
| LastName | VARCHAR(50) | NOT NULL | Last name |
| Role | VARCHAR(60) | NOT NULL | Position or responsibility |
| HireDate | DATE | NOT NULL | Employment start date |

**Relations:** Referenced by `CHECK.EmployeeID` and `CorrectiveAction.EmployeeID`.

### AirplaneModel — aircraft model lookup

| Column | SQL type | Constraints | Meaning |
|---|---|---|---|
| Model | VARCHAR(100) | PK, NOT NULL | Unique model code |
| Manufacturer | VARCHAR(100) | NOT NULL | Model manufacturer |

**Relations:** One model can be referenced by many airplanes.

### Airplane — individual aircraft

| Column | SQL type | Constraints | Meaning |
|---|---|---|---|
| AirplaneID | INT | PK, NOT NULL | Aircraft identifier |
| Capacity | INT | NOT NULL | Seating capacity of this aircraft |
| ManufacturingYear | INT | NOT NULL | Aircraft manufacture year |
| Model | VARCHAR(100) | FK, NOT NULL | References AirplaneModel(Model) |
| RegistrationNumber | VARCHAR(30) | NOT NULL, UNIQUE | Synthetic unique aircraft registration |

**Relations:** Referenced by `CHECK.AirplaneID` and `Flight.AirplaneID`.

### CHECK — aircraft safety inspections

| Column | SQL type | Constraints | Meaning |
|---|---|---|---|
| CheckID | INT | PK, NOT NULL | Inspection identifier |
| CheckDate | DATE | NOT NULL | Date of inspection |
| CheckType | VARCHAR(80) | NOT NULL | Inspection category |
| CheckResultJSON | JSONB | NOT NULL | Structured inspection results |
| NextCheckDate | DATE | NOT NULL | Planned next inspection |
| EmployeeID | INT | FK, NOT NULL | References Employee(EmployeeID) |
| AirplaneID | INT | FK, NOT NULL | References Airplane(AirplaneID) |

**Relations:** One employee can conduct many checks; one aircraft can undergo many checks. Linked to Hazard via `Identifies`.

### Hazard — identified safety hazards

| Column | SQL type | Constraints | Meaning |
|---|---|---|---|
| HazardID | INT | PK, NOT NULL | Hazard identifier |
| HazardType | VARCHAR(80) | NOT NULL | Hazard category |
| RiskLevel | VARCHAR(30) | NOT NULL | Risk classification |
| Location | VARCHAR(120) | NOT NULL | Where the hazard was identified |
| HazardDetailsJSON | JSONB | NULL allowed | Optional structured details |

**Relations:** Referenced by `CorrectiveAction.HazardID` and `Identifies.HazardID`.

### CorrectiveAction — work to resolve hazards

| Column | SQL type | Constraints | Meaning |
|---|---|---|---|
| ActionID | INT | PK, NOT NULL | Unique action identifier |
| ActionDescription | TEXT | NOT NULL | Action description |
| RecoveryTime | INT | NOT NULL | Recovery-time value |
| State | VARCHAR(30) | NOT NULL | Current action state |
| Duration | INT | NOT NULL | Duration value |
| HazardID | INT | FK, NOT NULL | References Hazard(HazardID) |
| EmployeeID | INT | FK, NOT NULL | References Employee(EmployeeID) |

**Relations:** A hazard and an employee may be referenced by multiple corrective actions.

### Flight — scheduled/recorded flights

| Column | SQL type | Constraints | Meaning |
|---|---|---|---|
| FlightID | INT | PK, NOT NULL | Flight identifier |
| FlightDate | DATE | NOT NULL | Flight date |
| Departure | VARCHAR(100) | NOT NULL | Departure location |
| Destination | VARCHAR(100) | NOT NULL | Destination |
| Duration | INT | NOT NULL | Flight duration |
| AirplaneID | INT | FK, NOT NULL | References Airplane(AirplaneID) |

**Relations:** A single airplane can be referenced by multiple flights.

### Identifies — inspection–hazard relationship

| Column | SQL type | Constraints | Meaning |
|---|---|---|---|
| CheckID | INT | Composite PK, FK, NOT NULL | References CHECK(CheckID) |
| HazardID | INT | Composite PK, FK, NOT NULL | References Hazard(HazardID) |

**Relations:** Joins checks and hazards; the combined `(CheckID, HazardID)` is unique.

## 5. Constraints and normalization rationale

**Implemented constraints:** primary keys, foreign keys, `NOT NULL` and aircraft `UNIQUE (RegistrationNumber)`. Additional real-world validation rules, for example valid manufacturing years and positive durations, are **not currently asserted** in the supplied `CREATE TABLE` code. If the lecturer requires more business checks, implement/test those separately rather than claiming they exist.

**Normalization:** Initially, `AirplaneID → Model → Manufacturer` introduced a transitive dependency under the business rule `Model → Manufacturer`. Moving the manufacturer into `AirplaneModel` and referencing its model code removes the redundancy. Under the business assumptions documented in the root README (for example, aircraft seating capacity may vary for a single model), the eight relations were analyzed as BCNF. The database's current rows alone do not prove arbitrary future functional dependencies.

**Meaningful dates:** HireDate, FlightDate, CheckDate and NextCheckDate are stored as SQL DATE values.

## 6. Known documentation and scope boundaries

- The system UI is a non-connected prototype.
- The editable original ERDPlus file must be added or updated if it is not already among the project files.
- The lecturer specifies **500 records per table**, and `AirplaneModel` currently has **5** model rows. Confirm whether this lookup table qualifies for an exemption; do not invent 495 fictitious model identifiers without clarification.
- A restore was tested successfully from the older backup on the same computer, and create + inserts were tested on a fresh local database with 42,905 records. The lecturer additionally requires an actual **restore on another computer**; that evidence is not yet established.
- Student identifying details and the Google AI Studio share URL still need to be entered by the students.
