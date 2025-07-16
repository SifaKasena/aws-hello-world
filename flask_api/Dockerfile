FROM python:3.12-slim-bullseye

WORKDIR /flask_api
COPY . .
RUN pip3 install -r requirements
EXPOSE ${PORT}

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app", "--access-logfile", "-" ]
