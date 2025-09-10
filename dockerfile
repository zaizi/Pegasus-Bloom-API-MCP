
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:."

COPY ./requirements.txt /app/requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]