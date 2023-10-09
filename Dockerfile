FROM python:3.11.4-bullseye

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --without dev_local

ENV DJANGO_SETTINGS_MODULE=adrianolczak.settings.local

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]