# Use the official Python 3.11 image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Install virtualenv before using it
RUN pip install --upgrade pip && pip install virtualenv

# Create a virtual environment
RUN virtualenv venv

# Set the PATH to use the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Copy the requirements file and install dependencies inside the virtual environment
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY script.py /app

# Run the Python script when the container starts
CMD ["python", "script.py", "--baseurl", "http://10.1.0.125:8282"]
