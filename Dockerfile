FROM python:3.6-alpine

MAINTAINER jiangtao "jiangtao.work@gmail.com"

EXPOSE 8000
ENV PYTHONUNBUFFERED 0

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk update \
    && apk add --update --no-cache g++ gcc libxslt-dev

WORKDIR /app
ADD . /app/

RUN pip install --no-cache-dir --upgrade pip -i https://mirrors.aliyun.com/pypi/simple \
    && pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

# ENTRYPOINT ["python", "run.py"]
