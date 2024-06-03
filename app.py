from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from great_expectations.checkpoint import Checkpoint
from great_expectations.core.batch import BatchRequest
import os

app = FastAPI()

# Load Checkpoint (Define data source, BatchRequest, and Expectations in `great_expectations.yml`)
checkpoint = Checkpoint(name='default_checkpoint')

@app.post("/data_quality")
async def check_data_quality(request: Request):
  """
  Endpoint to perform data quality checks.
  """
  try:
    # Get data source credentials from environment variables
    project_id = os.environ['PROJECT_ID']
    dataset_id = os.environ['DATASET_ID']
    table_name = os.environ['TABLE_NAME']

    # Construct BatchRequest based on provided environment variables
    batch_request = BatchRequest(
      datasource_name="default", 
      data_connector_name="bigquery",
      data_asset_name=table_name,
      runtime_parameters={"query": f"SELECT * FROM {project_id}.{dataset_id}.{table_name}"}
    )

    # Execute the checkpoint and get validation results
    validation_results = checkpoint.run(batch_request=batch_request)
    results_json = validation_results.to_json_dict()

    return JSONResponse(status_code=200, content=results_json)

  except Exception as e:
    return JSONResponse(status_code=500, content={'message': f"Data quality check failed: {str(e)}"})