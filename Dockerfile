# 1. Use an official Python runtime as a parent image
# Using a slim image keeps the final container size smaller.
FROM python:3.12-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file into the container
# This is done first to leverage Docker's layer caching.
# Dependencies will only be re-installed if requirements.txt changes.
COPY requirements.txt .

# 4. Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application's code into the container
COPY . .

# 6. Expose the port that the FastAPI app will run on
EXPOSE 8000

# 7. Define the command to run the application when the container starts
# We use --host 0.0.0.0 to make the app accessible from outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
