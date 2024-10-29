FROM python:3.10.8-buster

WORKDIR /opt/motius-project

COPY poetry.lock pyproject.toml ./

RUN pip install --upgrade pip && \
    pip install "poetry==1.6.1" && \
    poetry config virtualenvs.create false && \
    poetry install

COPY src src
COPY scripts scripts
COPY tests tests

ENV PYTHONPATH /opt/motius-project

CMD ["python", "src/bin/api.py"]
