import pandas as pd
import cx_Oracle


db_conn = cx_Oracle.connect(user="system", password="system")
db = db_conn.cursor()

needed_columns = [
                'regionname'
                ,'countryname'
                ,'status'
                ,'project_name'
                ,'boardapprovaldate'
                ,'totalamt'
                ]
data = pd.read_csv('data.csv')
data = data[needed_columns]

db.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD'")
db.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD'")
db.execute('DELETE FROM REGION')
db.execute('DELETE FROM COUNTRYPROJECTBRIDGE')
db.execute('DELETE FROM PROJECTLOANBRIDGE')
db.execute('DELETE FROM COUNTRY')
db.execute('DELETE FROM PROJECT')
db.execute('DELETE FROM LOAN')
db_conn.commit()

data['totalamt'] = data['totalamt'].str.replace(",","").astype(float)
data['totalamt'] = data['totalamt'].fillna(0)

for index, row in data.head(2500).iterrows():
    region_id = db.execute("SELECT region_id FROM Region where TRIM(region_name) = :region_name", region_name=row['regionname']).fetchall()
    if not region_id:
        region_id = db.execute("SELECT NVL(MAX(region_id)+1,1) FROM Region").fetchall()[0][0]
        db.execute("INSERT INTO REGION (REGION_ID, REGION_NAME) VALUES (:region_id, :region_name)", region_id=region_id, region_name = row['regionname'])
    else:
        region_id = region_id[0][0]
    
    country_id = db.execute("SELECT country_id FROM Country where TRIM(country_name) = :country_name", country_name=row['countryname']).fetchall()
    if not country_id:
        country_id = db.execute("SELECT NVL(MAX(country_id)+1,1) FROM Country").fetchall()[0][0]
        db.execute("INSERT INTO COUNTRY (COUNTRY_ID, COUNTRY_NAME, REGION_ID) VALUES (:country_id, :country_name, :region_id)", country_id=country_id, country_name=row['countryname'], region_id=region_id)
    else:
        country_id = country_id[0][0]
    
    project_id = db.execute("SELECT NVL(MAX(project_id)+1,1) FROM Project").fetchall()[0][0]
    loan_id = db.execute("SELECT NVL(MAX(loan_id)+1,1) FROM Loan").fetchall()[0][0]
    db.execute("INSERT INTO project (project_id, project_name) VALUES (:project_id, :project_name)", project_id=project_id, project_name=row['project_name'])
    db.execute("INSERT INTO loan (loan_id, status, amount, approval_date) VALUES (:loan_id, :status, :amount, :approval_date)", loan_id=loan_id, status=row['status'], amount=int(row['totalamt']), approval_date=row['boardapprovaldate'][0:10])
    db.execute("INSERT INTO countryprojectbridge (country_id, project_id) VALUES (:country_id, :project_id)", country_id=country_id, project_id=project_id)
    db.execute("INSERT INTO projectloanbridge (project_id, loan_id) VALUES (:project_id, :loan_id)", project_id=project_id, loan_id=loan_id)
    db_conn.commit()
