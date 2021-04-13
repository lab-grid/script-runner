#!/usr/bin/env bash

set -ex

if [[ ! -z "${BASESPACE_CFG}" ]]; then
    echo "${BASESPACE_CFG}" > /root/.basespace/default.cfg
fi

if [[ -z "${@}" ]]; then
    python3 -m gunicorn.app.wsgiapp --timeout 240 --bind 0.0.0.0:${PORT} --access-logfile - --error-logfile - --workers 4 main:app
else
    ${@}
fi
