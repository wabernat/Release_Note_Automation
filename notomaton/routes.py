from .app import app
from flask import request, jsonify, redirect, send_file
from .render import render_template, render_pdf, render_html
from .jira import get_fixed, get_known
from .assets import get_asset
import io
from .util.auth import requires_auth

@app.route('/')
def redirect_to_dashboard():
    return redirect('/dashboard')

@app.route("/dashboard")
@requires_auth
def dashboard():
    return render_template('dashboard', style=get_asset('style'))


@app.route('/_/render', methods=['GET'])
@requires_auth
def render():
    known = get_known(request.args['project'].lower(), request.args['version'])
    fixed = get_fixed(request.args['project'].lower(), request.args['version'])
    file_format = request.args['format']
    if file_format == 'pdf':
        return send_file(
            render_pdf({
                'project': request.args['project'],
                'version': request.args['version']
            }, known, fixed),
            as_attachment=True,
            attachment_filename='%s-%s-release-notes.pdf'%(request.args['project'], request.args['version']),
            cache_timeout=-1
        )
    elif file_format == 'html':
        return send_file(
            io.BytesIO(render_html({
                'project': request.args['project'],
                'version': request.args['version']
            }, known, fixed).encode('utf-8')),
            as_attachment=True,
            attachment_filename='%s-%s-release-notes.html'%(request.args['project'], request.args['version']),
            cache_timeout=-1
        )


@app.route('/_/issues', methods=['GET'])
@requires_auth
def issues():
    try:
        known = get_known(request.args['project'].lower(), request.args['version'])
        fixed = get_fixed(request.args['project'].lower(), request.args['version'])
        return render_template('issues', issues=known, issue_type='Known') + \
                render_template('issues', issues=fixed, issue_type='Fixed')
    except KeyError:
        return 'Bad Request', 400


@app.route('/_/download', methods=['GET'])
def download():
    pass
