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

-- Update the email field with random emails and domains
UPDATE niyitest -- Remember to change this to your table name please.
SET email = random_string(10) || '@' || random_domain();