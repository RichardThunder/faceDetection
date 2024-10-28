import yaml

def load_yaml_config(file_path):
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)  # 使用 safe_load 加载配置
    return config
