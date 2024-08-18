-- Create a function to generate a random string
CREATE OR REPLACE FUNCTION random_string(length INT) RETURNS TEXT AS $$
DECLARE
    chars TEXT = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    result TEXT = '';
BEGIN
    FOR i IN 1..length LOOP
        result := result || substr(chars, (random() * length(chars))::int + 1, 1);
    END LOOP;
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Create a function to pick a random domain
CREATE OR REPLACE FUNCTION random_domain() RETURNS TEXT AS $$
DECLARE
    domains TEXT[] = ARRAY['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com'];
    idx INT;
BEGIN
    idx := floor(random() * array_length(domains, 1)) + 1;
    RETURN domains[idx];
END;
$$ LANGUAGE plpgsql;

-- Function to generate random first or last names
CREATE OR REPLACE FUNCTION random_name(length INT) RETURNS TEXT AS $$
DECLARE
    chars TEXT = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    result TEXT = '';
BEGIN
    FOR i IN 1..length LOOP
        result := result || substr(chars, (random() * length(chars))::int + 1, 1);
    END LOOP;
    RETURN result;
END;
$$ LANGUAGE plpgsql;


-- Update the email field with random emails and domains on email table
UPDATE niyitest -- Remember to change this to your table name please.
SET email = random_string(10) || '@' || random_domain();

-- Update first_name, last_name, and full_name on users table based on conditions
WITH ccl_names AS (
    SELECT name FROM ccl_profiles --Remember to change this to your table name please.
)
UPDATE users --Remember to change this to your table name please.
SET 
    first_name = random_name(8),
    last_name = random_name(10),
    -- full_name = random_name(8) || ' ' || random_name(10),
	email = random_string(10) || '@' || random_domain()
WHERE 
    email NOT LIKE '%@reforge.com'
    AND full_name NOT IN (SELECT name FROM ccl_names);