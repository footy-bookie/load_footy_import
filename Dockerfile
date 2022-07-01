FROM python:3.9

WORKDIR src
COPY /src /src

RUN pip install -r requirements.txt

CMD [ "python", "main.py"]