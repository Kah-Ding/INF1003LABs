FROM python:3.9-slim
WORKDIR /app
COPY auditor.py .
CMD ["python", "auditor.py"]