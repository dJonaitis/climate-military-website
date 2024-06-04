# This file converts the database to a CSV file
import sqlite3
from pathlib import Path

import pandas as pd
import os



PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

DATABASE = os.path.join(PROJECT_ROOT, 'user_tracking', 'userTracking.db')
conn = sqlite3.connect(DATABASE)

query_time = "SELECT * FROM PageView"
query_form = "SELECT * FROM TransferYear"

# read_sql_query reads SQL queries into pandas DataFrames.
# "df_table_time" and "df_table_button" are DataFrame variables.

df_table_time = pd.read_sql_query(query_time, conn)
df_table_form = pd.read_sql_query(query_form, conn)

# to_csv saves the DataFrame in a csv file.
# After running this programme, two .csv files are generated in the same directory: "table_time.csv" and "table_button.csv".

df_table_time.to_csv("table_time.csv", index=False)
df_table_form.to_csv("table_form.csv", index=False)
