from fastapi import FastAPI
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, engine

region = input("Enter a region: ")
start_date = input("Enter a start date: ")
end_date = input("Enter an end date: ")

def get_postgresql_conn():
    connection = psycopg2.connect(
        user = "postgres",
        password = '0105',
        host = "localhost",
        port = 5432,
        database = "earthquake_db"
    )
    return connection.cursor()



app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/earthquake_info")
def earthquake_info(
    region: str = "",
    start_date: str = "",
    end_date: str = ""
):
    print('successful')
    sql = f"""
    select * from earthquake
    where region = '{region}'
    and date >= '{start_date}'
    and date <= '{end_date}'
    """
    postgre_conn = get_postgresql_conn()
    data_df = pd.read_sql(sql, con = postgre_conn)
    data_dict = data_df.to_dict(orient = 'records')
    return {'date': data_dict}