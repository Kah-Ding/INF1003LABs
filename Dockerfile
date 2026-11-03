FROM python:3.9-slim

WORKDIR /app

COPY main.py product.py inventory.py file_handler.py ./

CMD ["python", "-u", "main.py"]
