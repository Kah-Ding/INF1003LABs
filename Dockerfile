FROM python:3.9-slim
WORKDIR /app
COPY persistent_auditor.py .
CMD ["python", "persistent_auditor.py"]