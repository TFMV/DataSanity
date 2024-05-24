import yaml
import great_expectations as gx
from sqlalchemy import create_engine

def load_db_config():
    with open("config/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config["db_creds"], config["tables"]

def create_datasource():
    db_config, tables = load_db_config()
    context = gx.get_context()
    
    connection_string = (
        f"postgresql+psycopg2://{db_config['username']}:{db_config['password']}"
        f"@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    )
    
    datasource = context.sources.add_postgres(name="my_datasource", connection_string=connection_string)
    
    schema = db_config['schema']
    for table in tables:
        full_table_name = f"{schema}.{table['name']}"
        datasource.add_table_asset(name=table['name'], table_name=full_table_name)
    
    context.add_datasource(datasource)
    return datasource

def run_expectations(datasource_name, table_name):
    context = gx.get_context()
    suite = context.get_expectation_suite(name="default")
    validator = context.get_validator(datasource_name=datasource_name, data_asset_name=table_name, expectation_suite=suite)
    
    db_config, tables = load_db_config()
    table_config = next(t for t in tables if t['name'] == table_name)
    results = []
    
    for exp in table_config['expectations']:
        exp_name = exp['name']
        args = exp['args']
        kwargs = exp['kwargs']
        result = getattr(validator, exp_name)(*args, **kwargs)
        results.append(result)
    
    return results
