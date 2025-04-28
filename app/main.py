from fastapi import FastAPI, Depends
from sqlmodel import Session
from app.db import get_session
from app.models import StockData
from app.crud import get_all_records, add_record
from db.db import get_session
app = FastAPI()

@app.get("/data")
def fetch_all_data(session: Session = Depends(get_session)):
    records = get_all_records(session)
    return {"data": records}

@app.post("/data")
def post_data(data: StockData, session: Session = Depends(get_session)):
    new_record = add_record(session, data)
    return {"message": "Record added successfully", "record": new_record}