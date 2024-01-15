FROM python:3.11.5-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /srv/app

RUN addgroup -S user && adduser -S user -G user

USER user

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

COPY ./data .

RUN source data/environment.sh

EXPOSE 58008

CMD ["make", "run_server"]
