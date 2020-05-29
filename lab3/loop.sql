DECLARE
    test_size INT DEFAULT 10;
BEGIN
    FOR i in 4..test_size LOOP
        INSERT INTO Region(region_id, region_name) VALUES(i-1, CONCAT('Test_Region',i));
    END LOOP;
END;