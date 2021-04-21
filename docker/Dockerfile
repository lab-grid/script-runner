ARG PYTHON_IMAGE_TAG=alpine

FROM python:${PYTHON_IMAGE_TAG}

WORKDIR /app

COPY . /script-runner
RUN pip install /script-runner
RUN rm -rf /script-runner

ENV FLASK_APP=script_runner.main:app

CMD "python3 -m gunicorn.app.wsgiapp --timeout 240 --bind 0.0.0.0:${PORT} --access-logfile - --error-logfile - --workers 4 ${FLASK_APP}"
