from fastapi import FastAPI
from app.config import get_db_config
from app.expectations import create_datasource, run_expectations

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to DataSanity"}

@app.get("/run_checks")
def run_checks():
    datasource = create_datasource()
    results = run_expectations(datasource.name)
    return results
