FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 8000

RUN python manage.py collectstatic --no-input

CMD ["sh", "-c", "python manage.py migrate && python manage.py loaddata initial_data.json && python manage.py runserver 0.0.0.0:8000"]