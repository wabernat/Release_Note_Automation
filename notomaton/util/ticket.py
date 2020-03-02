

def parse_version(ver):
    try:
        major, minor, patch = ver.split('.')
        return int(major), int(minor), int(patch)
    except ValueError:
        return None

def ring_to_s3c_version(ver):
    ring_ver = parse_version(ver)
    return f'7.{ring_ver[1] + 5}.{ring_ver[2]}'