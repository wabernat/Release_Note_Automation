from .app import app
from flask import request, jsonify
from .render import render_template
from .jira import get_fixed, get_known
from .assets import get_asset

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard', style=get_asset('style'))


@app.route('/_/render', methods=['POST'])
def render():
    pass


@app.route('/_/issues', methods=['GET'])
def issues():
    try:
        known = get_known(request.args['project'], request.args['version'])
        fixed = get_fixed(request.args['project'], request.args['version'])
        return render_template('issues', issues=known, issue_type='Known') + \
                render_template('issues', issues=fixed, issue_type='Fixed')
    except KeyError:
        return 'Bad Request', 400
    # except Exception as e:
    #     return 'Internal Error\n' + str(e), 500


@app.route('/_/download', methods=['GET'])
def download():
    pass
