import os
from fastapi import FastAPI
from app.expectations import create_datasource, run_expectations, load_db_config

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to DataSanity"}

@app.get("/run_checks")
def run_checks():
    datasource = create_datasource()
    db_config, tables = load_db_config()
    results = []
    for table in tables:
        table_name = table['name']
        results.append(run_expectations("my_datasource", table_name))
    return results

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
