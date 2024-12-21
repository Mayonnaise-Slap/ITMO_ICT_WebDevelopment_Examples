FROM python:3.8.5

COPY ./example_2310/ /project/
WORKDIR /project/
COPY ./example_2310/requirements.txt /
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

ENV PYTHONUNBUFFERED 1
