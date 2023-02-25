
FROM python:3.10.9

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip


WORKDIR /app
COPY . .


RUN python -m pip install -r requirements.txt


CMD  ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
