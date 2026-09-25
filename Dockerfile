FROM python:3.9-slim
WORKDIR /app
COPY persistent_auditor.py .
VOLUME ["/app/lab_inventory"]
CMD ["python", "persistent_auditor.py"]