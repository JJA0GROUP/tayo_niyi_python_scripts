from sqlalchemy import create_engine
import pandas as pd
import time

# Please make sure you install sqlalchemy and psycopg2-binary before running this code
# You can use command "pip install SQLAlchemy psycopg2-binary" for the above installation

class Pipeline:
    """This class is responsible for creating new table, appending new row and updating values in sql table from an Excel file"""
    
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.engine = create_engine("postgresql+psycopg2://<username>:<password>@<remote_host>:<port>/<database_name>")
        self.conn = self.engine.connect()

        
    def updateSqlValues(self):
        #This method updates column Location values on sql table from excel file
        
        employee_data = pd.read_csv(f'{self.csv_file}')
        employee_data.to_sql("test_table", self.conn, if_exists="replace", index=False)

        sql = """UPDATE 
         niyitest ed
         JOIN test_table tt
         ON ed.id = tt.id     
         SET ed.email = tt.email
         WHERE tt.email <> ed.email;"""

        drop_sql = """DROP TABLE test_table;"""

        #with engine.begin() as conn:     # TRANSACTION
        #conn.execute(sql)

        self.conn.execute(sql)
        self.conn.execute(drop_sql)
        
        
p = Pipeline('NiyiTest_modified.csv')
p.updateSqlValues()