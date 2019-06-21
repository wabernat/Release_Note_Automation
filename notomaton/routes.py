import io

from flask import jsonify, redirect, request, send_file

from .app import app
from .assets import Book, get_asset, load_book
from .constants import CANONICAL_TO_PRODUCT, Product
from .context import build_context
from .render import load_and_render_book, render_template
from .util.auth import requires_auth


@app.route('/')
def redirect_to_dashboard():
    return redirect('/dashboard')


@app.route("/dashboard")
@requires_auth
def dashboard():
    return render_template('dashboard', style=get_asset('common/style.css'))


@app.route('/_/render', methods=['GET'])
@requires_auth
def render():
    if 'product' not in request.args or 'version' not in request.args:
        return 'Bad Request', 400
    product = CANONICAL_TO_PRODUCT.get(request.args['product'].lower())
    if product is None:
        return 'Bad Request', 400
    version = request.args.get('version')
    file_format = request.args.get('format')
    if file_format != 'pdf' and file_format != 'html':
        return 'Bad Request', 400
    return send_file(
        load_and_render_book(product, version, mode=file_format),
        as_attachment=True,
        attachment_filename=f'{product}-{version}-release-notes.{file_format}',
        cache_timeout=-1
    )

@app.route('/_/has_book/<product>/<version>', methods=['GET'])
@requires_auth
def has_book(product, version):
    if CANONICAL_TO_PRODUCT.get(product.lower()) is None:
        return 'Bad Request', 400
    try:
        load_book(product, version)
    except Exception as e:
        return jsonify(dict(exists=False))
    return jsonify(dict(exists=True))


@app.route('/_/issues', methods=['GET'])
@requires_auth
def issues():
    if 'product' not in request.args or 'version' not in request.args:
        return 'Bad Request', 400
    if not request.args['product']:
        return 'Product can not be empty', 400
    elif not request.args['version']:
        return 'Version can not be empty', 400
    product = CANONICAL_TO_PRODUCT.get(request.args['product'].lower())
    if product is None:
        return 'Bad Request', 400
    book = Book('dashboard', '1.0.0')
    ctx = build_context(product, request.args['version'])
    return book.render(ctx)
