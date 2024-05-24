import yaml

def get_db_config():
    with open("config/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config["db_creds"], config["tables"]
