# 使用官方的 Python 运行时作为基础镜像
FROM python:3.12-slim
LABEL authors="richard"
# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有文件到镜像的 /app 目录
COPY . .

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 运行主程序
CMD ["python", "main.py"]

