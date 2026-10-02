FROM python:3.9-slim
WORKDIR /app
COPY inventory_manager.py .
VOLUME ["/app/lab_inventory"]
CMD ["python", "inventory_manager.py"]
