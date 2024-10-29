import datetime
import os
import shutil

from ultralytics import YOLO

from faceRecog import detect_face
from PIL import Image

from load_config import load_yaml_config

config = load_yaml_config("config/config.yaml")


def organize_images(source_folder, device):
    """
    将当前目录下的 .jpg 文件根据人脸检测结果移动到相应的文件夹。

    参数:
    source_folder (str): 包含要处理的图像文件的文件夹路径。
    mtcnn (MTCNN): MTCNN 模型实例。
    device: 计算设备（GPU 或 CPU）。
    """
    face_folder = os.path.join(source_folder, config['person_folder'])
    delete_folder = os.path.join(source_folder, config["no_person_folder"])
    threshold=config['threshold']
    ## load model
    model = YOLO("yolo11s.pt")
    # 将模型移动到 MPS 设备
    # model.to(device)
    os.makedirs(face_folder, exist_ok=True)
    os.makedirs(delete_folder, exist_ok=True)

    # 遍历源文件夹中的所有文件
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)

        # 仅处理 .jpg 文件且是文件而不是文件夹
        if os.path.isfile(file_path) and filename.lower().endswith('.jpg'):
            # 检查图像中是否存在人脸
            if detect_face(file_path, model, device,threshold):
                compress_image_to_target_size(file_path)
                shutil.move(file_path, face_folder)
                print(f'已移动文件: {filename} 到 {face_folder}')
                print(f"task complete:{datetime.datetime.now()}")
            else:
                shutil.move(file_path, delete_folder)
                print(f'已移动文件: {filename} 到 {delete_folder}')
                print(f"task complete:{datetime.datetime.now()}")


def compress_image_to_target_size(file_path):
    """
    压缩 JPEG 图片到指定的大小。
    - file_path: 图片路径
    - target_size_kb: 目标大小 (单位 KB)
    """

    target_size_kb = config['target_size_kb']
    target_size_bytes = target_size_kb * 1024  # 将目标大小转为字节
    quality = 95  # 初始质量设为 95
    step = 5  # 每次减少质量的步长

    # 尝试压缩直到达到目标大小
    with Image.open(file_path) as img:
        img = img.convert("RGB")  # 确保是 RGB 模式
        while True:
            # 临时保存图像到内存中以检查大小
            output_path = file_path.replace(".jpg", "_compressed.jpg")
            img.save(output_path, "JPEG", quality=quality)
            # 检查文件大小
            compressed_size = os.path.getsize(output_path)

            # 如果大小已符合要求，保存并退出
            if compressed_size <= target_size_bytes:
                os.rename(output_path, file_path)  # 用压缩图像替换原图
                print(f"压缩完成: {file_path} (大小: {compressed_size / 1024:.2f} KB)")
                break

            # 如果无法进一步降低质量或质量过低时停止
            if quality - step < 10:
                print(f"无法压缩到目标大小: {file_path} (最终大小: {compressed_size / 1024:.2f} KB)")
                os.remove(output_path)  # 删除过大的压缩图像
                break

            # 减少质量继续尝试
            quality -= step
