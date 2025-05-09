# from database import engine
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from users import user_router



# Base.metadata.create_all(bind=engine)
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="password",
    database="school_boxes_project",
    cursor_factory=RealDictCursor
    )

cursor = conn.cursor()

app = FastAPI()

app.include_router(user_router)

#todo create admin_panel+
#todo user will see products and filter+
