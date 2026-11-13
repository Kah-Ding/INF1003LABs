FROM python:3.9-slim

WORKDIR /app

COPY *.py ./

CMD ["python", "-u", "main.py"]
