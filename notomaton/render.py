import io
import tempfile

import pdfkit

from .assets import Book
from .constants import PRODUCT_TO_CANONICAL
from .context import build_context
from .templates import get_template

# For rendering internal app tempaltes
def render_template(name, **kwargs):
    tmpl = get_template(name)
    if tmpl is None:
        raise Exception('Unable to locate template %s'%name)
    return tmpl.render(**kwargs)

def _render_html(book, ctx):
    return book.render(ctx)

def _render_pdf(book, ctx):
    rendered_html = _render_html(book, ctx)
    pdf = io.BytesIO()
    pdf.write(pdfkit.from_string(rendered_html, False))
    pdf.seek(0)
    return pdf

_MODES = { 'html': _render_html, 'pdf': _render_pdf }
def render_book(book, ctx, mode='html'):
    render_func = _MODES.get(mode)
    if render_func is None:
        raise Exception('Unknown render mode %s', mode)
    return render_func(book, ctx)

def load_and_render_book(product, version, mode='html'):
    book = Book(PRODUCT_TO_CANONICAL[product], version)
    ctx = build_context(product, version)
    return render_book(book, ctx, mode)
