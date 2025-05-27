import os

import psycopg2
from psycopg2.extras import RealDictCursor

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from auth import authrouter
from home_page import home_page_router
from users import user_router
from card_payments import card_payments_router


os.makedirs("uploads", exist_ok=True)


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
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


app.include_router(user_router)
app.include_router(authrouter)
app.include_router(home_page_router)
app.include_router(card_payments_router)
