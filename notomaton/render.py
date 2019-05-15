from .templates import get_template
from .assets import get_asset
import tempfile
import io
import pdfkit

def render_template(name, **kwargs):
    tmpl = get_template(name)
    if tmpl is None:
        raise Exception('Unable to locate template %s'%name)
    return tmpl.render(**kwargs)


def render_html(conf, known, fixed):
    rknown = render_template('issues', issues=known, issue_type='known', **conf)
    rfixed = render_template('issues', issues=fixed, issue_type='fixed', **conf)
    return render_template(
        'release_notes',
        introduction=get_asset('introduction'),
        dependencies=get_asset('dependencies'),
        style=get_asset('style'),
        known_issues=rknown,
        fixed_issues=rfixed
    )


def render_pdf(conf, known, fixed):
    book = io.BytesIO()
    rendered_html = render_html(conf, known, fixed)
    book.write(pdfkit.from_string(rendered_html, False))
    book.seek(0)
    return book
