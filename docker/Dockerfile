
# ---- Define python version e workdir app ----
FROM python:3.11-slim
WORKDIR /kokkan

# ---- Define python dependencies ----
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy of infra ----
COPY config/ ./config/
COPY detectors/ ./detectors/
COPY engine/ ./engine/
COPY responders/ ./responders/
COPY safeguards/ ./safeguards/

# ---- Run Orchestrator ----
CMD ["python","./engine/healer.py"]