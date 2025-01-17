import yaml

def load_config(yaml_path: str) -> dict:
    """
    Loads the config from a YAML file and returns it as a Python dict.
    """
    with open(yaml_path, "r") as f:
        config_data = yaml.safe_load(f)
    return config_data