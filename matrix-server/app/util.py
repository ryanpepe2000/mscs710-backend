"""
Encapsulates all utility functions needed across Matrix Systems

@date 4/27/22
@author Christian Saltarelli
@author Ryan Pepe
"""


def clean_error_msg(msg):
    return msg.translate({ord(c): None for c in "[]'"})


# Method from psutil library, slightly modified to display 'KB' instead of 'K' etc...
# Original method can be found here: https://github.com/giampaolo/psutil/blob/master/psutil/_common.py
def bytes_to_amt_per_sec(n, format="%(value).1f %(symbol)s/s"):
    symbols = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i + 1) * 10
    for symbol in reversed(symbols[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return format % locals()
    return format % dict(symbol=symbols[0], value=n)
