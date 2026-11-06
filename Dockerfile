FROM python:3.9-slim

WORKDIR /app

COPY main.py product.py inventory.py file_handler.py physical_product.py digital_product.py can_be_shipped.py ./

CMD ["python", "-u", "main.py"]
