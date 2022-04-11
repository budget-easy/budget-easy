import pandas as pd
import psycopg2
from sqlalchemy import create_engine

from budget_easy.bing_api import get_bing_data
from budget_easy.google_api import get_google_data

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


def get_sql_data(query):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # create a connection to the PostgreSQL server
        conn = create_engine(f'postgresql+psycopg2://{os.getenv("user")}:{os.getenv("password")}@{os.getenv("host")}:{os.getenv("port")}/{os.getenv("database")}',
                        connect_args={'options': '-csearch_path={}'.format(os.getenv("schema"))})
		
        # create a cursor
        return pd.read_sql_query(query, conn)

    # the code below makes the function more robust, you can ignore this part
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_data(keyword, page_url, country):
    """get data from Google and Bing APIs and write it to sql
    required: keyword(s), page_url, country"""
    # get location codes for country
    location = get_sql_data(f"SELECT bing_location_id, google_location_id FROM locations WHERE canonical_name = '{country}'")
    
    # get google and bing data
    google = get_google_data(keyword,page_url,str(location['google_location_id'][0]))
    
    bing = get_bing_data(keyword,page_url ,str(location['bing_location_id'][0]))
    #bing = ''
    
    if isinstance(bing, pd.DataFrame):
        to_sql(pd.concat([google, bing]))
    else:
        to_sql(google)
        print('No bing data!')