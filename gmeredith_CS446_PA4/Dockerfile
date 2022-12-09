FROM python:latest

WORKDIR ~/gmeredith_CS446_PA4

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY pythonCode2.py ./

CMD [ "python3", "./pythonCode2" ]
