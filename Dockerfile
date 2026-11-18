FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY audit/ audit/
COPY rules/ rules/
COPY samples/ samples/
RUN useradd --create-home auditor && chown -R auditor /app
USER auditor
ENTRYPOINT ["python", "-m", "audit"]
