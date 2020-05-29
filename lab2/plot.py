import cx_Oracle
import chart_studio.plotly as py
import plotly.graph_objects as go
import chart_studio.dashboard_objs as dashboard
import re
from plotly.subplots import make_subplots
import chart_studio

username = input('Enter your user_name')
api_key = input('Enter your api_key')
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

def fileId_from_url(url):

    """Return fileId from a url."""

    raw_fileId = re.findall("~[A-z.]+/[0-9]+", url)[0][1: ]

    return raw_fileId.replace('/', ':')

db_conn = cx_Oracle.connect(user="system", password="system")

db = db_conn.cursor()

db.execute("""
                ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD'
                """)

first = db.execute("""
SELECT 
          COUNTRY.COUNTRY_NAME
         ,SUM(AMOUNT)
FROM PROJECT 
            INNER JOIN LOAN ON LOAN.PROJECT_ID = PROJECT.PROJECT_ID
            INNER JOIN COUNTRY ON COUNTRY.COUNTRY_ID = PROJECT.COUNTRY_ID
GROUP BY COUNTRY.COUNTRY_NAME
ORDER BY SUM(AMOUNT) DESC
""")

fig =  make_subplots(rows=2, cols=2,
                    specs=[[{"type": "xy"}, {"type": "xy"}],
                    [{"type": "domain"}, {"type": "xy"}]])

y, x = [], []
for row in first:
    y.append(row[1])
    x.append(row[0])

countries_loan = py.plot([go.Bar(y = y, x = x)], filename='countries loan file')

second = db.execute("""
SELECT
             COUNTRY.REGION_NAME
            ,SUM(AMOUNT)
FROM PROJECT 
            INNER JOIN LOAN ON LOAN.PROJECT_ID = PROJECT.PROJECT_ID
            INNER JOIN COUNTRY ON COUNTRY.COUNTRY_ID = PROJECT.COUNTRY_ID
WHERE BOARD_APPROVAL_DATE > '2017-01-01'
GROUP BY COUNTRY.REGION_NAME
""")

labels, values = [], []
for row in second:
    labels.append(row[0])
    values.append(row[1])
world_parts_investmets = py.plot([go.Pie(labels=labels, values=values)], filename='world parts investments')

third = db.execute("""
SELECT 
         BOARD_APPROVAL_DATE
        ,SUM(AMOUNT)
FROM 
        LOAN
GROUP BY BOARD_APPROVAL_DATE
ORDER BY BOARD_APPROVAL_DATE DESC
""")

y, x = [], []
for row in third:
    y.append(row[1])
    x.append(row[0])

loans_by_time =  py.plot([go.Scatter(y = y, x = x)], filename='loans by time')

my_dboard = dashboard.Dashboard()

countries_loan_id = fileId_from_url(countries_loan)
world_parts_investmets_id = fileId_from_url(world_parts_investmets)
loans_by_time_id = fileId_from_url(loans_by_time)
box_1 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': countries_loan_id,
    'title': 'Countries loans'
}
 
box_2 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': world_parts_investmets_id,
    'title': 'World parts debts'
}
 
box_3 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': loans_by_time_id,
    'title': 'Loans by time'
}

my_dboard.insert(box_1)
my_dboard.insert(box_2, 'below', 1)
my_dboard.insert(box_3, 'left', 2)
 
py.dashboard_ops.upload(my_dboard, 'My dashboard')
