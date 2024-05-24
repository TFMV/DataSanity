import great_expectations as gx
from great_expectations.core.batch import BatchRequest
from app.config import get_db_config, get_tables_config

context = gx.get_context()

def create_datasource():
    db_config = get_db_config()
    connection_string = f"postgresql+psycopg2://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    datasource_name = "my_datasource"
    
    datasource = context.sources.add_postgres(
        name=datasource_name, 
        connection_string=connection_string
    )
    
    return datasource

def run_expectations(datasource_name):
    context = gx.get_context()
    tables_config = get_tables_config()
    
    results = {}
    
    for table in tables_config:
        asset_name = table['name']
        expectations = table['expectations']
        
        batch_request = BatchRequest(
            datasource_name=datasource_name,
            data_asset_name=asset_name
        )
        validator = context.get_validator(batch_request=batch_request)
        
        table_results = {}
        for expectation in expectations:
            result = getattr(validator, expectation['name'])(*expectation['args'], **expectation['kwargs'])
            table_results[expectation['name']] = result
        
        results[asset_name] = table_results
        
    return results
