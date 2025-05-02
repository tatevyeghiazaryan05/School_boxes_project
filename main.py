# from database import engine
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI


# Base.metadata.create_all(bind=engine)
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="password",
    database="online_store",
    cursor_factory=RealDictCursor
    )

cursor = conn.cursor()

app = FastAPI()


#todo create admin_panel
#todo user will see products and filter
