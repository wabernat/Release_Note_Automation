from .templates import get_template


def render_template(name, **kwargs):
    tmpl = get_template(name)
    if tmpl is None:
        raise Exception('Unable to locate template %s'%name)
    return tmpl.render(**kwargs)
