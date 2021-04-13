from flask_restx import Resource, fields, Namespace

from script_runner.server import app


api = Namespace('server-health', description="Service health checks.", path='/')


health_output = api.model('HealthOutput', {
    'version': fields.String(),
    'server': fields.Boolean(),
})


@api.route('/health')
class HealthResource(Resource):
    @api.doc(model=health_output)
    def get(self):
        return {
            'version': app.config['SERVER_VERSION'],
            'server': True,
        }
