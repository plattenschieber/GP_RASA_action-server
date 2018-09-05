FROM python:3.6-slim

# Copy Project
COPY . /app

# Work directory
WORKDIR /app

# install requirements
RUN pip install -r requirements.txt

# Start action server
ENTRYPOINT python -m rasa_core_sdk.endpoint --actions actions