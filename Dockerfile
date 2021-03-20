FROM python:3.6

LABEL maintainer="Lujia Zhong <937371423@qq.com>"

COPY . /detectweb

WORKDIR /detectweb

RUN pip install -r requirements.txt -i https://mirror.baidu.com/pypi/simple && pip install gunicorn&&chmod 755 run_server.sh

EXPOSE 8080

ENTRYPOINT [ "./run_server.sh" ]
