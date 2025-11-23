-- Function that checks class capacity before registration
CREATE OR REPLACE FUNCTION check_class_capacity()
RETURNS TRIGGER AS $$
DECLARE
    class_capacity INTEGER;
    current_registrations INTEGER;
BEGIN
    -- Get the capacity of the class
    SELECT capacity INTO class_capacity
    FROM group_class
    WHERE class_id = NEW.class_id;
    
    -- Count current registrations for this class
    SELECT COUNT(*) INTO current_registrations
    FROM class_registration
    WHERE class_id = NEW.class_id;
    
    -- Check if class is full
    IF current_registrations >= class_capacity THEN
        RAISE EXCEPTION 'Class is full. Capacity: %, Current registrations: %', 
            class_capacity, current_registrations;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger that fires before insert on class_registration
CREATE TRIGGER prevent_class_overbooking
    BEFORE INSERT ON class_registration
    FOR EACH ROW
    EXECUTE FUNCTION check_class_capacity();