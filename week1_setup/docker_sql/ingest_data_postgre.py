import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    csv_name = "output1.csv"

    os.system(f"wget {url} -O {csv_name}")


    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()
    

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=1000)

    df = next(df_iter)

    #to generate a schema in order to put data into database in pandas a module named 'io' is used
    # print(pd.io.sql.get_schema(df, name='yellow_taxi_data'))


    # df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    # df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


    #will insert the header
    df.head(0).to_sql(name=table_name, con = engine, if_exists = 'replace')


    df.to_sql(name=table_name, con = engine, if_exists = 'append')


    while True:
        t_start = time()
        
        df = next(df_iter)
        # df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        # df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql(name=table_name, con = engine, if_exists = 'append')
        t_end = time()
        
        print('inserted into chunk...., took %.3f second' % (t_end - t_start))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='ingest data into postgresql')

    parser.add_argument('--user', help='take the username for postgres')
    parser.add_argument('--password', help='take the password for postgres')
    parser.add_argument('--host', help='take the host for postgres')
    parser.add_argument('--port', help='take the port for postgres')
    parser.add_argument('--db', help='take the database name for postgres')
    parser.add_argument('--table_name', help='take the tablename for postgres')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()
    main(args)
