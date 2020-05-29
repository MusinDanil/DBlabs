import pandas as pd

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

print(data.head(5))