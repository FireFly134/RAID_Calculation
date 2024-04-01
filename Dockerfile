FROM python:3.12-slim

ENV PYTHONFAULTHANDLER=1 \
     PYTHONUNBUFFERED=1 \
     PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/local/app

# Install wkhtmltopdf
RUN apt-get update && apt-get install -y wkhtmltopdf

RUN pip install pipenv
COPY ./Pipfile* ./

RUN pipenv install --system --dev --deploy

COPY . .

CMD ["python3", "main_bot.py"]
