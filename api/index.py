from fastapi import FastAPI
from datetime import datetime, date
from typing import Dict
import random
import korean_age_calculator as kac
import sys
import pandas as pd
import psycopg
from dotenv import load_dotenv
import os
from psycopg.rows import dict_row


### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

load_dotenv()
db_name = os.getenv("POSTGRES_DATABASE")
DB_CONFIG = {
        "user": os.getenv("POSTGRES_USER"),
        "dbname": db_name,
        "password": os.getenv("POSTGRES_PASSWORD"),
        "host": os.getenv("POSTGRES_HOST"),
        "port": os.getenv("DB_PORT", "5432")
}
# DB_CONFIG = {
#         "user": "sunsin",
#         "dbname": "postgres",
#         "password": "mysecretpassword",
#         "host": "localhost",
#         "port": "5432"
# }

# def get_connection():
#     return psycopg.connect(**DB_CONFIG)



@app.get("/api/py/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI"}

@app.get("/api/py/ageCalculator/birthday/{birthday}")
def age_calculator(birthday: str) -> Dict[str, str]:
    """
    생년월일을 입력받아 만나이를 계산하는 API

    :param birthday: 생년월일 (형식: YYYY-MM-DD)
    :return: 생년월일 및 만나이를 포함한 JSON 응답
    """
    #random_age = random.randint(0, 100)
    
    today = date.today()
    birth_date = datetime.strptime(birthday, "%Y-%m-%d").date()
    age = today.year - birth_date.year

    list1 = ["쥐", "소", "호랑이", "토끼", "용", "뱀", "말", "양", "원숭이", "닭", "개", "돼지" ]
    cal=(birth_date.year-4)%12

    zodiac=list1[cal]

    if birth_date.month>today.month:
        age=age-1
    elif birth_date.month==today.month:
        if birth_date.day>today.day:
            age=age-1
    

    #한국식 나이계산
    kage = kac.how_korean_age(year_of_birth=birth_date.year)

    return {
            "birthday": birthday,
            "age": str(age),
            "kage": str(kage),
            "speaker": "홍길동",
            "version": sys.version,
            "basedate": str(today),
            "zodiac": zodiac,
            "message": "Age calculated successfully!"
            }

@app.get("/api/py/ageCalculator/pickStudent")
def pickStudent():
    studentlist = ["조민규", "강현룡", "백지원", "서민혁", "권오준", "조성근", "전희진", "배형균", "민경국"]
    randomNumber = random.randint(0, len(studentlist)-1)

    student = studentlist[randomNumber]

    return {
            "student": student,
            "message": "Picked student successfully!"
            }

@app.get("/api/py/select_all")
def select_all():
    # load_dotenv()
    query = """select * from view_select_all;"""
    
    with psycopg.connect(**DB_CONFIG, row_factory=dict_row) as conn:
        cur = conn.execute(query)
        rows = cur.fetchall()
        return rows


# @app.get("/api/py/db")
# def import_db():
#     query = """SELECT
#     menu_name AS menu,
#     dt
#     FROM lunch_menu
#     ORDER BY dt DESC"""
    
#     conn = get_connection()
#     with conn.cursor() as cur:
#         cur.execute(query)
#         rows = cur.fetchall()
#     select_df = pd.DataFrame(rows, columns=['menu', 'dt'])
#     return select_df