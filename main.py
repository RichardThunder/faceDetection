import os
from datetime import datetime

import torch

from load_config import load_yaml_config
from orgnize_images import organize_images
import schedule
import time


def generate_subfolder_paths(folder_path):
    # 存储所有子文件夹路径的列表
    subfolder_paths = []

    # 遍历文件夹中的内容
    for root, dirs, files in os.walk(folder_path):
        # 只遍历第一层子文件夹
        for subfolder in dirs:
            # 生成完整的子文件夹路径
            full_path = os.path.join(root, subfolder)
            subfolder_paths.append(full_path)
        break  # 只处理当前文件夹，避免递归进入子文件夹

    return subfolder_paths


def main():
    # 使用示例

    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"使用设备: {device}")
    config = load_yaml_config("config/config.yaml")

    for source_folder in generate_subfolder_paths(config["source_folder"]):
        organize_images(source_folder, device)
    print(f"task complete:{datetime.now()}")


if __name__ == '__main__':
    config = load_yaml_config("config/config.yaml")
    schedule.every(config["interval"]).hours.do(main)
    main()
    while True:
        schedule.run_pending()
        time.sleep(1)
