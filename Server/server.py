from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import config

app = Flask(__name__, static_folder=None)
CORS(app, resources={r"/api/*": {'origins': config.CORS_ORIGINS}})

# --------------------------------------------------#
# Server Settings
# --------------------------------------------------#
app.config['AVAILABLE_TYPE_LIST'] = config.AVAILABLE_TYPE_LIST
app.config['API_MAX_RETRIES'] = config.API_MAX_RETRIES
app.config['API_TIMEOUT'] = config.API_TIMEOUT
app.config['AGENT_MODEL'] = config.AGENT_MODEL
app.config['AGENT_ROLE_INST'] = config.AGENT_ROLE_INST
app.config['AGENT_TEAM_EVAL_INST'] = config.AGENT_TEAM_EVAL_INST
app.config['AGENT_LOOKUP_INST'] = config.AGENT_LOOKUP_INST
app.config['AGENT_PERSONA_INST'] = config.AGENT_PERSONA_INST

with app.app_context():
    from Model import llm
    llm.load_agent()
    from API import health, evaluate, lookup, persona

# --------------------------------------------------#
# API Routes
# --------------------------------------------------#
@app.get('/')
def llm_health_check():
    response = health.check()
    status = 200
    if response['agent_status'] == 'error':
        status = 500
    response['status'] = status
    return jsonify(response), status

@app.post('/evaluate')
def llm_evaluate():
    body = request.get_json(silent=True)
    if not body:
        abort(400, description='No request body provided')
    team = body.get('team')
    if team is None:
        abort(400, description='No team data provided')
    elif isinstance(team, list) and len(team) == 0:
        abort(400, description='Team list is empty')

    status = 200
    response = evaluate.check_team(team)
    if not response['success']:
        status = 500

    return jsonify(response), status

@app.post('/persona')
def llm_persona():
    status = 200
    response = persona.evaluate()
    if not response['success']:
        status = 500
    return jsonify(response), status

@app.post('/dex')
def llm_lookup():
    body = request.get_json(silent=True)
    if not body:
        abort(400, description='No request body provided')
    target = body.get('target')
    if target is None:
        abort(400, description='No target pokemon provided')

    status = 200
    success, response = lookup.search(target)
    if not success:
        status = 500
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