import re


def camel_case(s):
    s = re.sub(r"(_|-)+", " ", s).title()
    return ''.join([s[:]])


name = 'the.righteous.gemstones.s02e04.720p.web.h264-cakes.mkv'

print(camel_case(name))
