#!/usr/bin/env python

"""Sets up a flask-restx server for running the swabseq analysis R-script."""

from script_runner.server import app, api
from script_runner.api.script import api as script
from script_runner.api.health import api as server_health


api.add_namespace(script)
api.add_namespace(server_health)


if __name__ == '__main__':
    app.run()
