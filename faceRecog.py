# import cv2
#
# def contains_face(image_path):
#     """
#     检查指定图像文件中是否存在人脸。
#
#     参数:
#     image_path (str): 图像文件的路径。
#
#     返回:
#     bool: 如果检测到人脸则返回 True，否则返回 False。
#     """
#     # 加载人脸检测的分类器
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#
#     # 读取图像
#     image = cv2.imread(image_path)
#
#     # 检查图像是否成功加载
#     if image is None:
#         raise ValueError(f"无法读取图像: {image_path}")
#
#     # 转换为灰度图像
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # 检测人脸
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
#
#     # 如果检测到人脸，则返回 True
#     return len(faces) > 0

# # 使用示例
# image_path = 'path_to_your_image.jpg'  # 替换为你的图像文件路径
# if contains_face(image_path):
#     print("图像中存在人脸。")
# else:
#     print("图像中不存在人脸。")

from PIL import Image


def is_person_detected(results, img_width, img_height, threshold):

    # 遍历每个预测结果

    for result in results:
        # 遍历每个检测框
        for box in result.boxes:
            # 检查类别ID，通常COCO数据集中 '0' 代表人
            if int(box.cls) == 0:  # 人物类的ID通常是0（根据训练数据集调整）
                # 计算检测框的宽度和高度
                x1, y1, x2, y2 = box.xyxy[0]  # 获取检测框坐标
                face_area = (x2 - x1) * (y2 - y1)  # 计算检测框的面积

                # 计算面积占比
                face_ratio = face_area / (img_width * img_height)
                print(face_ratio)
                # 如果面积占比超过阈值，返回 True
                if face_ratio > threshold:
                    return True

    # 没有符合条件的人物时，返回 False
    return False

def detect_face(image_path,model, device,threshold):
    """
    返回:
    bool: 如果检测到人脸，返回 True；否则返回 False。
    """


    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"文件未找到: {image_path}")
    except IOError:
        print("无法打开图片，请检查文件格式或损坏情况")
    except Exception as e:
        print(f"发生错误: {e}")
    result = model(image_path, device=device)
    if is_person_detected(result, img.width, img.height, threshold):
        return True
    else:
        return False
