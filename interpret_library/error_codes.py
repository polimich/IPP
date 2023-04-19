import sys
from datetime import datetime


class ErrorCodes:
    """ Error codes for errors in interpret.py"""
    badParameter = 10
    inFileError = 11
    outFileError = 12
    xmlError = 31
    syntaxError = 32
    semanticError = 52
    badTypeError = 53
    missingVarError = 54
    missingFrameError = 55
    missingValueError = 56
    badOperandError = 57
    badStringError = 58

def error(message, code):
    """ Prints error message and exits with code"""
    sys.stderr.write(f"({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}): Error: {message}")
    sys.exit(code)


def log(message):
    """ Prints log message"""
    sys.stderr.write(f"({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}): {message}")

