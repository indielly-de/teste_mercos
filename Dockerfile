FROM python:3.9

WORKDIR /app

COPY src/ /app
COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app:create_app", "-b", "0.0.0.0:8000", "--reload"]
