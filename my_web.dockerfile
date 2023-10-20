# 设置基础镜像
FROM python:3.11

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . /app/

# 安装依赖包
RUN pip install -r requirement.txt

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 运行django
CMD python manage.py runserver 0:0:0:0:8000