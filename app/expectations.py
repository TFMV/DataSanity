import yaml
import great_expectations as gx
from sqlalchemy import create_engine
from great_expectations.core.expectation_suite import ExpectationSuite

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
    engine = create_engine(connection_string)

    datasource_name = "my_datasource"
    if datasource_name not in context.list_datasources():
        context.sources.add_sql(
            name=datasource_name,
            connection_string=connection_string
        )
    
    datasource = context.get_datasource(datasource_name)
    schema = db_config['schema']
    for table in tables:
        full_table_name = f"{schema}.{table['name']}"
        if table['name'] not in datasource.get_available_data_asset_names():
            datasource.add_table_asset(name=table['name'], table_name=full_table_name)

    return datasource

def create_expectation_suite():
    context = gx.get_context()
    suite_name = "default"
    try:
        suite = context.get_expectation_suite(expectation_suite_name=suite_name)
    except gx.exceptions.DataContextError:
        suite = ExpectationSuite(expectation_suite_name=suite_name)
        context.add_expectation_suite(expectation_suite=suite)

    db_config, tables = load_db_config()
    schema = db_config['schema']

    for table in tables:
        table_name = table['name']
        validator = context.get_validator(
            datasource_name="my_datasource",
            data_asset_name=f"{schema}.{table_name}",
            expectation_suite_name=suite_name
        )
        
        for exp in table['expectations']:
            exp_name = exp['name']
            args = exp['args']
            kwargs = exp['kwargs']
            getattr(validator, exp_name)(*args, **kwargs)
        context.save_expectation_suite(suite)

def run_expectations(datasource_name, table_name):
    context = gx.get_context()
    create_expectation_suite()
    suite = context.get_expectation_suite(expectation_suite_name="default")
    validator = context.get_validator(datasource_name=datasource_name, data_asset_name=table_name, expectation_suite_name=suite.expectation_suite_name)
    
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
