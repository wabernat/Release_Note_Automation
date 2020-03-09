import io
import tempfile

import pdfkit

from .assets import Book
from .constants import PRODUCT_TO_CANONICAL
from .context import build_context
from .templates import get_template
import datetime

# For rendering internal app tempaltes
def render_template(name, **kwargs):
    tmpl = get_template(name)
    if tmpl is None:
        raise Exception('Unable to locate template %s'%name)
    return tmpl.render(**kwargs)

def as_file(f):
    def inner(*args, **kwargs):
        out = io.BytesIO()
        data = f(*args, **kwargs)
        if isinstance(data, str):
            data = data.encode('utf-8')
        out.write(data)
        out.seek(0)
        return out
    return inner

def _render_html(book, ctx):
    return book.render(ctx)

def _render_pdf(book, ctx):
    pdf_opts = {
        'footer-left': f'© {datetime.date.today().year} Scality. All rights reserved\n\n',
        'footer-right': '• [page]',
        'footer-line': '',
        'footer-font-size': '10',
#        'footer-spacing': '6',
        'margin-bottom': '6mm',
    }
    rendered_html = _render_html(book, ctx)
    return pdfkit.from_string(rendered_html, False, toc={}, options=pdf_opts, cover_first=True)

_MODES = { 'html': _render_html, 'pdf': _render_pdf }
def render_book(book, ctx, mode='html'):
    render_func = _MODES.get(mode)
    if render_func is None:
        raise Exception('Unknown render mode %s', mode)
    return render_func(book, ctx)

@as_file
def load_and_render_book(product, version, mode='html'):
    book = Book(PRODUCT_TO_CANONICAL[product], version)
    ctx = build_context(product, version)
    return render_book(book, ctx, mode)
