import yaml

def get_config():
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config

def get_db_config():
    config = get_config()
    return config['db_creds']

def get_tables_config():
    config = get_config()
    return config['tables']
