FROM python:3.7.1-alpine

ADD . /app

WORKDIR /app

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install pipenv  && pipenv install --system

#ENTRYPOINT ["python"]
#CMD ["run.py"]

CMD pipenv run alembic upgrade head && python run.py