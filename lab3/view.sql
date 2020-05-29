DROP VIEW countries_owe;
DROP VIEW region_loans_by_time;   
DROP VIEW money_by_time;

CREATE VIEW countries_owe AS
    SELECT
        country.country_id
        ,country_name
        ,amount
    FROM
        country
        JOIN countryprojectbridge 
            ON countryprojectbridge.country_id = country.country_id
        JOIN project 
            ON countryprojectbridge.project_id = project.project_id
        JOIN projectloanbridge 
            ON projectloanbridge.project_id = project.project_id
        JOIN loan 
            ON projectloanbridge.loan_id = loan.loan_id;
            
CREATE VIEW region_loans_by_time AS
    SELECT
        region.region_id
        ,region.region_name
        ,loan.approval_date
        ,amount
    FROM
        country
        JOIN countryprojectbridge 
            ON countryprojectbridge.country_id = country.country_id
        JOIN project 
            ON countryprojectbridge.project_id = project.project_id
        JOIN projectloanbridge 
            ON projectloanbridge.project_id = project.project_id
        JOIN loan 
            ON projectloanbridge.loan_id = loan.loan_id
        JOIN region
            ON region.region_id = country.region_id;
            
CREATE VIEW money_by_time AS
    SELECT
        approval_date
        ,amount
    FROM
        loan;





