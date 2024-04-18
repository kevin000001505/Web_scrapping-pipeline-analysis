from fastapi import FastAPI
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, engine


def get_postgresql_conn() -> engine.base.connection:
    




app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}