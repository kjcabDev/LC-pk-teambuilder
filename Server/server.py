from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import config

app = Flask(__name__, static_folder=None)
CORS(app, resources={r"/api/*": {'origins': config.CORS_ORIGINS}})

# --------------------------------------------------#
# Server Settings
# --------------------------------------------------#
app.config['AGENT_MODEL'] = config.AGENT_MODEL
app.config['AGENT_EVAL_INSTRUCTIONS'] = config.AGENT_EVAL_INSTRUCTIONS

with app.app_context():
    from API import health, evaluate

# --------------------------------------------------#
# API Routes
# --------------------------------------------------#
@app.get('/')
def llm_health_check():
    llm_state = health.check()
    response = {
        'status': 'ok',
        'llm_is_active': llm_state,
        'llm_creds': 'full'
    }
    return jsonify(response)

@app.post('/evaluate')
def llm_evaluate():
    body = request.get_json(silent=True)
    if not body:
        abort(404, description='No request body provided')
    team = body.get('team')
    if team is None:
        abort(404, description='No team data provided')
    elif isinstance(team, list) and len(team) == 0:
        abort(404, description='Team list is empty')

    status = 200
    response = evaluate.check_team(team)
    return jsonify(response), status

# --------------------------------------------------#
# Error Handlers
# --------------------------------------------------#
@app.errorhandler(404)
@app.errorhandler(400)
def _page_not_found(err):
    return jsonify( {
        'error': getattr(err, 'description', str(err)),
    }), err.code

# --------------------------------------------------#
# Server Startup
# --------------------------------------------------#

if __name__ == '__main__':
    app.run(
        host = config.HOST,
        port = config.PORT,
        debug = config.DEBUG
    )