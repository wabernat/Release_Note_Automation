

def parse_version(ver):
    try:
        parts = ver.split('.')
        return tuple(map(int, parts))
    except ValueError:
        return None

def trim_version(ver, digits=3):
    parsed = parse_version(ver)
    return '.'.join(map(str, parsed[:digits]))

def ring_to_s3c_version(ver):
    ring_ver = parse_version(ver)
    return '.'.join(map(str, [7, ring_ver[1] + 5, *ring_ver[2:]]))
