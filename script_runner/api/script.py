from celery.result import AsyncResult

from flask import abort, request
from flask_restx import Resource, fields, Namespace

from script_runner.analysis import run_script
from script_runner.authorization import requires_auth


api = Namespace('script', description='Operations for running a long-lived script.', path='/')


script_result = api.model('ScriptResult', {})
script_attachments = api.model('ScriptAttachments', {
    'LIMS_results.csv': fields.String(),
})
script_output = api.model('ScriptOutput', {
    'id': fields.String(),
    'status': fields.String(),
    'results': fields.List(fields.Nested(script_result)),
    'attachments': fields.Nested(script_attachments),
})


@api.route('/script/<path:path>')
class ScriptTasksResource(Resource):
    @api.doc(security='token', model=script_output)
    @requires_auth
    def post(self, path):
        task = run_script.delay(path, request.args, request.json)

        return {
            "id": task.task_id,
            "status": "ready" if task.ready() else "not-ready",
        }


@api.route('/script/<string:task_id>')
class ScriptTaskResource(Resource):
    @api.doc(security='token', model=script_output)
    @requires_auth
    def get(self, task_id):
        result = AsyncResult(task_id)

        if result.ready():
            response = result.get()
            response['id'] = result.task_id
            return response
        else:
            return {
                'id': result.task_id,
                'status': 'not-ready',
            }
