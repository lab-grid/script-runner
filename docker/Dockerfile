ARG SCRIPT_RUNNER_VERSION=local+container
ARG PYTHON_IMAGE_TAG=alpine

FROM python:${PYTHON_IMAGE_TAG}}

WORKDIR /app

RUN pip install script_runner==${SCRIPT_RUNNER_VERSION}

COPY ./entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./ .

ENV PYTHONPATH="${RBASE}:${PYTHONPATH}"
ENV FLASK_APP=/app/main.py
ENV SERVER_VERSION=$SERVER_VERSION

ENTRYPOINT [ "/entrypoint.sh" ]
