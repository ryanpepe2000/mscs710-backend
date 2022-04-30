"""
Encapsulates all utility functions needed across Matrix Systems

@date 4/27/22
@author Christian Saltarelli
"""


def clean_error_msg(msg):
    return msg.translate({ord(c): None for c in "[]'"})
