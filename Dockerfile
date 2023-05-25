FROM python:slim
ADD ./http_monitor.py   /root/http_monitor.py
WORKDIR /root
RUN apt update && pip install sdcclient
CMD ["python","/root/http_monitor.py"]
