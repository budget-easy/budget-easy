import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# import modules to adress environment variables
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os

def to_sql(df):
    """write df to sql"""
    table_name = 'keywords'
    
    # sqlalchemy engine for writing data to a database
    engine = create_engine(f'postgresql+psycopg2://{os.getenv("user")}:{os.getenv("password")}@{os.getenv("host")}:{os.getenv("port")}/{os.getenv("database")}',
                        connect_args={'options': '-csearch_path={}'.format(os.getenv("schema"))})

    if engine!=None:
        try:
            df.to_sql(name=table_name, # Name of SQL table
                            con=engine, # Engine or connection
                            if_exists='replace', # Drop the table before inserting new values 
                            schema='capstone_group2', # Use schmea that was defined earlier
                            index=False, # Write DataFrame index as a column
                            chunksize=5000, # Specify the number of rows in each batch to be written at a time
                            method='multi') # Pass multiple values in a single INSERT clause
            print(f"The {table_name} were imported successfully.")
        # Error handling
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            engine = None