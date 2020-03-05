

def parse_version(ver):
    try:
        parts = ver.split('.')
        return tuple(map(int, parts))
    except ValueError:
        return None

def ring_to_s3c_version(ver):
    ring_ver = parse_version(ver)
    return '.'.join(map(str, [7, *ring_ver[1:]]))
