from .templates import get_template
from .assets import get_asset

def render_template(name, **kwargs):
    tmpl = get_template(name)
    if tmpl is None:
        raise Exception('Unable to locate template %s'%name)
    return tmpl.render(**kwargs)


def render_html(conf, known, fixed):
    rknown = render_template('issues', issues=known, type='known', **conf)
    rfixed = render_template('issues', issues=fixed, type='fixed', **conf)
    return render_template(
        'release_notes',
        introduction=get_asset('introduction'),
        dependencies=get_asset('dependencies'),
        style=get_asset('style'),
        known_issues=rknown,
        fixed_issues=rfixed
    )
