ARG SCRIPT_RUNNER_VERSION=local+container
ARG PYTHON_IMAGE_TAG=alpine

FROM python:${PYTHON_IMAGE_TAG}}

WORKDIR /app

RUN pip install script-runner-api==${SCRIPT_RUNNER_VERSION}

COPY ./entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./ .

ENV FLASK_APP=script_runner.main:app
ENV SERVER_VERSION=$SERVER_VERSION

ENTRYPOINT [ "/entrypoint.sh" ]
