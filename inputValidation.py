import re

IPV4_RE = re.compile(
    r'^(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)'
    r'(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}$'
)

def is_valid_ipv4(ip: str) -> bool:
    return IPV4_RE.match(ip.strip()) is not None