import pandas as pd
import cx_Oracle
import csv

db_conn = cx_Oracle.connect(user="system", password="system")
db = db_conn.cursor()

def save_table(arg):
    db.execute('select * FROM ' + arg)
    with open('export_csv/' + arg + '.csv', 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow([ i[0] for i in db.description ])
        writer.writerows(db.fetchall())


save_table('Region')
save_table('Country')
save_table('Project')
save_table('Loan')
save_table('Projectloanbridge')
save_table('Countryprojectbridge')

db_conn.close()



