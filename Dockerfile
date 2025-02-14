# Use the official Python image as base
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install Poetry
RUN pip install poetry

# Install dependencies using Poetry
RUN poetry install --no-root

# Expose the port Django runs on
EXPOSE 8000

# Command to run migrations and start the app
CMD ["sh", "-c", "poetry run python manage.py migrate && poetry run python manage.py runserver 0.0.0.0:8000"]
