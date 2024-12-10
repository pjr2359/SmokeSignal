# Use an official Python image that has a Debian-based environment so we can install dependencies easily
FROM python:3.11-slim


# Set environment variables to ensure output is immediately flushed
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system-level dependencies needed to build psycopg2 from source
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/
RUN pip install --upgrade pip
# Install Python dependencies, including psycopg2 and Django
RUN pip install --no-cache-dir -r requirements.txt

# Copy your entire project to the container
COPY . /app

# Expose the port your app runs on
EXPOSE 8000

# Start your application with gunicorn (adjust the project name and wsgi module as needed)
CMD ["gunicorn", "weedfeed.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=3"]
