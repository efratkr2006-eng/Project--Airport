
-- Airport Safety Management System
-- Stage 1: Database Schema

-- 1. EMPLOYEE
CREATE TABLE EMPLOYEE (
    EmployeeID INT NOT NULL,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Role VARCHAR(60) NOT NULL,
    HireDate DATE NOT NULL,
    PRIMARY KEY (EmployeeID)
);

-- 2. AIRPLANE
CREATE TABLE AIRPLANE (
    AirplaneID INT NOT NULL,
    Capacity INT NOT NULL,
    ManufacturingYear INT NOT NULL,
    Model VARCHAR(100) NOT NULL,
    Manufacturer VARCHAR(100) NOT NULL,
    PRIMARY KEY (AirplaneID)
);

-- 3. CHECK
CREATE TABLE "CHECK" (
    CheckID INT NOT NULL,
    CheckDate DATE NOT NULL,
    CheckType VARCHAR(80) NOT NULL,
    CheckResultJSON JSONB NOT NULL,
    NextCheckDate DATE NOT NULL,
    EmployeeID INT NOT NULL,
    AirplaneID INT NOT NULL,
    PRIMARY KEY (CheckID),
    FOREIGN KEY (EmployeeID)
        REFERENCES EMPLOYEE(EmployeeID),
    FOREIGN KEY (AirplaneID)
        REFERENCES AIRPLANE(AirplaneID)
);

-- 4. HAZARD
CREATE TABLE HAZARD (
    HazardID INT NOT NULL,
    HazardType VARCHAR(80) NOT NULL,
    RiskLevel VARCHAR(30) NOT NULL,
    Location VARCHAR(120) NOT NULL,
    HazardDetailsJSON JSONB,
    PRIMARY KEY (HazardID)
);

-- 5. CORRECTIVEACTION
CREATE TABLE CORRECTIVEACTION (
    ActionID INT NOT NULL,
    ActionDescription TEXT NOT NULL,
    RecoveryTime INT NOT NULL,
    State VARCHAR(30) NOT NULL,
    Duration INT NOT NULL,
    HazardID INT NOT NULL,
    EmployeeID INT NOT NULL,
    PRIMARY KEY (ActionID),
    FOREIGN KEY (HazardID)
        REFERENCES HAZARD(HazardID),
    FOREIGN KEY (EmployeeID)
        REFERENCES EMPLOYEE(EmployeeID)
);

-- 6. FLIGHT
CREATE TABLE FLIGHT (
    FlightID INT NOT NULL,
    FlightDate DATE NOT NULL,
    Departure VARCHAR(100) NOT NULL,
    Destination VARCHAR(100) NOT NULL,
    Duration INT NOT NULL,
    AirplaneID INT NOT NULL,
    PRIMARY KEY (FlightID),
    FOREIGN KEY (AirplaneID)
        REFERENCES AIRPLANE(AirplaneID)
);

-- 7. IDENTIFIES
CREATE TABLE IDENTIFIES (
    CheckID INT NOT NULL,
    HazardID INT NOT NULL,
    PRIMARY KEY (CheckID, HazardID),
    FOREIGN KEY (CheckID)
        REFERENCES "CHECK"(CheckID),
    FOREIGN KEY (HazardID)
        REFERENCES HAZARD(HazardID)
);
