

def parse_version(ver):
    try:
        major, minor, patch = ver.split('.')
        return int(major), int(minor), int(patch)
    except ValueError:
        return None
