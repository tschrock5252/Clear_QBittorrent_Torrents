FROM python:2.7.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app

# Create and activate a virtual environment
RUN virtualenv venv
ENV PATH="/app/venv/bin:$PATH"
#ENV PYTHONPATH="/app/venv/bin:$PATH"

# Install dependencies from the requirements.txt file
RUN pip install -r requirements.txt

# Copy the Python script into the container
COPY script.py /app

# Run the Python script when the container starts
CMD ["python", "script.py"]
