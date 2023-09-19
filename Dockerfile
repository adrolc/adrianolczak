FROM python:3.11.4-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy poetry files to the working directory
COPY pyproject.toml poetry.lock* ./

# Install project dependencies
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --without dev_local

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=adrianolczak.settings.local

# Expose port 8000 for the Django development server
EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]