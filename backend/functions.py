# This file contains the functions that are used commonly in the Jupyter notebooks

import pycountry
import sqlite3


def country_to_iso(country_name):
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except LookupError:
        return None
    


def df_to_database(df, tableName):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('./data/countryDatabase.db')
        df.to_sql(tableName, conn, if_exists='replace', index=False)
        # Close the connection
        conn.commit()
        conn.close()
        return 'Success.'
    except:
        return 'Failed to write to database.'

