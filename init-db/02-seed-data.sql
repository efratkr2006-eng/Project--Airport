
-- Add employees until the table contains 500 rows.
-- Preserve the original 60 Mockaroo employees.

INSERT INTO public.employee
    (employeeid, firstname, lastname, role, hiredate)
SELECT
    n,
    'Employee' || n,
    'Demo' || n,
    CASE n % 4
        WHEN 0 THEN 'Safety Inspector'
        WHEN 1 THEN 'Safety Officer'
        WHEN 2 THEN 'Technician'
        ELSE 'Supervisor'
    END,
    DATE '2018-01-01' + ((n * 17) % 2800)
FROM generate_series(61, 500) AS g(n)
ON CONFLICT (employeeid) DO NOTHING;


-- Add airplanes 121-500
-- Keep the existing 120 airplanes

INSERT INTO public.airplane
    (airplaneid, capacity, manufacturingyear,
     model, registrationnumber)
SELECT
    n,
    CASE (n - 1) % 5
        WHEN 0 THEN 180
        WHEN 1 THEN 220
        WHEN 2 THEN 189
        WHEN 3 THEN 290
        ELSE 132
    END,
    2019 + ((n - 1) % 8),
    CASE (n - 1) % 5
        WHEN 0 THEN 'A320'
        WHEN 1 THEN 'A321'
        WHEN 2 THEN '737-800'
        WHEN 3 THEN '787-9'
        ELSE 'E195-E2'
    END,
    'TEST-' || n
FROM generate_series(121, 500) AS g(n)
ON CONFLICT (airplaneid) DO NOTHING;


-- Add flights until there are 20,000 records
-- Preserve the existing 700 flights

DO $$
DECLARE
    existing_count INT;
    max_id INT;
BEGIN
    IF current_database() <> 'EFRAT_restore_test' THEN
        RAISE EXCEPTION 'Wrong database!';
    END IF;

    SELECT COUNT(*), COALESCE(MAX(flightid), 0)
    INTO existing_count, max_id
    FROM public.flight;

    INSERT INTO public.flight
        (flightid, flightdate, departure,
         destination, duration, airplaneid)
    SELECT
        max_id + n,
        DATE '2026-01-01' + (n % 365),
        CASE n % 5
            WHEN 0 THEN 'TLV'
            WHEN 1 THEN 'LHR'
            WHEN 2 THEN 'JFK'
            WHEN 3 THEN 'CDG'
            ELSE 'FCO'
        END,
        CASE n % 5
            WHEN 0 THEN 'LHR'
            WHEN 1 THEN 'JFK'
            WHEN 2 THEN 'CDG'
            WHEN 3 THEN 'FCO'
            ELSE 'TLV'
        END,
        120 + ((n * 13) % 480),
        1 + ((n - 1) % 500)
    FROM generate_series(
        1, GREATEST(0, 20000 - existing_count)
    ) AS g(n);
END $$;


-- Add safety checks until there are 20,000 records
-- Preserve the existing checks

DO $$
DECLARE
    existing_count INT;
    max_id INT;
BEGIN
    IF current_database() <> 'EFRAT_restore_test' THEN
        RAISE EXCEPTION 'Wrong database!';
    END IF;

    SELECT COUNT(*), COALESCE(MAX(checkid), 0)
    INTO existing_count, max_id
    FROM public."CHECK";

    INSERT INTO public."CHECK"
        (checkid, checkdate, checktype,
         checkresultjson, nextcheckdate,
         employeeid, airplaneid)
    SELECT
        max_id + n,
        DATE '2026-01-01' + (n % 365),
        CASE n % 4
            WHEN 0 THEN 'Engine Inspection'
            WHEN 1 THEN 'Safety Inspection'
            WHEN 2 THEN 'Electrical Inspection'
            ELSE 'Routine Inspection'
        END,
        jsonb_build_object(
            'status',
            CASE n % 3
                WHEN 0 THEN 'Passed'
                WHEN 1 THEN 'Warning'
                ELSE 'Failed'
            END,
            'notes', 'Generated safety check',
            'check_number', max_id + n
        ),
        DATE '2026-01-01' + (n % 365) + 90,
        1 + ((n - 1) % 500),
        1 + ((n - 1) % 500)
    FROM generate_series(
        1, GREATEST(0, 20000 - existing_count)
    ) AS g(n);
END $$;
