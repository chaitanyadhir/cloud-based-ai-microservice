# Use an official Python image as a base
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Expose ports
EXPOSE 8000 8501

# Start both FastAPI backend and Streamlit frontend
# FastAPI on :8000, Streamlit on :8501
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0"]

