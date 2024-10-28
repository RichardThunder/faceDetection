import os

def get_jpg_file_paths(directory):
    """
    获取指定文件夹下的所有 jpg 文件路径列表，如果文件数量超过 100 个，则分段成多个列表。

    :param directory: 文件夹路径
    :return: jpg 文件路径的列表或多个列表的列表
    """
    # 确保提供的路径是一个有效的文件夹
    if not os.path.isdir(directory):
        raise ValueError(f"'{directory}' 不是一个有效的文件夹路径")

    # 获取文件夹下所有 jpg 文件的路径
    jpg_file_paths = [
        os.path.join(directory, filename)
        for filename in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, filename)) and filename.lower().endswith('.jpg')
    ]
    return jpg_file_paths

# 示例使用
folder_path = '你的文件夹路径'
try:
    jpg_file_lists = get_jpg_file_paths(folder_path)
    for i, jpg_file_list in enumerate(jpg_file_lists):
        print(f"JPG 文件列表 {i + 1}:")
        for jpg_file in jpg_file_list:
            print(jpg_file)
except ValueError as e:
    print(e)
