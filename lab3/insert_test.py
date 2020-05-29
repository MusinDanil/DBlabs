import cx_Oracle

test_chunk_size = 5

db_conn = cx_Oracle.connect(user="system", password="system")

db = db_conn.cursor()

print(db.execute('select * from region'))
db.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD'")
db.execute('DELETE FROM REGION')
db.execute('DELETE FROM COUNTRYPROJECTBRIDGE')
db.execute('DELETE FROM PROJECTLOANBRIDGE')
db.execute('DELETE FROM COUNTRY')
db.execute('DELETE FROM PROJECT')
db.execute('DELETE FROM LOAN')
db_conn.commit()

db.execute("INSERT INTO REGION (REGION_ID, REGION_NAME) VALUES (1, 'East Asia and Pacific')")
db.execute("INSERT INTO COUNTRY (COUNTRY_ID, REGION_ID, COUNTRY_NAME) VALUES (1 , 1, 'Republic of the Marshall Islands')")
db.execute("INSERT INTO PROJECT (PROJECT_ID, PROJECT_NAME, CLOSING_DATE) VALUES (1 , 'Local Development Support Project','1998-12-09')")
db.execute("INSERT INTO LOAN (LOAN_ID, STATUS, AMOUNT, APPROVAL_DATE) VALUES (1 ,  'act',35000000 ,'1998-12-09')")
db.execute("INSERT INTO countryprojectbridge (COUNTRY_ID, PROJECT_ID) VALUES (1, 1)")
db.execute("INSERT INTO projectloanbridge (LOAN_ID, PROJECT_ID) VALUES (1, 1)")
db_conn.commit()

db.close()