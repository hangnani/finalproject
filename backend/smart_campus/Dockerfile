# 使用官方 Python 镜像作为基础镜像
FROM python:3.8-slim-buster

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 到工作目录
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码到工作目录
COPY . .

# 暴露端口
EXPOSE 8000

# 运行命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]