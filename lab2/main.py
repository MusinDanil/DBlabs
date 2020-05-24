import cx_Oracle

db_conn = cx_Oracle.connect(user="system", password="system")

db = db_conn.cursor()

db.execute("""
                ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD'
                """)

print("\nCумарна заборгованість країн у порядку спадання:\n")

temp = db.execute("""
SELECT 
          COUNTRY.COUNTRY_NAME
         ,SUM(AMOUNT)
FROM PROJECT 
            INNER JOIN LOAN ON LOAN.PROJECT_ID = PROJECT.PROJECT_ID
            INNER JOIN COUNTRY ON COUNTRY.COUNTRY_ID = PROJECT.COUNTRY_ID
GROUP BY COUNTRY.COUNTRY_NAME
ORDER BY SUM(AMOUNT) DESC
""")

for row in temp:
    print(row)

print("\nНещодавно відкриті позики кожного регіону кожного регіону:\n")

temp = db.execute("""
SELECT
             COUNTRY.REGION_NAME
            ,MAX(BOARD_APPROVAL_DATE)
            ,SUM(AMOUNT)
FROM PROJECT 
            INNER JOIN LOAN ON LOAN.PROJECT_ID = PROJECT.PROJECT_ID
            INNER JOIN COUNTRY ON COUNTRY.COUNTRY_ID = PROJECT.COUNTRY_ID
WHERE BOARD_APPROVAL_DATE > '2017-01-01'
GROUP BY COUNTRY.REGION_NAME
""")

for row in temp:
    print(row)

print("\nПозики по часу:\n")

temp = db.execute("""
SELECT 
         BOARD_APPROVAL_DATE
        ,SUM(AMOUNT)
FROM 
        LOAN
GROUP BY BOARD_APPROVAL_DATE
ORDER BY BOARD_APPROVAL_DATE DESC
""")

for row in temp:
    print(row)