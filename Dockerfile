# 使用官方的Python运行时作为父镜像
FROM python:3.7

# 设置工作目录为/app
WORKDIR /app

# 将当前目录内容复制到容器的/app内
COPY . /app

# 安装任何需要的包
RUN pip install --no-cache-dir -r requirements.txt

# 收集静态文件到指定目录
RUN python manage.py collectstatic --noinput

# 对外暴露的端口号
EXPOSE 8000

# 定义环境变量
ENV PYTHONUNBUFFERED 1

# 当容器启动时运行Django项目
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]