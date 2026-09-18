FROM python:3.9-slim
WORKDIR /app
COPY modular_auditor.py .
CMD ["python", "modular_auditor.py"]